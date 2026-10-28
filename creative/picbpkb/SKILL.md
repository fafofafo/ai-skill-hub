---
name: picbpkb
description: Use when 要暗调禅意冷峻风海报提示词（给主题/歌名，大地色低饱和）。含模板与出图流程。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [海报, 暗调, 禅意, 冷峻, 大地色, 胶片颗粒, image2.5]
    related_skills: [picbpnew, picbp, pic-poster-family]
---

# picbpkb — 暗调禅意冷峻风海报提示词（大地色·低饱和·侧逆光）

基于 picbpnature 开发（2026-10-16 用户指定，训练方式同 picbpnature）：保留 picbpnew 全部结构/约束/署名，**仅替换画质/色调/风格三段**为「暗调禅意冷峻」视觉（英文风格描述，image2.5 对英文风格词更敏感）。原 picbphjq，2026-10-16 用户重命名为 picbpkb。

## 触发
- 用户给主题并要求「暗调」「禅意」「冷峻」「大地色」「低饱和」「胶片颗粒」「侧逆光」「明暗对照」「chill」「禅」「冷淡风」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文结构 + 英文风格段（保留原英文句法）

## 参考视觉特征（2026-10-16 用户提供，image2.5 实测规范，英文原文）
**画风/色调/风格（暗调禅意冷峻）：**
- darkened earthy base tones interwoven with dusty teal, muted desaturated palette → 暗化大地色基底 + 灰蒙青绿交织，低饱和褪色色调
- heavy restrained film grain → 厚重而克制的胶片颗粒
- high-contrast side-backlighting (side rim light) → 高对比侧逆光（侧轮廓光）
- volumetric smoke scattering → 体积烟雾散射
- chiaroscuro light/shadow contrast → 明暗对照（Chiaroscuro，卡拉瓦乔式）
- minimalist composition, generous negative space → 极简构图、大量留白
- subtle motion of leaves and fabric caught in wind → 风中叶片与织物的微妙动态
- zen-like stillness with cold menace → 禅意静寂与冷峻威胁并存
- 氛围关键词：静、冷、克制、电影感、隐忍张力

## 模板结构（中文结构，保留 picbpnew 全部结构与约束，画质/色调/风格段替换为暗调禅意冷峻英文描述）

请生成一张以「<地点>·<主题>」为主题的暗调禅意冷峻风拼贴海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用 darkened earthy base tones interwoven with dusty teal, muted desaturated palette, heavy restrained film grain, high-contrast side-backlighting (side rim light), volumetric smoke scattering, chiaroscuro light/shadow contrast, minimalist composition, generous negative space, subtle motion of leaves and fabric caught in wind, zen-like stillness with cold menace。融合现代插画、街头艺术、平面设计与拼贴插画。整体为平面插画质感，不要摄影写实，不要3D玩具风。画面左上角放置超大主标题「<主标题>」，字体为 bold、立体挤压感、现代波普艺术字，带利落描边和清晰投影，醒目且准确，不能写错字。标题是第一视觉焦点，具有很强设计感。画面右上区域表现<地点>老城与<地域>风情建筑，包含<建筑细节清单>等具有<地域>特色的建筑细节，建筑紧凑排列，层层叠叠，形成密集的老街氛围。画面中部加入具有<地点>城市气息的街头元素，如现代招牌、<地域>店铺标识、骑楼下店铺、木质招牌、<地域>窗花、当代路牌，以及具有地方感的交通与生活元素，增强街巷故事感。画面底部前景放大 2 到 3 个代表<地点>文化的巨型元素，例如<本地特产/文化元素清单>。物体比例夸张，可以像建筑一样大，从左右底角延伸进画面，与街区建筑形成超现实拼贴关系。整体色彩以暗化大地色与灰蒙青绿为主——低饱和褪色色调，darkened earthy base tones interwoven with dusty teal, muted desaturated palette，深色背景与侧逆光高光形成明暗对照（chiaroscuro），胶片颗粒厚重克制，留白充分，形成冷峻、禅意、隐忍张力的高级感，避免整张画面被单一颜色覆盖。构图饱满但层次清晰，元素前后穿插，几乎没有无意义空白，但主标题必须清晰可读，地标建筑必须明确可辨。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的历史街区商业插画海报，暗调禅意感强，视觉张力足，极繁但有秩序，具有电影海报与文创海报的高级设计感。

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用）。

## 出图前固定追加句（英文风格段适用）
模板含英文风格段（image2.5 风格词），发给 RunningHub 前在提示词最后补一句：`输出的英文全部翻译成中文`（防英文文字残留；模板结构/约束本身保持英文不变）。

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
- 长中文提示词写入文件再 $(cat) 传入，避免 shell 转义；t2i 前把 markdown 符号清理为纯文本更稳

## 经验
- 与 picbpnature 的差异（画质/色调/风格三处）：
  1. 画质：扁平矢量示意图 → **厚重克制胶片颗粒 + 体积烟雾散射 + 侧逆光**
  2. 色调：纯白+蓝灰+青绿 → **暗化大地色 + 灰蒙青绿，低饱和褪色**
  3. 风格：学术机制图 → **禅意静寂 + 冷峻威胁（zen-like stillness with cold menace）**
- **结构来源（用户 2026-10-16 定）**：模板结构、建筑/街头/巨型元素、署名、最终输出句**全部照搬 picbpnew**，只替换画质/色调/风格三段；与 picbpgd/picbpclean/picbpsky/picbpdarkblue/picbpnature 做法一致
- **主题替换技巧**：主题=歌名/概念时把意象物化成「巨型元素」嵌进底部（孤独→孤树/灯塔/枯山；武侠→剑/斗笠/孤亭；思念→旧物/信封/孤舟）；背景按意境选（荒野/雾林/废墟）
- **风格记忆点**：暗化大地色+灰蒙青绿低饱和 + 侧逆光轮廓光 + 体积烟 + 明暗对照 + 大量留白 + 风中微动；克制不花哨
- pic 技能族：pic1-7 + picbp + picbpnew + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb；触发时按模板区分
