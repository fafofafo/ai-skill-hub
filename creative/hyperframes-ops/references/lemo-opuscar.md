# lemo-opuscar 代码做片风格库（实测跑通静帧）

59 种代码渲染影片风格（MIT / CC BY 4.0），纯 node + playwright，**无需 Claude Code 也能跑**（README 声称 Built for Claude，实际渲染器独立）。风格提示词见各 `styles/<风格>/STYLE.md`，可借鉴风格写法到自家 MV 流程。

## 快速跑通（稀疏克隆 + 静帧渲染）
1. 稀疏克隆（ghfast.top 代理）：
   `git clone --depth 1 --filter=blob:none --sparse https://ghfast.top/https://github.com/lemomo-ai/lemo-opuscar.git`
   `cd lemo-opuscar && git sparse-checkout set core styles/<风格>`
2. `npm install`（仅 playwright-core + three 两个依赖）
3. `export PLAYWRIGHT_CHROME=/data/ms-playwright/chromium-1234/chrome-linux64/chrome`（**必须用完整 chromium**；headless-shell 会报 "A network error"）
4. 修字体坑：`demo/fonts` 的 woff2 **不在 git 仓库**（只有 fonts.css 引用）→ 页面 `document.fonts.load()` 抛 "A network error occurred"，READY 永不置位。解法：Google Fonts 下载同款 IBM Plex ttf 放入 demo/fonts，把 fonts.css 的 woff2 引用改成 ttf。
5. 渲染静帧：`node core/render/still.mjs styles/<风格>/demo 3.6 35.82 --prefix bf_ --out <dir>`（SwiftShader 软件渲染每帧约 4.5s）
6. 画面验证：PIL 统计亮度/黑边占比/中心色，确认非黑屏且与 STYLE.md 描述一致再交付。

## 坑
- 完整 build.sh（TTS→whisper→1433 帧渲染→混音 mux）在无 GPU 本机约 2-3 小时——只验证静帧层即可，音频链未测不承诺。
- 风格清单：README `styles/` 下列出 59 种（backrooms / ukiyoe / risograph / pixel-rpg / shadow-puppet 等），挑风格先读对应 STYLE.md 的 Essence 与 Materials 段。
