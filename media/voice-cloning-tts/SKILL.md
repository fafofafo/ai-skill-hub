---
name: voice-cloning-tts
description: Use when 克隆音色/语音合成(TTS)。含零样本/固定音色/批量长文合成全流程与坑。
---

# 音色克隆 / 语音合成 (TTS)

把一段干净人声素材克隆成可用的合成音色，或用它合成任意文本语音。默认走硅基流动 CosyVoice2-0.5B API（用户已有 key，零额外部署）。

## 流程

1. **定位素材并验证**：用户说"刚发的素材"时，素材可能是本会话或上个会话的产物（多在 /tmp），先 find 最近音视频文件确认。视频先抽音频：`ffmpeg -y -v error -i in.mp4 -t 10 -vn -ac 1 -ar 44100 -b:a 192k ref.mp3`。要求：单人声、无背景音乐/杂音、发音清晰；参考段 **必须 <30s，建议 8-10s**（取开头最干净一段）。
2. **准备参考文本**：素材若跑过 ASR（如 video-auto-cut 产物带 .srt），直接复用字幕文本；**必须修正 ASR 明显错字**（参考文本越贴合实际发音，克隆越准）。无字幕就先转写（faster-whisper / SenseVoice）。
3. **取 key**：硅基流动 key 在 `~/.hermes/config.yaml` 的 `auxiliary.vision.api_key`（base_url `https://api.siliconflow.cn/v1`），只读进脚本，不要回显。
4. **调合成接口**：`POST https://api.siliconflow.cn/v1/audio/speech`，JSON body：
```json
{
  "model": "FunAudioLLM/CosyVoice2-0.5B",
  "voice": "",
  "input": "<要合成的文本>",
  "response_format": "mp3",
  "references": [{"audio": "data:audio/mpeg;base64,<参考音频base64>", "text": "<参考文本>"}]
}
```
`voice` 传空串 = 动态零样本克隆；返回二进制音频直接落盘。原生 urllib/requests 把 references 放 JSON 顶层即可（OpenAI SDK 示例的 extra_body 只是封装差异）。
5. **验证并交付**：`ffprobe` 查时长确认非空；用 `MEDIA:/path.mp3` 发回用户听效果。

## 要点与坑

- **动态克隆（voice=""）不需要实名认证**；`/v1/uploads/audio/voice` 预置音色需要实名认证。临时试音/换音色一律走动态克隆。
- **input 文本不要加空格**（官方文档明示）；换行用中文标点即可。
- 计费按 input 的 UTF-8 字节数，定价页实测 **¥0.05/千字符**（1 万字 ≈ ¥0.5）——报成本直接按字符数 × 0.00005 算，不凭"极便宜"含糊描述。
- **同账号可用的语音模型**（`GET /v1/models` 实测 98 个模型，语音类 3 个）：`FunAudioLLM/CosyVoice2-0.5B`（克隆+TTS 主力）、`fnlp/MOSS-TTSD-v0.5`（对话式）、`FunAudioLLM/SenseVoiceSmall`（ASR）；另有厂商 ASR 标免费。需要 ASR→TTS 全链路时不用另找 key。
- **期望时延**：预置音色合成 3.6 秒音频实测 21.9 秒返回（含冷启动）；批量长文务必并发 + 重试，不要串行等。
- 参考音频 base64 会较大（10s mp3 ≈ 240KB），直接内联进 JSON 即可，无需文件上传。
- 音色像不像取决于参考段质量；多试不同 8-10s 段，选听感最干净的。
- **真人音色对外/商用有授权风险**：克隆博主/他人声音用于用户自测没问题，对外发布前提醒用户先取得授权或换自己的声音。

## 固定音色（长期复用）

用户要"存成固定音色/以后直接用"时：`POST https://api.siliconflow.cn/v1/uploads/audio/voice`，multipart/form-data：
- 字段：`model=FunAudioLLM/CosyVoice2-0.5B`、`customName=<名字>`、`text=<参考文本>`
- 文件：`file=<参考音频mp3>`
- 响应 `{"uri": "speech:<name>:<id>:<id>"}`，之后合成请求 `voice=<uri>` 即可，不再需要 references。
- **音色库统一存 `~/项目目录/音色库.md`**（含 uri/来源/用法）。用户说"用XX的声音"先查该文件拿现成 uri，别重新克隆。
- **customName 只支持字母/数字/下划线/连字符 ≤64 字符**（中文报 code 20048 "Invalid custom name"）→ 用拼音做 customName（wangzuxian 等），中文名登记进音色库（中文名↔拼音 uri 对照），对用户仍用中文名；批量传多个音色逐个 `curl -F file=@` 直接看响应 uri（脚本传 key 易踩空导致 uri 为空，单条 curl 最稳）。
- 上传接口文档称需实名认证，实测未实名也通过；若遇实名报错，提示用户去 cloud.siliconflow.cn 完成实名后重试。动态克隆 voice="" 始终不受影响。

## 批量合成长文案（实测流水线）

1. **ASR 文案预处理**：ASR 提取的文案（faster-whisper 等）通常无句号、每行一个断句 → 每行末尾加"。"形成口播节奏；**修正专有名词错字**（人名/片名/公司名如"家和→嘉禾""飞音计划→飞鹰计划"），念出来才不别扭。
2. **切块**：按 ≤300 字/块切（单次 input 太长会超限）；input 内不留空格/换行。
3. **并发合成**：`ThreadPoolExecutor(max_workers=3)` 逐块调 `/v1/audio/speech`（固定音色 `voice=<uri>`），每块重试 3 次。
4. **拼接**：生成 concat list（`file '/tmp/chunk_XX.mp3'`）→ `ffmpeg -y -f concat -safe 0 -i list.txt -c copy out.mp3`。
5. **交付**：`MEDIA:/path` 发文件，报时长/字数/分段数；说明修正过的错别字，并问是否需要调整（语速/某段重念/还原原文）。

可复用脚本：`scripts/batch_synth.py`（读 chunks.json + uri → 并发合成 → concat）。

## 方言/跨语言

CosyVoice2 支持中英日韩、粤语/四川话/上海话等，参考段语言不限。
