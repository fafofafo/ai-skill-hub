---
name: code-driven-video
description: Use when 代码程序化生成视频（p5.js 逐帧+headless），复刻 Opus 5.5 代码直出 MV。
---

# 代码直出视频（程序化动画 MV）——纯代码、零视频模型、零成本

用 LLM 写 p5.js 代码逐帧绘制画面 → headless Chrome 逐帧截图 → ffmpeg 合成。**不用任何图像/视频生成模型**。
这是 Opus 5.5「代码直出 MV」思路的可复刻版（bittide/donald 同路线，2026-09-28 本机 P0 全链路验证：15s/450 帧/46s 渲染）。

## 触发
- 用户要「动画 MV / 代码直出动画 / 程序化视频」（非 AI 生视频、非静态图片轮播）
- 复刻 Opus 5.5 写代码画视频的工作流
- **跑 lemo-opuscar 风格库 demo**（59 种代码做片风格，如 backrooms/皮影/浮世绘）：见 `references/lemo-opuscar-styles.md`（2026-10-27 实测跑通流程+坑）

## 管线总览
```
MP3/音频 → 预分析(节拍+能量→timeline JSON) → LLM 写 p5.js sketch(内嵌 timeline)
→ headless Chrome 逐帧渲染(noloop+redraw) → ffmpeg 合成+音频 → 抽帧验证
```
全链路约 6 分钟（含分析/写码/渲染/合成）；CPU 软件渲染约 10fps 真实速度（450 帧 46s），长片后台跑。

## Step 1 · 音频预分析 → timeline JSON
**必须预分析驱动动画，不用实时 FFT**：headless Chrome 无音频设备，p5.sound 实时 FFT 不可靠。
```bash
ffmpeg -y -v error -i in.mp3 -ar 8000 -ac 1 -f s16le pcm.raw
# python: 每 50ms 一窗算能量 e + 过零率 zc；节拍=能量包络峰值+200ms 抑制窗
# 输出 timeline.json: {duration, beats:[t], fps, e:[...], zc:[...]}（e/zc 按 50ms 帧索引）
```
## Step 2 · 写 p5.js sketch
- **timeline 数据必须内嵌进 HTML**（`__TIMELINE__` 占位替换）：file:// 加载下 fetch() 受 CORS 限制，外链取不到
- 动画按帧查询：`t = frameCount/FPS` → `e = TL.e[floor(t*20)]`；节拍触发脉冲环/粒子爆发/加速旋转
- **必须 `noLoop()` + `window._p5Ready = true`**：headless 渲染脚本靠 redraw() 逐帧推进，无 noLoop 会跳帧/重复帧
- 每个画布元素（背景/粒子/频谱柱/几何）用能量 e 与节拍驱动，体现「音乐驱动」而非纯随机动画

## Step 3 · headless 逐帧渲染（scripts/render_mv.js）
```bash
NODE_PATH=<p5js-skill>/scripts/node_modules node scripts/render_mv.js sketch.html --frames 450 --output frames \
  --chrome <Playwright chromium 路径>
```
- puppeteer-core 需手动 npm install（装到 p5js skill 的 scripts/ 下；export-frames.js 用的是 puppeteer 完整版，别混）
- chromium 用 **Playwright 缓存版**：`~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome`

## Step 4 · ffmpeg 合成
```bash
ffmpeg -y -v error -framerate 30 -i frames/frame-%04d.png -i in.mp3 \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -c:a aac -b:a 128k -shortest -movflags +faststart out.mp4
```

## Step 5 · 验证（必须）
- **抽 4+ 个时间点帧 MD5 必须不同**（证明动态非静态重复帧）
- vision 看帧：确认配色/元素/无叠字无溢出，节拍密集段视觉丰富
- ffprobe 核时长 = 音频全长、尺寸合理

## 铁律（血泪坑）
1. **snap 版 chromium 不能用**：`/usr/bin/chromium` 与指向它的 google-chrome 是 snap，AppArmor 挡 file:// 访问和 /tmp 写入（`ERR_FILE_NOT_FOUND` / `Permission denied`）。用 Playwright 缓存的独立 deb 二进制
2. **noLoop + redraw 逐帧**：见 Step 2，违反则帧不同步
3. **timeline 内嵌**：见 Step 2，违反则画布空白（fetch 失败）
4. 节拍检测阈值：`max(mean_e*1.5, 0.05)`，相邻峰 <200ms 抑制；阈值过高会漏拍
5. 合成 `-shortest` 保证与音频同长；`-framerate 30` 与帧数/FPS 一致

## 相关
- **本技能已被 `code-driven-mv` 取代**：code-driven-mv 含完整更新（频谱柱配色/JPEG 长片/toDataURL/交叉淡化/官方歌词字幕等全部血泪坑）。做代码直出 MV 一律加载 `code-driven-mv`。
- **lemo-opuscar 风格库是独立路线**（three.js 渲染，非 p5.js）：59 种代码做片风格，稀疏克隆+静帧渲染流程、字体缺失/headless-shell 两个坑见 `references/lemo-opuscar-styles.md`
- 环境：node v26、puppeteer-core（p5js skill scripts/）、Playwright chromium（~/.cache/ms-playwright/chromium-1234/）、ffmpeg 6.1
- 参考：p5js 技能（创作规范/性能细节）、musicvideo 技能（歌词逐字同步可复用词级时间戳）
- 案例：~/项目目录/outputs/mv_poc/code_mv_poc_15s.mp4（15s 竖版 720x1280 霓虹 MV）
