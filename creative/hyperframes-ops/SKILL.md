---
name: hyperframes-ops
description: Use when 用 HyperFrames/lemo-opuscar 做代码直出视频（卡点/MV/风格库静帧渲染）。
---

# HyperFrames 卡点视频（music-to-video，2026-10-09 实测跑通）

把音乐变成卡点 MP4：beatgrid 分析节拍 → 切帧 → 每帧 HTML 构图 → headless 渲染。

## 本机环境（已配好）
- CLI: `npx --yes hyperframes@0.8.143`（Node 24，PATH=/home/ubuntu/.local/node/bin）
- 浏览器: `HYPERFRAMES_BROWSER_PATH=/data/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`（必须设，否则找 snap chromium 失败）
- beatgrid 分析器: `/data/tmp_work/hf_skill/skills/music-to-video/scripts/analyze-beatgrid.py`（用 /home/ubuntu/venvs/wespeaker-venv/bin/python，已装 librosa）
- skill 源码: /data/tmp_work/hf_skill/（ghfast.top 克隆）

## 工作流
1. 截取音乐段（整曲太长先截 demo）：`ffmpeg -ss 0 -t 30 -i in.mp3 assets/bgm.mp3`
2. 分析节拍：`python analyze-beatgrid.py assets/bgm.mp3 -o audiomap.json` → 看 BPM/beats_sec/phrases（乐句边界=切换点）
3. 配图：RunningHub t2i（默认复古旅行海报风），图是竖版 880x1184，需 ffmpeg 预处理成 1920x1080（原图居中+模糊填充背景）
4. 写 index.html：根 div 必须 `data-composition-id="root" data-start data-duration data-width data-height`（**必须第一个**，audio 放 root 里面）；每场景一个 data-composition-id 的 div + 节拍边界切换；中文字体需 `@font-face src:local()` 声明否则 lint 报错；根级 `<audio id data-start data-duration data-has-audio=true src=assets/bgm.mp3>` 才有声音；动效用 GSAP timeline 存 window.__timelines
5. `npx hyperframes check` → 0 errors 后 `npx hyperframes render`（30s 片约 3 分钟，软件渲染较慢）

## lemo-opuscar（另一代码做片风格库，实测静帧跑通）
- 59 种代码渲染风格（MIT），纯 node+playwright，无需 Claude Code 也能独立跑。
- 完整实测配方（稀疏克隆 / 完整 chromium 要求 / 字体坑 / still.mjs 渲染）→ `references/lemo-opuscar.md`

## 坑
- **root_missing_composition_id/dimensions**：根 div 缺 data-composition-id/data-width/height，且必须排 body 第一个
- **font_family_without_font_face**：中文需 @font-face local() 声明
- **静音**：没有根级 `<audio data-has-audio>` 会 hasAudio:false
- **图片 >2MB 不内联**：警告不影响渲染
- **snap chromium 被删**后必须设 HYPERFRAMES_BROWSER_PATH

## 交付
- 默认发 QQ 邮箱 345469023@qq.com（email-send-stdlib 技能），IMAP 读回验证
