---
name: hyperframes-video
description: Use when 用 HyperFrames 做 HTML→MP4 视频（音乐卡点/设计感）。已实测跑通。
---

# HyperFrames 本地视频渲染（HTML → headless → MP4）

HeyGen 开源框架（Apache-2.0，`heygen-com/hyperframes`，2026-10 已实测跑通）。把一段音乐 + 可选图片/视频变成**节拍同步**的 MP4：分析节拍 → 切成帧 → 每帧一个 HTML 构图 → headless Chrome 逐帧截图 → ffmpeg 合成。**无素材纯排版也能出片**（文字/动效卡点）。适合做「设计感/客户展示级/科技感」视频；日常「发歌+图片做 MV」仍走 mv1（频谱+歌词）。

## 本机环境（已配好，勿重装）
- Node ≥22：`/home/ubuntu/.local/node/bin/node`（v24 可用）——PATH 里加 `export PATH=/home/ubuntu/.local/node/bin:$PATH`
- ffmpeg 系统自带；playwright chromium 已迁 `/data/ms-playwright/`（`/home/ubuntu/.cache/ms-playwright` 是 symlink）
- librosa 在 `/home/ubuntu/venvs/wespeaker-venv`（beat 分析用）

## 步骤
1. 装 CLI（一次性）：`npx -y hyperframes --version`（当前 0.8.x）
2. 建项目：`npx hyperframes init <name> --non-interactive --example=blank --skill=music-to-video`
3. 放音乐：`mkdir -p assets renders && cp <music> assets/bgm.mp3`（演示先截短：`ffmpeg -ss 0 -t 15 -i assets/bgm.mp3 assets/bgm.mp3`）
4. **beat 分析（卡点基础）**：从 skill 仓库拉分析脚本（GitHub 被墙用 ghfast.top：`git clone --depth 1 --filter=blob:none --sparse https://ghfast.top/https://github.com/heygen-com/hyperframes.git && git sparse-checkout set skills/music-to-video skills/hyperframes-core`），然后 `wespeaker-venv/bin/python skills/music-to-video/scripts/analyze-beatgrid.py assets/bgm.mp3 -o audiomap.json --print`——输出 BPM/鼓点分类/强弱拍/能量/硬停，卡点切换时间对齐它的真实节拍
5. 写帧：每帧一个 `data-composition-id` 的 div，`data-start`/`data-duration` 对齐节拍；动效用 GSAP 时间线注册到 `window.__timelines["<id>"]`（模板见 repo 的 index.html 结构）
6. 校验：`npx hyperframes check`（布局采样/对比度/动画 0 错误）
7. 渲染：`npx hyperframes render` → `renders/*.mp4`（4 秒片 ~9 秒渲染）

## 铁律/坑（实测踩过）
- **HYPERFRAMES_BROWSER_PATH 必须显式指到现有 headless shell**：默认找系统 chromium，但本机 snap chromium 已删 → 报 `requires the chromium snap`。设 `export HYPERFRAMES_BROWSER_PATH=/data/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`
- **音轨静音坑**：渲染默认 `hasAudio:false`——必须在 index.html 根级加 `<audio id="bgm" data-start="0" data-duration="<总长>" data-has-audio="true" src="assets/bgm.mp3"></audio>`（带 id，mixer 才拾取）；否则画面有、声音没。
- **声音只看节拍，别自己再测**：analyze-beatgrid.py 是唯一节拍源；舒缓音乐时别硬卡 beat（按乐句/能量走）
- 渲染完验证：`ffprobe -show_entries stream=codec_type,codec_name` 确认有 h264 视频轨 + aac 音轨

## 交付
- 渲染产物放 `/data/tmp_work/<proj>/renders/`；给用户可 `MEDIA:/path.mp4` 直发
- 与 mv1 分工：mv1=日常频谱+歌词 MV（已固化自动走）；HyperFrames=设计感/纯排版/客户展示级卡点（说"用 HyperFrames 做"才走）

## 相关
- mv1 / musicvideo：ffmpeg 频谱+歌词路线
- code-driven-video：p5.js 代码直出（另一条 headless 路线）
