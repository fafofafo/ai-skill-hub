---
name: social-media-auto-publish
description: Use when 自动发布到小红书等平台（sau）。含无头安装、patchright 坑、扫码登录。
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [小红书, 自动发布, social-auto-upload, sau, patchright, 无头]
    related_skills: [cdp-browser-automation, free-media-gen, external-content-verification]
---

# 中文社交平台自动发布（social-auto-upload / sau）

基于开源项目 `dreammis/social-auto-upload`（14k+ stars，MIT）——浏览器自动化模拟真实用户上传发布，支持小红书/抖音/B站/快手/视频号/TikTok/YouTube 等。本机已验证：**小红书图文**全链路（2026-09-07）。

## 安装（无头 Linux，已验证）
```bash
mkdir -p ~/tools && cd ~/tools
git clone --depth 1 https://github.com/dreammis/social-auto-upload.git
cd social-auto-upload
uv sync                       # 装 patchright 等依赖
UV_INDEX_URL=https://mirrors.cloud.tencent.com/pypi/simple uv pip install playwright pillow
cp conf.example.py conf.py
# conf.py 关键：LOCAL_CHROME_PATH = ""（必须留空！见坑1）；LOCAL_CHROME_HEADLESS = True
# 装 patchright 专属 chromium（关键！见坑2）
unset PLAYWRIGHT_DOWNLOAD_HOST
.venv/bin/python -m patchright install chromium
```
环境：Python 3.11+、Node、Chrome 可选（实际上不需要系统 Chrome）。国内机器 `uv sync` 需腾讯镜像 `UV_INDEX_URL`。

## 配置三坑（不踩必崩）
1. **conf.py 的 `LOCAL_CHROME_PATH` 必须留空**。若指向系统 chrome（如 `/usr/bin/google-chrome`），patchright 传参 `--disable-field-trial-config` 系统 Chrome 不认 → 启动即崩 `unknown flag`，exit 64。
2. **patchright 要自己的专属 chromium build**（browsers.json revision 1208 "Chrome for Testing"）。用 `python -m patchright install chromium`；**不要**设 `PLAYWRIGHT_DOWNLOAD_HOST=npmmirror`（会 Download failure），用默认官方 CDN `cdn.playwright.dev`。报 `Executable doesn't exist at ...chromium-1208` 就是没装对；**不要**把 playwright 的 chromium-1234 软链成 1208（参数集不兼容照样崩）。
3. **launch 别用 `channel="chromium"`**——同样参数不兼容。改代码用默认 `launch(headless=True)`（本会话已把 `uploader/xiaohongshu_uploader/main.py` 里所有 `channel="chromium"` 去掉，直接默认 launch）。

## 登录（无头 + 手机扫码）
```bash
.venv/bin/sau xiaohongshu login --account <账号名>   # 后台跑，等二维码
```
- 无头模式会把二维码打印成终端 ASCII 并**保存 PNG**：`cookies/xiaohongshu_<账号名>_xhs_login_qrcode_<时间戳>.png`
- **二维码 5 分钟时效**，超时进程退出并清理图片——生成后**立即**把 PNG 发给用户（企微 `MEDIA:` 路径），让用户手机小红书 APP【我→扫一扫】扫码
- 扫码成功 → cookie 存 `cookies/xiaohongshu_<账号名>.json`；`sau xiaohongshu check --account <名>` 校验（返回 `valid`）
- 注意：扫码后绑定的是**用户手机上当前登录的小红书账号**，务必先确认用户用哪个号（主号/小号）再发内容

## 发布图文
```bash
.venv/bin/sau xiaohongshu upload-note --account <账号名> \
  --images /path/img.png [img2.png ...] \
  --title "标题" --note "正文" --tags "标签1,标签2"
```
- 至少 1 张图；封面可用 PIL 生成（中文字体：`/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`，脚本见模板）
- 日志到 `SUCCESS: 🥳 图文发布成功` 即成功；话题标签匹配不到候选会 WARNING 跳过，不影响发布
- 视频：`upload-video`；定时发布：`--schedule "%Y-%m-%d %H:%M"`；多平台命令类同（douyin/bilibili/tencent…）

## 坑：发布卡「冲刺发布图文」无限循环
症状：日志反复 `🏃 小人正在冲刺发布图文`（while True 点发布按钮→等成功 URL→失败重试）。
- **最常见根因：账号未绑定手机号**。创作平台弹提示"你还未绑定手机号…绑定后才可发布笔记"，发布被拦。修复=用户小红书 APP【设置→账户与安全→手机号】绑定。
- 诊断：用 patchright 直接开 `https://creator.xiaohongshu.com/new/note-manager`（storage_state=cookie 文件）读页面文本，看提示/笔记状态；注意首页"最新笔记"只显示部分，完整列表在**笔记管理页**。
- `--debug` 参数未必把截图传到预期路径，别依赖它；直接 DOM 读状态更可靠。

## 内容管理 / 删除
- 笔记管理页 `https://creator.xiaohongshu.com/new/note-manager`（侧边栏"笔记管理"），所有笔记都在这里（草稿/审核中/已发布）。
- 删除：hover 笔记卡片出现操作栏，删除按钮 class `note-card__action-btn--del`（无删除 CLI 命令，用浏览器脚本点）。

## 风险认知（务必告知用户）
- 浏览器模拟 + 持久化 Cookie = 绕过平台人工操作预期，**平台检测可能限流/降权/封号**；项目作者 README 自己都写"降低平台检测风险"。
- 默认策略：**小号/测试号试跑 → 低频发布 → 观察稳定后再考虑主号**；Cookie 只存本地（chmod 600 目录）不泄露。
- 小红书个人号无官方发布 API，所有"自动发布"工具都是这条路，风险不可消除，只能缓解。

## 支持文件
- `templates/make_cover.py` — PIL 生成小红书封面图（1080×1440，中文大字）。
