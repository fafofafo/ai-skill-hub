---
name: picbpbookface
description: Use when 要极繁主义矢量艺术杂志封面海报提示词（给主题/色彩/标题，picbpnew 骨架+中国神话×现代）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 杂志封面, 极繁主义, 矢量插画, 中国神话, 现代视觉, picbpnew骨架, image2.5]
---

# picbpbookface — 极繁主义矢量艺术杂志封面海报提示词（picbpnew 骨架 + 中国神话×现代）

2026-10-22 用户指定：**生成方式参考 picbpnew**（主题嵌入开头/左上角超大主标题/底部系列署名/右上 FAFO 标注），内容保留 picbookface 的极繁杂志封面画风（中国神话元素×现代视觉语言/复杂线条层层叠加/顶部英文大标题+中文主标题+编号日期栏目名/黑金朱红青绿等色彩方向）。picbookface 保留不动。

## 触发
- 用户给主题/色彩/标题并要求「杂志封面」「极繁主义」「矢量插画」「中国神话×现代」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头 + 左上主标题

## 模板结构（picbpnew 骨架 + picbookface 内容，中文）

请生成一张以「<主题>」为主题的极繁主义矢量艺术杂志封面海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用极繁主义矢量插画——复杂线条、层层叠加、细节密集、色彩丰富、装饰性强，整体像一张已经完成设计的高级艺术杂志封面，中国神话元素与现代视觉语言融合。画面左上角放置超大主标题「<主标题>」，字体为 bold、立体挤压感、杂志封面艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面主体为<由主题联想的神话主体元素：神兽、飞天、龙、凤、麒麟、仙山、宫阙、祥云、星辰、月相、浪纹、火焰纹、丝带、符咒、古代器物>，同时加入现代杂志排版、潮流海报、科技图形、网格线、编号、边框、信息标签、半调网点、印刷颗粒，构图饱满但有清晰视觉中心，主视觉突出，周围加入大量辅助图形和细节。完整文字排版：顶部大标题清晰写「<顶部英文主标题>」，中部或下方中文主标题写「<中文主题标题>」，辅助小字写「<副标题/日期/编号/主题短句>」，顶部标题使用朦胧字、边缘网点渐变、印刷颗粒、杂志封面大字排版，中文标题清楚可读有书法感或现代字体感，加入少量编号、日期、栏目名、竖排小字、边框和信息块，形成完整杂志版式。色彩方向为<填写色彩：黑金朱红青绿/奶白鎏金宝蓝/荧光紫电光蓝/复古米黄朱砂红>，高级时尚现代，不要廉价国潮，不要普通插画感，不要低质感卡通。不要真实品牌Logo，不要水印，不要二维码，不要乱码，不要英文乱字，不要空白无主题，不要简单平铺元素。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的极繁主义矢量艺术杂志封面海报，高级艺术杂志封面完成度。

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
- **2026-10-22 创建**：picbookface 的 picbpnew 骨架版——主题嵌入开头+左上超大主标题+底部系列署名+FAFO；内容保留极繁杂志封面画风（中国神话×现代视觉/复杂线条层层叠加/顶部英文大标题+中文主标题+编号日期栏目名/色彩方向可选）
- **与 picbookface 区别**：picbookface=原始模板（画幅可选3:4-9:16-16:9/无左上主标题）；picbpbookface=picbpnew 骨架（固定3:4 左上主标题+系列署名+FAFO，正文保留杂志排版元素）
- **核心记忆点**：picbpnew 骨架 + 极繁杂志封面 + 中国神话×现代视觉 + 复杂线条层层叠加 + 顶部英文大标题+中文主标题+编号栏目名 + 色彩方向可选
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpy2k + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picbpfood + picbpghost2 + picbpqinyong + picgirlghost2 + picmanstory + picmanface + picbookface + piccar + picfgcity + picbpcar + picbpmanstory + picbpbookface；触发时按模板区分
