---
name: picbpkt
description: Use when 要复古犯罪片电影感海报提示词（给主题/歌名，Pulp Crime Neo-noir，高亮版）。含模板与出图流程。
version: 1.2.0
metadata:
  hermes:
    tags: [海报, 复古犯罪, 黑色电影, Neo-noir, 70年代, 胶片, 高对比, 写实, image2.5]
---

# picbpkt — 复古犯罪片电影感海报提示词（Retro Pulp Crime / Neo-noir）

2026-10-20 用户提供风格定义并固化：styled cinematic realism, retro pulp crime cinema——1970s 美国混合 1990s 独立犯罪片美学，gritty neo-noir 新黑色电影氛围，35mm 胶片质感。内容形式照搬 picbpnew（主题嵌入开头/左上超大主标题/系列署名/FAFO标注），画质/色调/风格换复古犯罪片三段。

## 触发
- 用户给主题并要求「复古犯罪」「Pulp Crime」「黑色电影」「Neo-noir」「70年代美国」「90s 独立犯罪片」「胶片颗粒」「高对比硬光」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头；主题是歌名/地名/概念时自动联想犯罪片场景

## 风格核心（用户提供的固定描述）
- **定义**：styled cinematic realism, retro pulp crime cinema——1970s America mixed with 1990s independent crime film aesthetic，gritty neo-noir atmosphere
- **人物**：realistic human characters（写实人物）、natural skin texture（自然皮肤纹理）、cool detached characters（冷静疏离角色）、stylish rebellious mood（时尚叛逆氛围）、dark humor（黑色幽默）
- **环境**：vintage American environments（复古美式环境）、raw and authentic production design（粗粝真实的制作设计）、tactile textures（可触质感）
- **配色**：faded crimson red（褪色绯红）、mustard yellow（芥末黄）、tobacco brown（烟草棕）、dirty cream（脏奶油）、muted teal（柔和青蓝）——rich but slightly desaturated colors（浓郁但略褪色）
- **光效（v1.2.0 对齐 picgirlkt 改高亮）**：warm tungsten lighting（暖钨丝灯）为主光源，**高调布光（high-key lighting）**——画面整体明亮通透、背景明亮不压暗、浅阴影、柔光漫射、soft highlight bloom，人物面部与背景都清晰可见，无大面积死黑；cinematic lighting（电影感布光）
- **质感**：35mm analog film look、photochemical color grading（光化学调色）、visible fine film grain（可见细胶片颗粒）、subtle halation（柔和光晕）、soft highlight bloom（柔和高光泛光）、smoky atmosphere（烟雾氛围）、organic imperfections（有机瑕疵）

## 模板结构（中文，主题嵌入开头）

请生成一张以「<主题>」为主题的复古犯罪片电影感海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用 styled cinematic realism, retro pulp crime cinema——1970s America mixed with 1990s independent crime film aesthetic，gritty neo-noir atmosphere。画面主体为<由主题联想的主体，如人物/场景/歌名意象>，置于<由主题联想的复古犯罪片场景，如老旧美式街巷/酒吧/车库/雨夜街道>中，场景包含<主题相关的黑色电影细节，如霓虹招牌、老式汽车、烟雾、电话亭、泛黄海报、深色角落>，粗粝真实的制作设计，冷静疏离氛围。画面左上角放置超大主标题「<主标题>」，字体为 bold、立体挤压感、复古犯罪片标题艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。人物为写实角色、自然皮肤纹理、cool detached characters、stylish rebellious mood、dark humor。材质与质感为 35mm analog film look、photochemical color grading、可见细胶片颗粒、柔和光晕、soft highlight bloom、烟雾氛围、有机瑕疵。配色为 faded crimson red、mustard yellow、tobacco brown、dirty cream、muted teal——浓郁但略褪色。光线为暖钨丝灯为主光源、高调布光、画面整体明亮通透、背景明亮不压暗、浅阴影、柔光漫射、soft highlight bloom、cinematic lighting——无大面积死黑，保留复古暖调但整体明亮。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的复古犯罪片电影感海报，粗粝、叛逆、怀旧、有型。

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
- **2026-10-20 v1.1.0 光影调整**：画面改明亮（用户指定）——暖钨丝灯主光源、浅阴影、柔光漫射、soft highlight bloom，保留复古暖调但不再深阴影高对比阴暗；深阴影/高对比弃用
- **2026-10-20 v1.2.0 对齐 picgirlkt 改高亮**：用户问「默认是否都高亮」——升级为 high-key lighting 高调布光、背景明亮不压暗、无大面积死黑，与 picgirlkt v1.1.0 亮度等级统一
- **核心记忆点**：复古犯罪片 + neo-noir 新黑色电影 + 70年代美式/90s 独立犯罪片 + 褪色绯红芥末黄烟草棕脏奶油柔和青蓝（浓郁略褪色）+ **暖钨丝灯高调布光明亮通透背景不压暗** + 35mm 胶片颗粒光化学调色柔光晕烟雾 + 写实角色自然皮肤纹理 + 冷静疏离时尚叛逆黑色幽默；无怪物无超自然
- **主题替换技巧**：主题=歌名/地名/概念时嵌入开头并附一句画面内容，犯罪片元素与质感光影关键词全部保留；主题是歌名/人物事件时可作「犯罪/悬疑/叛逆」联想
- **风格差异**：与 picbpretro（复古未来电影感，老车+宇宙+冷调胶片）不同——本技能是复古犯罪现实题材，暖钨丝灯+深阴影+高对比，粗粝写实；与 picbpbackroom（后室阈限空间，黄墙荧光+低像素录像）不同——本技能是 35mm 胶片电影感+人物叙事
- **安全提示**：写实人物主题避开「紧身/身材线条」等描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirly2k + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny；触发时按模板区分
