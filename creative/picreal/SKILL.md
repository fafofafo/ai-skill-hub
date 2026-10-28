---
name: picreal
description: Use when 要写实温暖亭阁古董柜摄影海报提示词（给主题/画面，白玉青瓷+微尘薄雾，英文 Midjourney 参数模板）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 写实摄影, 亭阁, 古董柜, 白玉青瓷, 微尘薄雾, 英文模板, image2.5]
---

# picreal — 写实温暖亭阁古董柜摄影海报提示词（英文 Midjourney 参数模板）

2026-10-23 用户提供英文提示词模板固化：宏大而有序的温暖亭阁、陈列白玉摆件与青瓷花瓶的古董柜、空气中漂浮的微尘、微湿反光地板、远处薄雾——写实摄影质感（--ar 16:9 / --style raw / --stylize 300 / --v 6.1 / --no 排除项）。**内容形式据此自定义（英文写实摄影模板型，非 picbpnew 拼贴骨架）**。

## 触发
- 用户给主题/画面并要求「写实摄影」「温暖亭阁」「古董柜」「白玉青瓷」「微尘薄雾」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为英文；主题/画面嵌入描述位置

## 模板结构（用户提供的固定模板，英文）

Grand and orderly warm pavilion, curio cabinet displaying white jade ornaments and celadon vases, faint floating dust in the air, slightly wet reflective floor, thin mist in the distance --ar 16:9 --style raw --stylize 300 --v 6.1 --no text, watermark, logo, cartoon, anime, illustration, 3d render

## 主题替换技巧
- 主题/画面嵌入开头描述（如「<主题画面描述>」+ 后续写实场景元素），末尾保留 --ar/--style/--stylize/--v/--no 参数
- 可微调：亭阁→对应场景（庙宇/大殿/藏书楼）、古董柜陈列物→对应器物（按主题替换白玉/青瓷为其他古物）、地板湿度/雾气浓度随氛围
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
- **2026-10-23 创建**：用户提供英文写实摄影模板——宏大有序温暖亭阁/古董柜陈列白玉摆件与青瓷花瓶/空气中漂浮微尘/微湿反光地板/远处薄雾/--ar 16:9/--style raw/--stylize 300/--v 6.1/--no text, watermark, logo, cartoon, anime, illustration, 3d render
- **核心记忆点**：写实摄影 + 温暖亭阁 + 古董柜白玉青瓷 + 漂浮微尘 + 微湿反光地板 + 远处薄雾 + 16:9 横版 + raw 风格 + stylize 300 + v6.1 + 排除文字水印卡通动漫插画3D
- **模板类型**：英文 Midjourney 参数模板（独立模板型，非 picbpnew 骨架）；画幅 16:9 与默认 app 3:4 不符，出图前说明
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- **2026-10-23 实测「FAFO工作室」**（picreal/picreal2/picreal3 三张）：①默认 app **不支持 --ar 16:9**，实际输出 880×1184（约 3:4），要严格 16:9 需换支持 ratio 的 app；②`--no text` 会杀掉 FAFO 标注——picreal、picreal3 把 text 从 --no 移除并在正文写「FAFO工作室」后成功出金色横匾/文字，picreal2 同样移除仍随机未出（属模型随机性，重跑或加强文字权重可解）；③画风复核实测：picreal=长廊亭阁+对称玻璃古董柜+丁达尔微尘+湿地板反光+尽头薄雾全到位；picreal2=14mm 广角畸变/低角度/对称/前景虚化帘幕/中景书桌手稿/书架纵深全到位；picreal3=POV+折叠春园+不可能阶梯+广角畸变荷兰角+晨光过曝+彩色漏光bokeh+褪色胶片颗粒全到位
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpy2k + picpp + pic1960pp + picbpgd + picbphuge + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbp3d + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + picbp2 + picbp2sunny + piclove + piclovesunny + picgirl + picsunny + picbpfood + picbpghost2 + picbpqinyong + picgirlghost2 + picmanstory + picmanface + picbookface + piccar + picfgcity + picclimb + picrun + picbprun + picgirlrun + picreal；触发时按模板区分
