---
name: video-auto-cut
description: Use when 口播视频自动剪辑（去静音/气口/加字幕）。服务器 ffmpeg 全自动，POC 已验证。
version: 1.0.0
metadata:
  hermes:
    tags: [视频剪辑, 口播, 静音切除, 字幕, ffmpeg]
---

# 口播视频自动剪辑（POC 已验证 2026-09-18）

口播稿 → 自动去长静音/气口 + 可选烧字幕 → 成品 MP4。服务器无界面全自动。

## 工具
`~/项目目录/tools/video_auto_cut.py`（依赖 ffmpeg + faster-whisper in Hermes venv）
```bash
python3 ~/项目目录/tools/video_auto_cut.py 输入.mp4 --max-gap 1.2 --burn-subtitles --out 输出.mp4
```
参数：`--min-silence`（最短静音 0.6s）/`--threshold`（-35dB）/`--max-gap`（静音保留上限，超出的切掉）

## 流程
1. faster-whisper ASR（带时间戳，中文 small 模型）
2. ffmpeg silencedetect 找静音段
3. 静音 > max-gap 的切到 max-gap（保留气口，不切光）
4. 分段提取 + concat demuxer 合并（**不要用 filter_complex concat**——同文件多路输入会 Error linking filters）
5. 可选烧录 SRT 字幕（--burn-subtitles）

## 实测（2026-09-18）
合成口播 11.5s（2.5s+3s 长静音）→ 8.4s，输出静音段精确 1.2s（max-gap）。

## 坑
- ffmpeg silencedetect/volumedetect 输出在 **stderr**，subprocess 要 capture stderr
- atrim 参数用显式 `start=/end=`
- 同文件多 -i + filter_complex concat 链接失败 → 用分段文件 + `-f concat -safe 0`
- 用户用途/素材待确认：自用（口播出片）还是产品化（接单/卖 Skill）——POC 已完成自用验证
