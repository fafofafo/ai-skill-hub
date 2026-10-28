---
name: bgm-identification
description: "Use when 识别视频/音频的背景音乐曲目。含分离、指纹识别、风格判断。"
version: 1.0.0
metadata:
  hermes:
    tags: [bgm, 背景音乐, demucs, shazam, 音频分析]
---

# 背景音乐识别（BGM Identification）

## When to Use
- 用户问「这个视频/音频的背景音乐是什么」「BGM 能听出来吗」

## 流程
1. **确认有无 BGM**：ffmpeg 提取音频 → `silencedetect=noise=-45dB:d=0.35`。纯口播必有静音间隙；**106s 全程无 0.35s 静音 = 有持续垫底声（BGM/环境声）**。频谱图（showspectrumpic）低频持续能量 + 中高频竖条纹也佐证
2. **分离人声与背景**：demucs `-n htdemucs --two-stems vocals`（输出 no_vocals.wav=纯BGM / vocals.wav）。46s 音频约 45s 算完（CPU）
   - 更轻的替代：原音频是立体声时，`pan=mono|c0=c0-c1` 侧声道相消可去居中的人声（仅剩立体声 BGM 成分）——但**先确认声道数**，单声道这招无效
3. **指纹识别**：shazamio（免费无需 key）识别原声 + 滤波段 + 分离后纯 BGM 段。用 `uv venv` + `uv pip install shazamio`（torch/demucs 走腾讯镜像 `UV_DEFAULT_INDEX=https://mirrors.cloud.tencent.com/pypi/simple`，官方源超时）
4. **风格判断**（识别不出时）：showspectrumpic 频谱图 → 视觉模型分析（电子/国风/钢琴、节奏疏密）
5. **汇报**：命中→曲名+艺人+元数据；未命中→诚实说查不到，给风格描述 + 分离出的纯 BGM 音频（放大 20-25dB）让用户耳朵辨认/手机听歌识曲

## 坑（血泪）
- **版权曲库垫乐（Epidemic Sound/Artlist/剪映曲库类）不在 Shazam 指纹库**，识别器全 miss 是常态，不代表流程失败——如实汇报「查不到曲名」比硬编一个答案强
- 网易云/QQ音乐识曲接口本机不可用（404/bad request）→ 别浪费时间，直接 shazamio
- 提取音频时**别用 `-ac 1`**（会把立体声拍扁，侧声道相消失效）；先 ffprobe 看 channels
- demucs 装 torch 大且慢，腾讯镜像 + uv venv 是正解；别用官方 pytorch index（会超时）
- 分离出的 no_vocals 响度很低（比人声低 ~20dB），识别前要 `volume=20-25dB` 放大
