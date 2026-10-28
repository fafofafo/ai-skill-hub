---
name: xiaohongshu-auto-publish
description: Use when 小红书图文自动发布/账号管理/删笔记。含 social-auto-upload 踩坑与信息图流水线。
version: 1.0.0
metadata:
  hermes:
    tags: [小红书, 自动发布, 图文, xhs, social-auto-upload, 运营]
---

# 小红书自动发布与账号运营

## When to Use
- 用户要求在小红书发图文/笔记、管理账号、删笔记、批量运营。
- 内容生产流水线：选题 → 文案 → RunningHub 复古信息图 → 自动发布。

## 工具与核心命令
工具目录 `~/tools/social-auto-upload/`（venv 在 `.venv/`），账号=用户测试（小号，cookie 已存）：
```bash
cd ~/tools/social-auto-upload
.venv/bin/sau xiaohongshu login --account 用户测试   # 无头扫码登录（终端二维码+本地png）
.venv/bin/sau xiaohongshu check --account 用户测试  # 校验 cookie
.venv/bin/sau xiaohongshu upload-note --account 用户测试 --images 图1.png 图2.png --title "标题" --note "正文" --tags "标签1,标签2"
```
发布后不回显图给用户（用户看发布页即可），只报发布成功。

## 登录（无头扫码）
`login` 生成终端二维码 + 保存 png（`cookies/xiaohongshu_<账号>_xhs_login_qrcode_*.png`），**5 分钟过期**，发给用户手机小红书 APP 扫。账号须已绑定手机号，否则发布被拒。

## 安装/环境踩坑（重要，勿重复踩）
1. **patchright 专属 chromium 必须装**：`unset PLAYWRIGHT_DOWNLOAD_HOST; .venv/bin/python -m patchright install chromium`（走官方 CDN cdn.playwright.dev，勿设 npmmirror 会失败）。
2. **代码里 launch 参数**：`channel="chromium"` 会导致 `unknown flag disable-field-trial-config` 崩溃；`LOCAL_CHROME_PATH` 指向系统 chrome 同样崩溃。改为默认 `launch(headless=True)` + conf.py 里 `LOCAL_CHROME_PATH = ""`（已改好，勿还原）。
3. 缺 playwright 模块时：`uv pip install playwright`（uv venv 无 pip）。

## 发布正文限制
- **正文硬限约 1000 字**，安全值 ≤600 字。超长会卡死在"小人正在冲刺发布图文"无限循环（点发布→等成功URL失败重试）。卡住先杀进程，精简正文重发。
- 细节内容尽量转信息图（用户偏好），正文做概述引导。

## 删笔记（无 CLI 删除，走浏览器自动化）
`~/tools/runhub/记忆系列/del_note.py`（可改关键词复用）：
- 打开 `creator.xiaohongshu.com/new/note-manager`，**枚举 `div.note-card` 按标题 inner_text 匹配**（`text=` 选择器不可靠）；`inner_text` 必须 await。
- hover **卡片本体** → 点 `[class*='action-btn--del']` → 确认弹窗按钮是 **「确定」**（不是"删除"）。
- 发布后笔记可能显示多条同名（审核/已发布多状态），逐个删。

## 内容生产流水线（用户偏好）
1. **配图全走 RunningHub 复古风**（见 skill runhub-image-gen）：封面+每层/每点一张信息图，一图一知识点，通俗易懂。
2. **图中文字用中文**：AI 文生图生成中文会翻车 → RunningHub 生成无文字底图 + PIL 叠中文（脚本模板见 runhub-image-gen）。
3. **配图与文字强绑定（2026-09-07）**：每张底图意象直指该层/该点讲的技术机制（如"会话历史"=检索档案柜+放大镜，"程序记忆"=锻造技能工具），不是泛泛复古氛围图。
4. **技术细节要真（2026-09-07）**：正文/图内文字从技术角度写机制原理实现（如 prompt caching / memory flush / FTS5 / Honcho / SKILL.md 三层加载），不要笼统科普。正文≤600-800 字，细节放图。
5. 文案：标题抓痛点，正文概述+引导，标签 3-5 个。

## 批量出图注意（2026-09-07）
RunningHub 连发多张可能报 `421 TASK_QUEUE_MAXED`（data=None 异常）——任务队列上限，等 30s 自动重试即可，不是余额问题。批量脚本必须带重试循环。

## 合规红线
- 不引导站外（微信/QQ/私我）= 封号重灾区；成交走小红书店铺（薯店，数字商品类目，身份证即可）。
- 不用绝对化用语（包会/最全/100%）。不刷量。
