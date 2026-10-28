---
name: xiaohongshu-content-publish
description: Use when 发布图文到小红书（自动发布+信息图制作+笔记管理）。含全流程与踩坑。
version: 1.0.0
metadata:
  hermes:
    tags: [xiaohongshu, 小红书, 自动发布, 信息图, social-auto-upload]
---

# 小红书图文生产 + 自动发布

## When to Use
- 给用户的账号（默认小号「小红薯5FA9159D」）自动发布图文笔记。
- 制作小红书信息图卡片（每张一主题，图内叠中文技术要点）。
- 管理已发布笔记（删除/替换）。

## 工具栈
- 自动发布：`~/tools/social-auto-upload/`（dreammis/social-auto-upload，CLI `sau`）
  - venv：`.venv/bin/sau`（uv 环境，无 pip）
  - cookie：`cookies/xiaohongshu_<账号>.json`（已持久）
- 配图：RunningHub 复古风底图 + PIL 叠中文（见 runhub-image-gen 与 `~/tools/runhub/` 下各系列 make_cards.py 模板）

## 完整流水线（已验证多次）
1. **登录**（一次性）：`sau xiaohongshu login --account <名>` → 无头浏览器生成二维码（终端 ASCII + PNG）→ 用户手机小红书 APP 扫码。二维码 **5 分钟时效**，过期重新跑。
2. **制作信息图**：RunningHub 生成复古风底图（提示词统一 `no text, no letters, no words`）→ PIL 顶部叠中文大标题 + 底部半透明条叠技术要点。底图意象必须直指该图主题（用户偏好：配图与文字强关联）。
3. **发布**：
```bash
cd ~/tools/social-auto-upload && .venv/bin/sau xiaohongshu upload-note --account 用户测试 \
  --images 封面.png 图2.png ... --title "标题" --note "$(cat /tmp/body.txt)" --tags 标签1,标签2
```
4. **管理/删除**：见 scripts/del_note.py（匹配标题→hover 卡片→点删除→确认弹窗「确定」）。

## 关键坑（血泪，务必遵守）
- **patchright 专属 chromium**：项目用 patchright（非 playwright）。必须装 `python -m patchright install chromium`（官方 CDN，别设 npmmirror 镜像）。`channel="chromium"` 和 `executable_path=系统chrome` 都会因参数不兼容崩（unknown flag `disable-field-trial-config`）；正确写法是默认 `launch(headless=True)` 不带参数。conf.py 的 `LOCAL_CHROME_PATH` 留空。
- **未绑定手机号的号不能发布**：页面提示「绑定手机号后才可发布笔记」，发布会无限「冲刺」循环。让用户先在 APP 绑定。
- **正文限约 1000 字**：超过会在点发布后无限循环（`preparing 冲刺发布图文`）。**控制在 800 字内**，细节全放图里。
- **话题标签匹配不到会自动跳过**（WARNING 但继续发布），不影响。
- 发布成功标志：`图文发布成功，小人开心收工`；期间多条「冲刺」属正常等待，但>3 分钟仍循环=卡住，杀掉查原因。

## 用户偏好（本账号运营）
- 配图**全部走 RunningHub 复古风**（默认风格见 runhub-image-gen），封面+所有配图统一。
- **图片不用发给用户预览**——直接发布，用户去发布页看。
- **尽可能把文字转成配图**（一图一层/一个要点），正文只做概述引导。
- 内容要**技术细节丰富**（原理+实现，从技术角度写，不笼统）。
- 系列主题：AI 进化/自我学习之路（五层记忆、技能系统、多Agent、技能蒸馏、进化复盘、AI安全、AI省钱、验证汇总……）。

## 支持文件
- scripts/del_note.py —— 按标题删除笔记（含确认弹窗处理）
- templates/make_cards.py —— 信息图批量生成模板（RunningHub 底图 + PIL 叠中文 + 队列重试）
