---
name: xiaohongshu-publish
description: Use when 小红书图文自动发布/运营（发删笔记、卖Skill种草）。含工具用法、平台坑、配图偏好。
version: 1.0.0
metadata:
  hermes:
    tags: [小红书, 自动发布, social-auto-upload, 图文, 种草, 运营]
    related_skills: [runhub-image-gen]
---

# 小红书图文自动发布与运营

## When to Use
- 给用户的小红书账号发图文/种草笔记、删笔记、批量运营。
- 用户做「卖 Skill 种草」「AI 内容科普」时（小号「用户测试/小红薯5FA9159D」）。
- 配图一律配合 `runhub-image-gen`（RunningHub 复古风）。

## 工具与账号
- 自动发布工具：`~/tools/social-auto-upload/`（social-auto-upload，CLI=`sau`，用 `.venv/bin/sau`）
- 账号 cookie：`~/tools/social-auto-upload/cookies/xiaohongshu_用户测试.json`（已登录，长期有效）
- 发布：`sau xiaohongshu upload-note --account 用户测试 --images a.png b.png --title "标题" --note "正文" --tags "t1,t2"`
  - 多图直接并列多张图片路径；定时发布加 `--schedule "%Y-%m-%d %H:%M"`
- 删除笔记：`~/tools/runhub/记忆系列/del_note.py "标题关键词"`（用 social-auto-upload 的 venv python 跑）

## 无头扫码登录（重新登录时）
```
.venv/bin/sau xiaohongshu login --account 用户测试   # 后台跑
```
- 生成终端 ASCII 二维码 + 本地 png（cookies/ 下），把 png 发给用户手机小红书 APP 扫码。
- 二维码 5 分钟过期；扫码后 cookie 自动保存。

## 平台规则与坑（实测）
- ⚠️ **未绑定手机号的账号不能发布笔记**：页面弹"绑定手机号后才可发布"横幅，工具会卡在"冲刺发布图文"无限循环。让用户到 APP 绑手机号即可。
- ⚠️ **删除笔记的确认弹窗按钮是「确定」**（不是"删除"）——del_note.py 已按此写死。
- ⚠️ **正文约 1000 字上限**：实测 1228 字卡在"冲刺发布图文"无限循环（发布按钮点后弹正文过长提示，不跳成功页）。**正文控制在 800 字内最稳**；技术细节靠信息图承载，不靠正文堆字。
- ❌ **站外导流是封号重灾区**：笔记/评论/私信/水印出现微信/QQ/"私我"→ 限流封号（2026 打击极严）。合规路径=开通薯店站内成交。
- ❌ 标题/正文避免绝对化用语（"包会/最全/100%"）。
- ⚠️ 浏览器自动化上传属灰色地带（模拟真人+持久 Cookie），有平台检测/限流风险——用户已知情接受，用小号跑，低频发布。

## 用户配图/内容偏好（2026-09-07 明确）
1. **图内不要英文文字**：RunningHub 文生图提示词要求 `no text, no letters, no words`；信息文字用 PIL 叠中文（底图+中文信息图卡片）。
2. **尽可能把文字转成配图**：一图一知识点（信息图卡片），正文精简、图承载内容，通俗易懂。
3. **配图要和文字强绑定**：底图意象要直指该层内容/技术机制（例如"会话历史"配检索档案柜、"技能蒸馏"配锻造链），不是泛泛的复古场景图；图内文字就是该知识点的要点。
4. **技术细节从技术角度展开**：讲真实原理/机制/实现（如 prompt caching、memory flush、FTS5、Honcho、agentskills.io、三层渐进加载），不要概览式一两句；深度不够用户会打回重做。
5. **图片生成后不用发预览**：直接发布，用户自己去小红书看。

## 信息图卡片工作流（推荐）
- 底图：RunningHub 文生图（3:4 竖版，`no text`）+ 复古风默认风格。
- 叠字：PIL + `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`，顶部半透明条叠大标题、底部半透明条叠要点。
- 参考脚本：`~/tools/runhub/记忆系列/make_cards.py`（封面+5 层级卡片示例，直接改 CARDS 列表复用）。
- 单篇配图 3-6 张为宜（小红书最多 9 张）。
- 批量生成脚本：`~/tools/runhub/进化系列/make_cards_all.py`（多套 6 张卡片循环，含 RunningHub 队列满自动重试 + 每张间隔 3s）——新系列直接从它改 CARDS/SERIES。
- 底图提示词统一加 `no text, no letters, no words`（避免 AI 生成乱码英文），信息全走 PIL 中文。

## 发布节奏（实测教训 2026-09-07）
- 单日大量连发有**限流/营销号判定风险**：一天 11 篇后建议停（种草笔记"扣AI引导"曾疑似被下架）；用户已接受建议控制节奏。
- 健康节奏：**每天 1-2 篇**，先跑数据看互动再定方向。批量生产可一次备好，但发布要拉开。

## 卖 Skill 的合规路径
- 站内转化=开小红书个人店（薯店）卖「数字商品」类目（AI工具/电子资料包），身份证即可，保证金 1000 元（可退）、服务费约 2%。
- 上架流程、类目选择、红线细节：见 `references/xiaohongshu-virtual-selling.md`。
- 开店由用户操作（实名+保证金）；种草笔记/商品文案/封面由 agent 全自动做。

## 参考
- `references/xiaohongshu-virtual-selling.md` — 小红书虚拟商品开店规则速查（2026）
- `runhub-image-gen` skill — 配图生成（默认复古风）
