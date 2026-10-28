---
name: ai-voice-cloning
description: "Use when 用户要克隆音色/AI配音/用某人声音念文案。硅基流动 CosyVoice2 全流程。"
version: 1.0.0
---

# AI 音色克隆与配音合成（硅基流动 CosyVoice2-0.5B）

把一段参考语音变成可复用的克隆音色，再用它念任意长文案。全链路已验证（2026-09-19：从口播视频克隆女声→存固定音色→合成 3409 字配音 10:00）。

## 前提
- **SiliconFlow API key**：复用 `~/.hermes/config.yaml` 的 `auxiliary.vision.api_key`（同一 key 可调语音接口），读出来写临时文件，不回显到对话
- ffmpeg（截参考音频/拼接长文案成品）
- 固定音色存档 `~/项目目录/音色库.md`（uri + 来源 + 用法）——新音色先查这里，别重复上传

## 流程

### 1 · 截参考音频（8-10s 干净单人声）
```bash
ffmpeg -y -v error -i 素材.mp4 -t 10 -vn -ac 1 -ar 44100 -b:a 192k /tmp/ref.mp3
```
- 要求：单说话人、无背景音、发音清晰（口播视频天然达标）
- 参考文本：若素材有 ASR 字幕（srt），取对应片段的文字轻度修正错别字；文本越准音色越稳

### 2 · 零样本动态克隆（验证音色，不需上传）
POST `https://api.siliconflow.cn/v1/audio/speech`，JSON：
```json
{"model":"FunAudioLLM/CosyVoice2-0.5B","voice":"","input":"测试句","response_format":"mp3",
 "references":[{"audio":"data:audio/mpeg;base64,<b64>","text":"<参考文本>"}]}
```
`voice` 传空串 = 动态克隆。返回 mp3 直接验证效果。

### 3 · 上传固定音色（方便以后直接用）
POST `https://api.siliconflow.cn/v1/uploads/audio/voice`（multipart/form-data）：`model`、`customName`、`text`、`file`。返回 `uri: speech:<name>:...` → 存入 `~/项目目录/音色库.md`。之后合成用 `voice=<uri>` 即可，不用再带参考音频。

### 4 · 长文案合成（千字级）
1. 文案按 ~300 字切块（用句号等标点边界切，别把字块死）
2. 逐块 POST `/audio/speech`（`voice=<uri>`），`ThreadPoolExecutor(max_workers=3)` 并发，每块可重试 3 次
3. 全部成功后 `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp3` 拼接
4. 用 ffprobe 验总时长再交付

## ⚠️ 必踩坑
- **克隆音色会泄漏参考文本（核心坑，血泪）**：CosyVoice 零样本克隆把参考音频文本的高频词/尾句带进输出（句首/句尾冒出原文的词，如参考音频多讲"不容易"，合成时就莫名吐出"的不容易"）。**修复：合成时 input 前加 `<|endofprompt|>` 标记**（`"input":"<|endofprompt|>" + text`）——实测完全切断泄漏；选参考片段时避开含高频词的段
- **排查"配音有怪词"**：faster-whisper 转写核对；对照实验用系统预置音色（`FunAudioLLM/CosyVoice2-0.5B:anna`）合成同文案，无怪词=克隆音色问题。ASR 小模型误识（"侠侣"→"狭履"）不是 TTS 问题，别误判
- **input 不能含空格**（接口硬性要求）：合成前 `re.sub(r"\s+","",text)` 去所有空白
- **参考音频 <30s**：动态克隆硬限制，10s 最稳
- **ASR 文案通常无句号、按行断句**：每行末尾补"。"再合成，形成口播节奏，否则一口气念到底
- **合成前先修正 ASR 错别字**（专有名词念错最刺耳）：如"家和"→"嘉禾"、"唐寄里"→"唐季礼"；汇报时注明已修正，用户要原文可还原
- **固定音色上传要实名认证吗**：官方文档说用户预置音色需实名，但实测接口可直接调用成功；若报实名错误就告知用户去 cloud.siliconflow.cn 完成认证
- 成本：按合成文本 UTF-8 字节计费，测试句几厘钱，千字文案约几分钱

## 版权边界（用户知情）
克隆真人声音：自用/测试可以；做对外/商用内容需先取得授权。每次交付都提醒一次。

## 广告视频联动（图→广告片，2026-09-19 验证）
画面与配音分离合成：
1. 底图：原图为主 + 背景模糊延伸（`scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];[0]scale=1080:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2`）
2. 运镜：zoompan 缓慢推镜 `z='min(1.0+0.001*on,1.12)':d=<帧数>:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30`（竖屏 9:16 广告）
3. 合成：画面+配音 `-filter_complex "[0:v]fade=t=in:st=0:d=0.8,fade=t=out:st=<时长-1.5>:d=1.5[v]" -shortest`
4. 文案按产品/画面主题写，先配音定总时长，再按时长生成画面

## 相关
- 免费视频生成通道（Agnes Video 2.5 Flash，当前 $0/秒）见 free-ai-video-gen 技能

