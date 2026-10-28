---
name: picreal2
description: Use when 要14mm超广角书房摄影海报提示词（给主题/画面，低角度对称构图+前景帘中景桌后景书架，英文 Midjourney 参数模板）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 写实摄影, 超广角, 14mm, 书房, 对称构图, 纵深, 英文模板, image2.5]
---

# picreal2 — 14mm 超广角书房摄影海报提示词（英文 Midjourney 参数模板）

2026-10-23 用户提供英文提示词模板固化：14mm 超广角镜头、低角度、对称构图、前景虚化帘幕、中景聚焦书桌、背景书架、强烈纵深、深层聚焦分层——写实摄影质感（--ar 16:9 / --style raw / --stylize 300 / --v 6.1 / --no 排除项）。**内容形式据此自定义（英文写实摄影模板型，非 picbpnew 拼贴骨架）**。

## 触发
- 用户给主题/画面并要求「超广角」「14mm」「书房摄影」「对称构图」「纵深聚焦」「低角度」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为英文；主题/画面嵌入描述位置

## 模板结构（用户提供的固定模板，英文）

14mm ultra-wide lens, low angle, symmetrical composition, foreground blurred curtain, midground focused desk, background bookshelf, strong depth, deep focus layering --ar 16:9 --style raw --stylize 300 --v 6.1 --no text, watermark, logo, cartoon, anime, illustration, 3d render

## 主题替换技巧
- 主题/画面嵌入开头描述（如「<主题画面描述>」+ 后续镜头/构图元素），末尾保留 --ar/--style/--stylize/--v/--no 参数
- 可微调：前景帘幕→对应前景（纱帘/竹帘/虚化绿植）、中景书桌→对应主体（按主题替换桌面物件）、背景书架→对应背景（书墙/窗景/展柜）
- **--no 排除项默认保留**：text, watermark, logo, cartoon, anime, illustration, 3d render

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用；本模板 --no text 排除文字，FAFO 标注冲突时省略或画面外处理）。

## 交付规则（2026-10-12 用户定，pic 全部适用）
- 生成的图片**直接发当前频道**（MEDIA: 路径），不再只发邮箱
- 图片**先不清理**、保留在服务器（用户 2026-10-14 更新：暂不删，后续可能复查/复用）
- 长提示词/中间产物落 /tmp 的可清理，图片文件保留

## 出图（完整流程最后一步）
提示词生成后直接调默认文生图工具出图（RunningHub，见 runhub-image-gen 技能）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 3:4——**注意**：本模板要求 16:9 横版（--ar 16:9），默认 app 输出约 3:4，严格比例需换支持 ratio 的 app 或提示用户）
- 长提示词写入文件再 $(cat) 传入，避免 shell 转义

## 经验
- **2026-10-23 创建**：用户提供英文写实摄影模板——14mm 超广角镜头/低角度/对称构图/前景虚化帘幕/中景聚焦书桌/背景书架/强烈纵深/深层聚焦分层/--ar 16:9/--style raw/--stylize 300/--v 6.1/--no 排除文字水印卡通动漫插画3D
- **与 picreal 关系**：同系列英文 Midjourney 参数模板（同 --ar/--style/--stylize/--v/--no 参数）；区别=picreal 是温暖亭阁古董柜写实，picreal2 是 14mm 超广角书房纵深摄影
- **核心记忆点**：14mm 超广角 + 低角度 + 对称构图 + 前景虚化帘幕中景聚焦书桌背景书架 + 强烈纵深 + 深层聚焦分层 + 16:9 横版 + raw 风格 + 排除文字水印卡通动漫插画3D
- **模板类型**：英文 Midjourney 参数模板（独立模板型，非 picbpnew 骨架）；画幅 16:9 与默认 app 3:4 不符，出图前说明
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- **2026-10-23 实测「FAFO工作室」**：画风全通过（14mm 广角畸变/低角度仰拍/左右对称/前景虚化帘幕/中景书桌+画册茶壶手稿/背景书架塞满书/前中后景纵深分明/暖调木质顶光侧光/写实摄影无卡通）；**FAFO 工作室文字未出现**——`--no text` 排除文字生效，即使从 --no 移除 text 仍随机未出（模型随机性，重跑或正文加强文字权重可解）；默认 app 实际输出 880×1184（约 3:4，非 16:9）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpy2k + picpp + pic1960pp + picbpgd + picbphuge + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbp3d + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + picbp2 + picbp2sunny + piclove + piclovesunny + picgirl + picsunny + picbpfood + picbpghost2 + picbpqinyong + picgirlghost2 + picmanstory + picmanface + picbookface + piccar + picfgcity + picclimb + picrun + picbprun + picgirlrun + picreal + picreal2；触发时按模板区分
