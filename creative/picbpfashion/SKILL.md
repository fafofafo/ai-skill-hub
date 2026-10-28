---
name: picbpfashion
description: Use when 要超写实女性商业时尚海报提示词（给主题/品牌名，国际先锋时尚广告水准）。含模板与出图流程。
version: 1.0.0
metadata:
  author: p_1bab4a
  license: MIT
  hermes:
    tags: [时尚海报, 超写实, 瑞士平面设计, 建筑几何, 现代主义字体, image2.5]
---

# picbpfashion — 超写实女性商业时尚海报提示词（国际先锋时尚广告水准）

2026-10-22 用户提供完整模板创建（TAVEN 品牌示例，原名 picbpfastion，后重命名为 picbpfashion）。风格：当代都市时装摄影 + 瑞士实验性平面设计 + 建筑几何构成 + 现代主义字体排版 + 克制复古配色。

## 触发
- 用户给主题/品牌名并要求「时尚海报」「超写实女性商业时尚」「先锋时尚品牌广告」「瑞士平面设计」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题（品牌名/歌名/概念）嵌入「<主题>」与主标题位置

## 模板结构（中文，参考 picbpnew 的海报结构，风格换成超写实商业时尚）

请生成一张以「<主题>」为主题的国际先锋时尚品牌广告海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用 Contemporary Fashion Editorial Photography + Swiss modernist graphic design，融合当代都市时装摄影、瑞士实验性平面设计、建筑几何构成与现代主义字体排版。画面呈现超写实商业时尚摄影质感，真实皮肤纹理、细腻毛孔、通透光影、高级时装布光，不要卡通、不要插画、不要3D玩具风。画面左上角放置超大主标题「<主标题/品牌名>」，字体为 bold、立体挤压感、现代无衬线艺术字，带利落描边和清晰投影，醒目且准确，不能写错字。标题是第一视觉焦点，具有很强设计感。画面右侧或中部加入<主题>相关的时尚主体（如原创女性模特/时装造型/品牌视觉元素），以超写实时装摄影呈现，占据画面主要视觉区域，人物与品牌文字形成强烈横向视觉平衡。画面中部或底部加入<主题>相关的时尚生活元素，如<配饰/场景/标语元素清单>，以建筑几何构成与瑞士网格排版融入，增强品牌故事感。画面底部可放大 1 到 2 个代表<主题>文化的巨型时尚元素，例如<品牌符号/产品/配饰清单>。物体比例夸张，可以像建筑一样大，与人物和排版形成超现实时尚拼贴关系。整体配色以<低饱和品牌色系，如薄荷灰绿/陶土红/深青绿/炭黑>为主，克制复古，避免大面积同一高饱和品牌色堆积，强调冷暖对比与舒适留白。构图饱满但层次清晰，元素前后穿插，但主标题必须清晰可读，时尚主体必须明确可辨。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的国际先锋时尚品牌广告海报，高级、冷静、利落而具有明确设计语言，视觉张力足。

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用；若模板已有完整页脚署名 AIXZD ZHAPU PROJECT SERIES 则与 FAFO 标注并存，不冲突）。

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
- 提交遇到队列繁忙/NoneType 报错时前台逐次重试（每次间隔 15-30s）

## 经验
- **生成方式（用户 2026-10-22 指定）**：参考 picbpnew 的海报结构——左上超大立体艺术字主标题（第一视觉焦点）/右侧或中部时尚主体（超写实时装摄影人物）/中部时尚生活元素/底部 1-2 个巨型时尚元素/配色/署名 AIXZD ZHAPU PROJECT SERIES；风格段换成超写实商业时尚（Contemporary Fashion Editorial Photography + Swiss modernist graphic design）
- **来源**：2026-10-22 用户提供 TAVEN 模板创建（原名 picbpfastion，用户 2026-10-22 要求重命名为 picbpfashion）
- **主题替换技巧**：主题=品牌名/歌名/概念时替换「<主题>」与主标题（品牌名）；左上标题/时尚主体（模特/时装造型）/中部元素/底部巨型元素/低饱和品牌色系/署名等全部保留
- **风格识别**：与 picgirl 系（日系写实少女）不同——本技能是商业时尚编辑摄影+平面设计构成；与 picbpnew（波普拼贴）不同——本技能超写实+克制排版
- pic 技能族：pic1-7 + pic-bp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picgirly2k + picgirl + picgirlfgnew + picgirlzh + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picsunny + picbpfashion；触发时按模板区分
