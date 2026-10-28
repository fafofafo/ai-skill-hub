---
name: picbpbookroom
description: Use when 要14mm超广角书房摄影海报提示词（给主题/画面，低角度对称构图+前景帘中景桌后景书架，picbpnew 骨架）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 写实摄影, 超广角, 14mm, 书房, 对称构图, 纵深, picbpnew骨架, image2.5]
---

# picbpbookroom — 14mm 超广角书房摄影海报提示词（picbpnew 骨架版）

2026-10-23 创建：**生成方式参考 picbpnew**（主题嵌入开头/左上角超大主标题/底部系列署名/右上 FAFO 标注），内容保留 picreal2 的写实摄影画风（14mm 超广角镜头/低角度/对称构图/前景虚化帘幕/中景聚焦书桌/背景书架/强烈纵深/深层聚焦分层）。

## 触发
- 用户给主题/画面并要求「超广角」「14mm」「书房摄影」「对称构图」「纵深聚焦」「低角度」风格
- 用户发来主题，要求「按 picbpbookroom 出图」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头 + 左上主标题

## 模板结构（picbpnew 骨架 + picreal2 画风，中文）

请生成一张以「<主题>」为主题的写实摄影海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。画面采用 14mm 超广角镜头拍摄、略微低机位仰角、左右严格对称构图，形成强烈空间纵深。前景是虚化的薄纱帘幕<按主题可替换前景元素>，边缘柔和散焦；中景清晰聚焦于一张深色木质书桌，桌面摆放摊开的画册手稿、茶壶、台灯与文房器物<按主题可替换桌面物件>；背景是一整面到顶的深色木质书架，层层塞满书籍与画框，形成密集纵向线条。三层景深分明——前景虚、中景实、背景深，透视线条向画面深处汇聚，超广角带来边缘拉伸与外扩畸变。画质为高像素写实摄影——真实木质纹理、纸张纤维、金属与陶瓷反光、自然明暗过渡、细节锐利。色调偏暖，木质与灯光营造温馨静谧氛围，主要光源来自顶部吊灯与窗外自然光，侧光与顶光结合形成柔和阴影。画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、沉稳金属质感艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。右上角粗体字标注：FAFO工作室

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用）。

## 交付规则（2026-10-12 用户定，pic 全部适用）
- 生成的图片**直接发当前频道**（MEDIA: 路径），不再只发邮箱
- 图片**先不清理**、保留在服务器（用户 2026-10-14 更新：暂不删，后续可能复查/复用）
- 长提示词/中间产物落 /tmp 的可清理，图片文件保留

## 出图（完整流程最后一步）
提示词生成后直接调默认文生图工具出图（RunningHub，见 runhub-image-gen 技能）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 880×1184 即 3:4）
- 长中文提示词写入文件再 $(cat) 传入，避免 shell 转义

## 经验
- **2026-10-23 创建**：picreal2 的 picbpnew 骨架版——主题嵌入开头+左上超大主标题+底部系列署名+FAFO；内容保留 14mm 超广角书房画风（低角度/对称/前景帘幕/中景书桌/背景书架/纵深分层）
- **与 picreal2 区别**：picreal2=英文 Midjourney 参数模板（--ar 16:9/--style raw/--stylize 300/--v 6.1/--no 排除）；picbpbookroom=中文 picbpnew 骨架（3:4/左上主标题/系列署名/FAFO）
- **实测（picreal2 原版·2026-10-23）**：14mm 广角畸变/低角度仰拍/左右对称/前景虚化帘幕/中景书桌（画册茶壶台灯山水手稿）/背景书架塞满书/前中后景纵深分明全到位；暖调木质顶光侧光柔和阴影；无卡通无乱码。**注意**：原版英文模板 --no text 导致 FAFO 未出现，中文骨架版无此参数约束，FAFO 应正常输出
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picpp + pic1960pp + picbpgd + picbpbookroom + picbpwjw + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picreal + picreal2 + picreal3；触发时按模板区分
