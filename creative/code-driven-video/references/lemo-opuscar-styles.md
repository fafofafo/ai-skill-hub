# lemo-opuscar 代码做片风格库（Opus 5.5 路线，59 风格）

## 是什么
lemomo-ai/lemo-opuscar：59 种「纯代码做片」风格工具箱，每种风格 = `styles/<slug>/STYLE.md`（风格提示词）+ `demo/`（全代码短片源码：three.js/WebGL 逐帧渲染）+ `DEMO.md`（构建说明）。MIT；无视频模型、无 stock 素材。README 称 Built for Claude/Opus 5.5，但渲染器是纯 node+playwright——**本机实测无需 Claude 也能跑静帧**。

## 快速渲染单个风格 demo 静帧（2026-10-27 本机实测跑通，backrooms）
```bash
# 1. 稀疏克隆（只拉 core + 目标风格；GitHub 被墙用 ghfast.top）
git clone --depth 1 --filter=blob:none --sparse https://ghfast.top/https://github.com/lemomo-ai/lemo-opuscar.git lemo-opuscar
cd lemo-opuscar && git sparse-checkout set core styles/backrooms   # 别把 package.json 加进 set——报 not a directory 会中断整条命令
npm install   # 依赖只有 playwright-core + three（~2s）

# 2. 必须用完整 chromium（headless-shell 会 A network error，见坑 2）
export PLAYWRIGHT_CHROME=/data/ms-playwright/chromium-1234/chrome-linux64/chrome

# 3. 渲染静帧（demo 页面必须 window.READY=true 才渲染；软件渲染每帧 ~4.5s @1920x1080）
node core/render/still.mjs styles/backrooms/demo 3.6 35.82 --prefix bf_ --out /tmp/out

# 4. 验证画面非黑屏：PIL 统计中心 4:3 区亮度 + 黑边占比 + 主色调（后室=暗黄 VHS）
```
完整影片：`build.sh`（TTS→whisper→events→混音→1433 帧渲染→mux），无 GPU 下全片约 2-3 小时，音频链重——本机只做静帧验证，别跑全片。

## 坑（实测）
1. **demo/fonts 的 woff2 字体文件不在 git 仓库里**（git 只跟踪 fonts.css 引用 + OFL 许可文本）。页面 main.js 对 7 种 IBM Plex 字体 `await document.fonts.load()`，字体 404 → 抛 "A network error occurred"，window.READY 永不置位，still.mjs 卡死退出。**修法**：Google Fonts 下载同款 7 个 ttf 放入 demo/fonts，把 fonts.css 的 woff2 引用改成 ttf（`format('truetype')`）。约 5 分钟解决。
2. **playwright-core 必须用完整 chromium**（`/data/ms-playwright/chromium-1234/chrome-linux64/chrome`）；`chromium_headless_shell-1208` 对 three.js 页面报同样的 "A network error occurred"。完整 chrome 需 `--headless=new --no-sandbox` 参数。
3. 无 GPU → 日志出现 `[note] WebGL runs on software rendering`（SwiftShader）是正常提示不是错误，别当成失败。
4. 页面 index.html 用 importmap 引用 `/node_modules/three/...`：npm install 后必须保留 node_modules；稀疏检出时别把 node_modules 排除。
5. 字体缺失只打 optional 警告时别急着判页面成功——**页面 [pageerror] A network error occurred 才是真信号**，模块全 200 也可能因字体 load 失败整体中断。

## 风格清单（59 种 + _template，GitHub API 实测 2026-10-27）
- **剪辑与纪实(8)**：caption-news, newsreel, countdown, city-symphony, visual-investigation, kino-montage, telestrator, news-package
- **证据型影片(8)**：satellite-briefing, briefing-board, lidar-survey, white-model, data-physical, teardown, microscope, archive-lighttable
- **手绘与绘画(7)**：crayon-book, watercolor, ink-wash, impasto, one-line, whiteboard, urban-sketch
- **东亚传统(4)**：shadow-puppet（皮影）, ukiyoe, papercut-red, paper-lantern
- **印刷与版画(5)**：risograph, halftone-dossier, woodcut, engraving, silkscreen-poster
- **图形与字体(7)**：swiss-motion, spy-titles, art-deco, blueprint, stained-glass, pictogram-motion, ascii-crt
- **信息与演示(5)**：dataviz, iso-infographic, dark-keynote, living-screencast, hologram-hud
- **卡通与动画(4)**：rubber-hose, cel-anime-80s, scifi-toon, midcentury-toon
- **游戏(4)**：pixel-rpg, hd-2d, microgame, game-show
- **电影与年代(2)**：silent-film, backrooms
- **材质与3D(5)**：brick-toy, paper-popup, tilt-shift, lowpoly-island, glass-product

## 相关
- 学习背景：伯岩AI课堂《冲上71.1k星的HyperFrames》一文；HyperFrames 与 lemo-opuscar 是两条独立代码成片路线（hyperframes-ops 技能管 HyperFrames）
- 每个风格还有 `DEMO.md`（该风格完整设计文档：分镜/调色/音效/构建说明+坑）与 `STYLE.md`（风格提示词），做新风格借鉴时先读这两个文件
