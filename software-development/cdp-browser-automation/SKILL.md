---
name: cdp-browser-automation
description: Use when 需要控制远程/无头浏览器（CDP 接管、真人过验证码后自动化）。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cdp, chromium, browser, automation, remote-browser, vnc, recaptcha, 远程浏览器]
    related_skills: [overseas-freelancing, blocked-page-recovery, inspecting-hermes-desktop-dom]
---

## When to Use
- 需要**自动操作一个网站**，但该网站拦数据中心 IP（Upwork 403）或登录有 reCAPTCHA（Guru）——服务器端 curl/无头浏览器过不了人机验证。
- 需要"真人过验证码一次，之后 AI 全自动接管"：把浏览器跑在服务器上（VNC WebUI 供真人登录一次），登录会话留在服务器，之后用 **CDP（Chrome DevTools Protocol）** 全自动操作（导航、填表、点按钮、读 DOM）。
- 任何"驱动服务器上的浏览器"的任务（不只接单平台）。

## 核心模式（一句话）
`linuxserver/chromium 容器（VNC WebUI 供真人） + 开启 CDP（--remote-debugging-port + --remote-allow-origins） + 容器内端口转发 + SSH 隧道 + websocket CDP 客户端`

## 部署步骤
1. **起容器**（参考 `references/linuxserver-chromium-cdp.md`）：
   - 映射 WebUI 端口（3002:3000）+ 设 `CUSTOM_USER`/`PASSWORD`（WebUI 登录）
   - `--shm-size=512m`（chromium 崩溃防护）
   - `--restart unless-stopped`
2. **开 CDP**：改容器内 `/usr/bin/wrapped-chromium`，给 chromium 启动参数加：
   - `--remote-debugging-port=9222`
   - `--remote-allow-origins=*`（**必须**，否则 WebSocket 连接被拒 403）
   - 然后 `docker restart <容器>`（cookie 在 /config 持久化，但**重启会丢当前打开标签页与登录会话**——见坑 2）
3. **暴露 CDP**：9222 默认绑容器内 `127.0.0.1`，宿主访问不到。容器内跑 Python 转发脚本 `scripts/port_forward.py`（监听 0.0.0.0:9223 → 转发 127.0.0.1:9222）。容器重建后转发进程丢失，需重跑。
4. **隧道到本机**：`ssh -N -L 9222:<容器IP>:9223 -p 10008 root@<host>`（容器 IP 用 `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <容器>`）
5. **CDP 控制**：用 `scripts/cdp_op.py`（websocket-client）导航/执行 JS/读页面。安装：`uv pip install --python <venv>/bin/python websocket-client`（系统无 pip 时用 uv）。

## 常用 CDP 操作
- 打开页面 + 读标题/URL/正文：`python cdp_op.py --navigate <url>`
- 执行任意 JS（填表/点击/读 DOM）：`python cdp_op.py --js 'document.querySelector(...).click()'`
- 检查登录态：导航到受保护页，读 body 里是否有 "Log In" 还是用户信息

## Pitfalls（血泪教训）
1. **Chrome WebSocket 403**：`Rejected an incoming WebSocket connection from the http://localhost:9222 origin` → 必须加 `--remote-allow-origins=*`（Chrome 111+ 安全限制）。只加 `--remote-debugging-port` 不够。
2. **重启会丢登录**：`docker restart` 后浏览器回到新标签页，**已登录会话可能掉**（标签页丢失；cookie 在 /config 是否保留取决于平台）。**真人登录后不要再动浏览器/容器**；所有配置调整先做再让真人登录。
3. **CDP 只绑 127.0.0.1**：容器外访问不到，必须容器内转发（Python 脚本）到 0.0.0.0。
4. **磁盘满导致拉镜像失败**：`no space left on device` 常发生在镜像**解压**时。Docker 29 用 **containerd snapshotter**（`/var/lib/containerd`）——只改 daemon.json `data-root` 不够，还要迁移/软链 `/var/lib/containerd`（见 references）。否则镜像数据仍写系统盘。
5. **无头环境 browser_exec 打不开重页面**：腾讯云 browser_exec 访问 Guru 超时（curl 200 但浏览器加载不了）。不要只靠 browser_exec 判断"不可达"——curl 200 说明可达，换个方案。
6. **curl 登录不了的平台**：登录表单是 JS 动态渲染（字段不在 HTML）+ reCAPTCHA 时，curl/requests 无解。用 CDP 浏览器 + 真人过一次验证码是正道。
7. **无 GPU 服务器上 Selkies WebUI 黑屏（但 CDP 正常）**：linuxserver/chromium 的 WebUI 视频流在无 GPU 机器上可能全黑（只有工具栏、看不到浏览器窗口），是**视频编码器**问题（GStreamer/编码器无硬件可用），不是浏览器坏了。验证方法：`docker exec` 确认 chromium/labwc 在跑 + CDP `Page.captureScreenshot` 截图正常（说明浏览器本身渲染 OK）。**不要在这上面耗时间**——要么接受黑屏（真人登录用不了 WebUI），要么换方案（用户自浏览器直接操作；Guru 这类不封 IP 的平台用户本机就能登录）。

## 限制与诚实边界
- reCAPTCHA 无法自动过（数据中心 IP 必被拦）；"真人过验证码一次"是唯一合规路径。
- 服务器端无法复用人手机浏览器的登录会话——会话隔离。
- 云安全组/防火墙：WebUI 端口需放行（用户控制台操作）。

## 支持文件
- `references/linuxserver-chromium-cdp.md` — 完整部署配方（含 docker/containerd 磁盘迁移）
- `scripts/cdp_op.py` — CDP 客户端（导航 + 执行 JS，websocket-client）
- `scripts/port_forward.py` — 容器内 9222→9223 端口转发
