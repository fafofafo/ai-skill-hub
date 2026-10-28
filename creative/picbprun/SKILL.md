---
name: picbprun
description: Use when 要高端运动品牌商业海报提示词（给主题/场景，picbpnew 骨架+跑步 Campaign KEEP GOING）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 运动品牌, 跑步, 商业摄影, 巨型字体, picbpnew骨架, image2.5]
---

# picbprun — 高端运动品牌商业海报提示词（picbpnew 骨架 + 跑步 Campaign）

2026-10-23 用户指定：**生成方式参考 picbpnew**（主题嵌入开头/左上角超大主标题/底部系列署名/右上 FAFO 标注），内容保留 picrun 的运动品牌 Campaign 画风（奔跑运动员后侧45°/巨大超窄纵向英文主视觉字体/冷色高级运动视觉/电影级商业摄影/KEEP GOING 文案系统）。picrun 保留不动。

## 触发
- 用户给主题/场景并要求「运动品牌海报」「跑步 Campaign」「KEEP GOING」「商业摄影海报」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头 + 左上主标题

## 模板结构（picbpnew 骨架 + picrun 内容，中文）

请生成一张以「<主题>」为主题的高端运动品牌商业海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用高端运动品牌 Campaign——国际运动品牌 Campaign、精品旅行杂志与高端商业摄影结合，画面真实、克制、有电影感，强调持续前进、日常坚持、自由奔跑的情绪。画面左上角放置超大主标题「<主标题>」，字体为 bold、立体挤压感、运动品牌艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面主体为<由主题/场景联想的具体场景：城市清晨街道/海岸悬崖公路/雨夜城市/山顶日出/现代跨海大桥/国际机场建筑群>中一名奔跑的年轻运动员，采用背后约45°的后侧视角，人物全身入镜，跑姿自然真实，身材精干有训练感但不过度肌肉化，穿着简洁运动装备：白色或冷灰色技术背心、轻量跑步短裤、白色运动袜，以及<品牌>跑鞋，跑鞋自然融入跑步动作清楚展示鞋侧轮廓与鞋底结构，人体比例自然双腿双脚结构正确跑鞋不变形鞋底与地面关系真实衣服有自然褶皱和风吹效果。画面加入一组巨大、超窄、纵向延伸的英文主视觉字体：<核心大字>，主文字占据画面大部分高度形成强烈视觉锤，人物与字体产生前后遮挡关系，部分文字被人物、建筑、道路或环境元素遮住，让字体像画面中的建筑结构一样参与构图，非对称构图、大面积留白、强烈纵向视觉节奏、高级杂志式排版。辅助标题：KEEP GOING；辅助文案：<一句短文案>；按钮文案：DISCOVER NOW →。色彩采用冷色高级运动视觉：深海蓝、钢蓝、午夜蓝、冰白、钛银、浅青色，根据场景加入少量<点缀色>。光影采用电影级商业摄影效果：冷色环境光、人物边缘轮廓光、自然长阴影、真实环境反射，40–50mm 商业摄影镜头、略微低机位、冻结自然跑步瞬间、背景保留明显空间纵深、跑鞋保持清晰细节、画面兼顾人物产品环境和字体。避免过度霓虹、过曝、高饱和和廉价科技感，不要图库广告感，不要普通健身房宣传海报，不要廉价 AI 光效，不要过度英雄化人物，不要复杂装饰。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的高端运动品牌商业海报，像一套真实发布的国际运动品牌 Campaign，高端商业摄影、精品旅行广告、运动生活方式和现代平面设计结合。

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
- **2026-10-23 创建**：picrun 的 picbpnew 骨架版——主题嵌入开头+左上超大主标题+底部系列署名+FAFO；内容保留运动品牌 Campaign 画风（奔跑运动员后侧45°/巨大超窄纵向英文主视觉字体/冷色高级运动视觉/电影级商业摄影/KEEP GOING 文案系统/5 变量）
- **与 picrun 区别**：picrun=原始模板（4:5 竖版完整文案系统：左上 AI SPORT/辅助标题 KEEP GOING/辅助文案/按钮/右侧竖排/底部 Daily AI Research Circle）；picbprun=picbpnew 骨架（3:4 左上超大主标题+系列署名+FAFO，正文保留跑步元素与 KEEP GOING/辅助文案/按钮）
- **核心记忆点**：picbpnew 骨架 + 运动品牌 Campaign + 奔跑后侧45° + 巨大纵向字体视觉锤 + 冷色高级 + KEEP GOING + 5 变量（场景/核心大字/辅助文案/环境元素/点缀色）
- **安全提示**：写实人物主题避开「紧身/身材线条」等描述（image2.5 安全审查 1501 拦截）；跑步人物注意腿部比例
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpy2k + picpp + pic1960pp + picbpgd + picbphuge + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbp3d + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + picbp2 + picbp2sunny + piclove + piclovesunny + picgirl + picsunny + picbpfood + picbpghost2 + picbpqinyong + picgirlghost2 + picmanstory + picmanface + picbookface + piccar + picfgcity + picclimb + picrun + picbprun；触发时按模板区分
