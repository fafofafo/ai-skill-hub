# Selkies 黑屏坑（无 GPU 服务器，2026-08 实测）

场景：linuxserver/chromium 远程浏览器（给用户在 WebUI 里登录 Guru 过验证码，AI 再 CDP 接管）。
用户能进 WebUI（看到 Selkies 工具栏），但浏览器窗口内容是**黑的**。

## 诊断结论
- **CDP 一切正常**：`Page.captureScreenshot` 截出的页面渲染完好、窗口 1280x720 maximized、
  chromium 进程/日志无错。黑屏只在 Selkies **视频流**一层。
- 原因：GStreamer 编码（`SELKIES_ENCODER=x264enc,jpeg`），无 GPU 的云服务器上软件编码不出画面。
- 影响：用户**看不到浏览器就没法过 reCAPTCHA** → "远程浏览器"方案整体卡死。
- 容器内没有 ffmpeg/import/xwd 截图工具，别找；用 CDP `Page.captureScreenshot` 拿 base64 PNG
  验证页面渲染（证明问题在显示层而非浏览器）。窗口检查：`Browser.getWindowForTarget` →
  `Browser.getWindowBounds`（应 maximized）。

## 对本接单线的影响（重要决策）
- **Guru 不像 Upwork 封 IP**——用户用自己电脑/手机浏览器直接访问 guru.com 就能登录（住宅 IP +
  真人验证码，完全合规）。**根本不需要远程浏览器**。
- 默认走半自动：AI 找单+写报价（自动），用户自己浏览器粘贴发送。
- 远程浏览器方案只在用户明确要"全自动"且服务器有 GPU/可用视频编码时才值得再试。

## 若真要全自动且无 GPU：备选思路（未验证）
- 让用户在本机浏览器登录 Guru，把**会话 cookie** 导出给 AI（用户不学技术则难办）
- 或换带 GPU/编码的服务器跑 linuxserver/chromium
