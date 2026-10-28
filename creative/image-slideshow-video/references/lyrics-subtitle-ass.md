# ASS 歌词字幕 + 背景乐歌词转录

## ASS 字幕模板（竖版 880x1184 示例）
```ass
[Script Info]
Title: 歌词
ScriptType: v4.00+
PlayResX: 880
PlayResY: 1184
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei,42,&H00FFFFFF,&H000000FF,&H00101010,&H80000000,0,0,0,0,100,100,0,0,1,2.5,1,2,40,40,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:08.00,0:00:21.80,Default,,0,0,0,,{\fad(600,600)}没有承诺 却被你抓得更紧
```
- PlayResX/Y 必须 = 视频尺寸（否则字幕缩放错位）；MarginV≈140 底部显示；WrapStyle 2 智能换行
- 浮现效果 = `{\fad(600,600)}`（淡入/淡出各 600ms）
- 时间轴：前奏 `START`（如 8s）后开始，每行 `STEP = (TOTAL - START) / N`，行 i 起止 = START + i*STEP ~ START + (i+1)*STEP；时间戳格式 `H:MM:SS.cc`

## 从背景乐转录歌词（无歌词文件时）
用硅基流动 ASR（无需本地 whisper）：
```bash
# 0. key 从 config.yaml 取（backup.env 没有硅基流动 key！）：
KEY=$(grep -oE 'api_key: sk-[A-Za-z0-9]+' ~/.hermes/config.yaml | head -1 | sed 's/api_key: //')
# 1. 模型选 Qwen/Qwen3-ASR-1.7B（转录准、连续、漏词少）——SenseVoiceSmall 漏词严重/空段多，只适合粗听
curl -s -X POST https://api.siliconflow.cn/v1/audio/transcriptions \
  -H "Authorization: Bearer $KEY" \
  -F "model=Qwen/Qwen3-ASR-1.7B" -F "file=@voice.wav"
# 返回 {"text":"..."}
```
- **ASR 按音频时长计费（usage.duration=seconds），不耗 LLM token**——细分段总时长不变 = 费用不变；仅转录结果回显进对话是少量 token
- 中文歌 ASR 可能把“没有”误识为“有”——用户给的歌词全文优先

## 逐句对齐时间轴（用户要"字幕和语音同步"时）
- 按 ~13s 一段切音频逐段转录，定位每句歌词真实起止（±1-2s）——勿全局平均（平均可与实际差 25s+）
```bash
# 精确 seek 必须 -ss 放 -i 后（-i 前是快速 seek，mp3 会落到错误位置导致段序错乱/重叠）
ffmpeg -y -v error -i bgm.mp3 -ss $st -t 13 -ar 16000 -ac 1 seg.wav
# 逐段 Qwen3-ASR 转录 → 按转录内容把用户歌词行映射到段窗口，段内多句均分
```
- 间奏/前奏段无歌词 → 对应歌词行跳过；转录为空不代表没歌词（模型漏词），结合前后段推断
- 批量转录串行 API 调用慢（23 段约 5-8 分钟），分 2-3 批跑防超时
