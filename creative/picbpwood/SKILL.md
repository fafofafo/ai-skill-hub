---
name: picbpwood
description: Use when 要微型木雕作品海报提示词（给主题/人物/摆件，木雕+海报级排版）。含模板与出图流程。
version: 1.0.0
metadata:
  author: p_1bab4a
  license: MIT
  hermes:
    tags: [木雕, 手作, 微缩, 静物摄影, 海报, image2.5]
---

# picbpwood — 微型木雕作品海报提示词（木雕摆件 + 海报级排版）

2026-10-22 基于 picwood（微型木雕手工作品）创建：木雕静物摄影 + 海报级主标题排版。风格：写实静物摄影 + 天然木材质感 + 手工雕刻痕迹 + 木工工作台场景 + 温暖工作室氛围 + 品牌海报构图。

## 触发
- 用户给主题/人物/摆件并要求「木雕」「木雕海报」「手工木雕摆件」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题（人物/摆件/概念）嵌入「主题为XX」与主体设计及主标题

## 模板结构（中文，参考 picbpnew 的海报结构，风格换成木雕艺术）

请生成一张以「<主题>」为主题的木雕艺术海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用 Hand-carved Wood Art / Woodcut Poster，融合木雕浮雕、木板刻画、手工木刻与木艺平面设计。画面呈现天然木材质感、清晰刻刀痕迹、细腻木纹与手工切削面，如真实椴木/橡木雕刻而成，保留手工雕刻的天然粗粝感，不上漆，不出现塑料/树脂/陶瓷质感。整体为木刻浮雕质感，不要摄影写实场景，不要3D玩具风。画面左上角放置超大主标题「<主标题>」，字体为 bold、立体挤压感、木刻艺术字，带利落描边和清晰投影，醒目且准确，不能写错字。标题是第一视觉焦点，具有很强设计感，如用刻刀深凿的效果。画面右上区域表现<主题>相关的地标/建筑/主体，包含<建筑/元素细节清单>等具有<主题>特色的细节，元素紧凑排列，层层叠叠，形成密集的木刻浮雕层次。画面中部加入具有<主题>气息的生活/文化元素，如<主题相关元素清单>，以木雕浮雕形式表现，增强主题故事感。画面底部前景放大 2 到 3 个代表<主题>文化的巨型木雕元素，例如<本地特产/文化元素清单>。物体比例夸张，可以像建筑一样大，从左右底角延伸进画面，与主体形成超现实木雕拼贴关系。整体配色以原木浅橡、焦糖胡桃、深咖木纹、暖米黄、做旧金为主，木色系自然温暖，避免整张画面被单一颜色覆盖。构图饱满但层次清晰，元素前后穿插，几乎没有无意义空白，但主标题必须清晰可读，主体元素必须明确可辨。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的木雕艺术主题海报，手工感强，视觉张力足，极繁但有秩序，具有文创海报与手作海报的高级设计感。

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
- **生成方式（用户 2026-10-22 指定）**：参考 picbpnew 的海报结构——左上超大立体艺术字主标题（第一视觉焦点）/右上区域主题主体/中部主题元素/底部 2-3 个巨型元素/配色/署名 AIXZD ZHAPU PROJECT SERIES；风格段换成木雕艺术（Hand-carved Wood Art / Woodcut Poster，原木浅橡/焦糖胡桃/深咖木纹木色系）
- **来源**：2026-10-22 用户创建 picwood（木雕手工作品）后要求衍生 picbpwood（海报版）并参考 picbpnew 生成方式
- **主题替换技巧**：主题=人物/摆件/概念时替换「<主题>」与主标题（主题名）；左上标题/右上区域/中部元素/底部巨型元素/木色系/署名等全部保留
- **风格识别**：与 picwood（纯木雕作品，无海报标题）不同——本技能带海报级主标题；与 picfood2（美食）/picbpfastion（时尚）不同——本技能木雕手作
- pic 技能族：pic1-7 + pic-bp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picgirly2k + picgirl + picgirlfgnew + picgirlzh + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picsunny + picbpfastion + picfood2 + picwood + picbpwood + picgirlwood；触发时按模板区分
