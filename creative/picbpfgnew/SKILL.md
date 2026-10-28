---
name: picbpfgnew
description: Use when 要新复古主义海报提示词（给主题/歌名，New Retro Style）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 新复古, 新复古主义, 复古美学, 当代设计, 商业摄影, image2.5]
---

# picbpfgnew — 新复古主义海报提示词（New Retro Style）

原 picfgnew，2026-10-20 用户重命名为 picbpfgnew（对齐 MV 变体 mvbpfgnew 命名）。

2026-10-20 用户提供风格定义并固化：当代设计重新诠释 20 世纪 60-90 年代复古美学（Mid-century Modern / Space Age / 70s retro / 80s graphic design / 90s commercial photography / retro futurism）。内容形式照搬 picbpnew（主题嵌入开头/左上超大主标题/系列署名/FAFO标注），风格/材质/配色/光效换新复古主义。

## 触发
- 用户给主题并要求「新复古」「New Retro」「复古现代」「Mid-century」「Space Age」「80s 平面设计」「90s 商业摄影」「圆润几何」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头；主题是歌名/地名/概念时自动联想新复古场景

## 风格核心（用户提供的固定描述）
- **定义**：New Retro Style 新复古主义——当代设计重新诠释 20 世纪 60-90 年代复古美学：Mid-century Modern、Space Age、70s retro、80s graphic design、90s commercial photography、retro futurism
- **形态**：圆润流线型工业设计、soft geometry、rounded geometry、capsule shapes、bubble forms、拱形结构与模块化几何
- **配色**：奶油白、米黄、焦糖棕、芥末黄、番茄红、橙色、橄榄绿、薄荷绿、复古青蓝，局部高饱和撞色
- **材质**：高光塑料、磨砂金属、透明亚克力、彩色玻璃、搪瓷、胡桃木、拉丝铝、chrome metal
- **图形语言**：大胆几何排版、粗体无衬线字体、棋盘格、条纹、圆点、渐变与复古印刷图形
- **光效/质感**：现代商业摄影与复古广告融合，柔和棚拍光、硬质阳光与长阴影、柔和 Bloom、轻微胶片颗粒、复古印刷色偏
- **氛围**：干净精致、高级、时尚、怀旧但不陈旧——retro nostalgia with contemporary aesthetics

## 模板结构（中文，主题嵌入开头）

请生成一张以「<主题>」为主题的新复古主义海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用 New Retro Style 新复古主义——当代设计重新诠释20世纪60-90年代复古美学：Mid-century Modern、Space Age、70s retro、80s graphic design、90s commercial photography、retro futurism。画面主体为<由主题联想的主体，如人物/产品/地标/歌名意象>，以圆润流线型工业设计呈现——soft geometry、rounded geometry、capsule shapes、bubble forms、拱形结构与模块化几何。画面左上角放置超大主标题「<主标题>」，字体为 bold、粗体无衬线、复古广告艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。背景与装饰使用大胆几何排版——棋盘格、条纹、圆点、渐变与复古印刷图形，现代商业摄影与复古广告融合。材质以高光塑料、磨砂金属、透明亚克力、彩色玻璃、搪瓷、胡桃木、拉丝铝、chrome metal为主。配色使用奶油白、米黄、焦糖棕、芥末黄、番茄红、橙色、橄榄绿、薄荷绿、复古青蓝，局部高饱和撞色。光线为柔和棚拍光与硬质阳光长阴影结合，柔和 Bloom，轻微胶片颗粒，复古印刷色偏。整体干净精致、高级、时尚、怀旧但不陈旧——retro nostalgia with contemporary aesthetics。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的新复古主义海报，高级时尚，怀旧精致。

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
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 3:4）
- 长中文提示词写入文件再 $(cat) 传入，避免 shell 转义；t2i 前把 markdown 符号清理为纯文本更稳

## 经验
- **核心记忆点**：60-90年代复古美学当代化 + 圆润胶囊几何（soft/rounded/capsule/bubble）+ 奶油米黄焦糖撞番茄红青蓝 + 高光塑料/磨砂金属/亚克力/铬 + 棋盘格条纹圆点渐变 + 棚拍光+长阴影+Bloom+胶片颗粒
- **主题替换技巧**：主题=歌名/地名/人物事件时嵌入开头并附一句画面内容，新复古元素与配色关键词全部保留
- **风格差异**：与 picbpretro（欧美复古未来电影感，老车+宇宙+冷调胶片）不同——本技能是当代设计感的干净精致复古广告风；与 picbpzh（昭和日系未来，热闹消费都市+特摄）不同——本技能偏国际 Mid-century 高级时尚
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny；触发时按模板区分
