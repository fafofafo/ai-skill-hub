---
name: picclimb
description: Use when 要真实户外编辑摄影×手工拼贴户外海报提示词（给主题）。含模板与出图流程。
version: 1.0.0
metadata:
  author: p_1bab4a
  license: MIT
  hermes:
    tags: [海报, 户外, 编辑摄影, 手工拼贴, 地形信息, 品牌广告, image2.5]
---

# picclimb — 真实户外编辑摄影×手工拼贴户外海报提示词（QUECHUA Campaign 风）

2026-10-23 用户提供完整模板创建（QUECHUA「PLAY OUTSIDE.」示例）。风格：真实户外编辑摄影 × 手工拼贴海报 × 地形信息设计 × 现代平面排版，轻量日常户外探索调性（非极限挑战）。

## 触发
- 用户给主题/户外单品并要求「户外海报」「户外品牌 Campaign」「真实户外编辑摄影」「拼贴户外」「抓绒/徒步/露营单品海报」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题/品牌/主标题嵌入对应位置

## 模板结构（中文，QUECHUA 示例可整体替换主题/品牌）

请生成一张 QUECHUA 户外 Campaign 海报，画面比例 4:5竖版，质量 8K UHD，风格为 真实户外编辑摄影 × 手工拼贴海报 × 地形信息设计 × 现代平面排版。整体效果必须像高级社交媒体广告和户外杂志封面的结合体，并且 full-bleed、no outer border、background to canvas edge。主题为 “PLAY OUTSIDE.”，调性真实、轻量、可进入，突出 日常户外探索 的舒服感，而不是极限挑战感。主角是一位 24岁左右的拉美女生，中长深色头发扎起，肤色健康，面部真实自然，眼神明亮，有一点冷晨户外的清醒感。她穿着 QUECHUA 浅米白抓绒上衣，外搭轻量户外马甲或薄外套，下身深色徒步裤。动作是 在冷清晨的山间步道上向前行走，一只手轻扶背包肩带或自然摆臂，状态放松但目标明确。场景为 冷晨山路 / 低温山谷步道，天空清亮，空气偏冷，远山层次清晰，地面带自然石路与草木。摄影风格要真实克制，光线偏清晨自然光，体现衣物蓬松保暖质感和真实户外氛围。镜头感为 50mm 环境人像，画面需兼具人和景的联系。画面只突出 一个核心产品：QUECHUA 抓绒上衣，重点刻画抓绒面料、保暖层次、拉链结构、衣领设计和真实穿着褶皱。产品必须穿在人物身上，自然融入，不要独立悬浮商品图。整体色彩以 Quechua 蓝 为图形主色，辅以 暖石灰、米白、森林绿。加入 一个巨大不规则户外蓝手绘色块，占画面约一半，带纸面肌理、轻微干刷与丝印感，作为整张海报的视觉锚点。拼贴图形以 等高线、路线标记、手绘箭头、海拔数据、指南针符号 为主，少量即可，布局要高级有节奏。可加入轻微纸张纤维、复印颗粒、套印偏移，让整张图像一本山地 Field Journal 的封面。左上角品牌文字：QUECHUAOUTDOOR EQUIPMENT主标题：PLAY OUTSIDE.辅助文案：Built for whatever the trail brings.底部 CTA：DISCOVER MORE →请在底部页脚加入辅助品牌信息：AIXZD ZHAPU PROJECT SERIES这部分要与整张图的编辑信息系统融合，像一个系列项目标识，整洁、克制、不喧宾夺主。整体必须传达一种 轻量、日常、舒服、真实、人人都能开始的户外探索感，而不是极限挑战。成品要像 抓绒保暖单品的品牌海报，但核心仍然是人和自然的关系。

## 主题替换技巧
- 主题/品牌/主标题替换：品牌名（QUECHUA→用户品牌）、主标题（PLAY OUTSIDE.→主题句）、辅助文案/CTA 同步换
- 人物可换：24岁拉美女生→按主题换主角（肤色/发型/年龄/服装单品），保持真实户外编辑摄影质感
- 场景可换：冷晨山路→对应户外场景（林间/溪谷/露营/雪地），保持清晨自然光、真实克制
- 核心单品换：抓绒上衣→用户单品（冲锋衣/徒步鞋/背包），产品必须穿/戴在人物身上
- 图形锚点保留：巨大不规则主色手绘色块（占画面一半）+ 等高线/路线/箭头/海拔/指南针拼贴 + 纸张纤维/复印颗粒/套印偏移
- 色彩方向按品牌主色调整（Quechua 蓝→品牌主色 + 暖石灰/米白/森林绿辅助）

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用；模板已有底部 AIXZD ZHAPU PROJECT SERIES 页脚则与 FAFO 标注并存，不冲突）。

## 交付规则（2026-10-12 用户定，pic 全部适用）
- 生成的图片**直接发当前频道**（MEDIA: 路径），不再只发邮箱
- 图片**先不清理**、保留在服务器（用户 2026-10-14 更新：暂不删，后续可能复查/复用）
- 长提示词/中间产物落 /tmp 的可清理，图片文件保留

## 出图（完整流程最后一步）
提示词生成后直接调默认文生图工具出图（RunningHub，见 runhub-image-gen 技能）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 3:4）
- 长中文提示词写入文件再 $(cat) 传入，避免 shell 转义；t2i 前把 markdown 符号清理为纯文本更稳；提交队列繁忙时前台逐次重试

## 经验
- **2026-10-23 创建**：用户提供 QUECHUA「PLAY OUTSIDE.」完整模板——真实户外编辑摄影×手工拼贴×地形信息×现代平面排版；调性轻量日常可进入（非极限挑战）；主角穿核心单品自然融入（无悬浮商品图）；巨大不规则主色手绘色块占画面一半作视觉锚点；等高线/路线/箭头/海拔/指南针拼贴；纸张纤维/复印颗粒/套印偏移的 Field Journal 封面感；Quechua 蓝主色；左上品牌文字/主标题/辅助文案/CTA/底部系列标识
- **核心记忆点**：真实户外编辑摄影 + 手工拼贴（等高线/箭头/海拔/指南针）+ 巨大不规则主色色块锚点 + 核心单品穿在人物身上 + 轻量日常户外调性 + 纸张纤维复印颗粒套印偏移 + 品牌色主色
- **与 picfood2/picbpfastion 区别**：本技能是户外品牌 Campaign（人物+单品+地形拼贴），不是美食/时尚海报
- pic 技能族：pic1-7 + picbp + picbpnew + picbpzh + picbpfgnew + picbpy2k + picpp + pic1960pp + picbpgd + picbphuge + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbp3d + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + picbp2 + picbp2sunny + piclove + piclovesunny + picgirl + picsunny + picbpfood + picbpghost2 + picbpqinyong + picgirlghost2 + picmanstory + picmanface + picbookface + piccar + picfgcity + picgirlfgcity + picclimb；触发时按模板区分
