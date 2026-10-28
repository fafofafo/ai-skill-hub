---
name: siliconflow-voice-cloning
description: "Use when 克隆音色或合成配音（CosyVoice2）。含防泄漏标记、上传、验证。"
version: 1.0.0
metadata:
  hermes:
    tags: [tts, 音色克隆, cosyvoice, siliconflow, 配音]
---

# SiliconFlow 音色克隆与配音（CosyVoice2-0.5B）

## When to Use
- 用户要「克隆某声音/音色」「用XX的声音念这段」「给视频/广告配音」
- 素材：参考音频 8-10s 干净单人声（<30s），必须能拿到对应转写文本

## 关键：<|endofprompt|> 防泄漏（血泪，必做）
**CosyVoice 零样本克隆会把参考音频的文字内容“吐”进合成结果**（句首/句尾冒出参考文本的词句，如参考文本含"不容易"→输出开头冒"的不容易"；含尾句"于是他就选择了这份工作"→开头冒整句）。

**修复（实测有效）：input 前缀加 `<|endofprompt|>`**：
```json
{"input": "<|endofprompt|>" + 要合成的文本}
```
- 对照实验实锤：同一文案，系统预置音色无泄漏，克隆音色泄漏；加标记后 0 泄漏（ASR 验证）
- 预置音色（固定上传的 voice uri）和动态音色（voice="" + references）都会泄漏，都要加标记
- fnlp/MOSS-TTSD-v0.5 克隆仍泄漏 → 别用，用 CosyVoice2
- 上传参考音色时也选不含高频词的干净段落，双保险

## 接口速查
- base: `https://api.siliconflow.cn/v1`，key 用 config `auxiliary.vision.api_key`（同 SiliconFlow key）
- **固定音色上传**：`POST /v1/uploads/audio/voice`（multipart）model=`FunAudioLLM/CosyVoice2-0.5B` + customName + text=参考音频转写 + file → 返回 `uri: speech:<name>:...`，之后 voice 参数用它
- **合成**：`POST /v1/audio/speech` body {model, voice, input, response_format: mp3}
- **动态音色**（不预上传）：voice="" + references=[{audio: dataURI(base64), text}]（同样加 endofprompt）
- 按输入文本 UTF-8 字节计费，便宜（一条广告 ≈ 几厘钱）

## 流程
1. 提取参考音频段（ffmpeg 截 8-10s），ASR 拿准确转写文本
2. 上传固定音色或直接用动态音色
3. 合成：每段 input 前缀 `<|endofprompt|>`；长文案分段（每段 ≤300 字），concat 拼接
4. **必测**：合成后 faster-whisper 转写验证——检查无泄漏（参考文本词）、无错字
5. 交付音频

## 用户偏好
- 广告/配音长文案分段合成再拼接（ffmpeg concat），别一条超长
- 交付时附时长/字数；音色 uri 记入 `~/项目目录/音色库.md` 便于复用
