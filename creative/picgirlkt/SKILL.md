---
name: picgirlkt
description: Use when 要复古犯罪片美女海报提示词（给主题/歌名，Pulp Crime Neo-noir，高亮版）。含模板与出图流程。
version: 1.1.0
metadata:
  hermes:
    tags: [海报, 复古犯罪, 黑色电影, 美女, Neo-noir, 70年代, 胶片, 明亮, 主题派生, image2.5]
---

# picgirlkt — 复古犯罪片美女海报提示词（Pulp Crime Neo-noir，主题派生式）

2026-10-20 创建：**内容生成方式参考 picgirl（主题派生式）**——画风固定为复古犯罪片电影感（源自 picbpkt v1.1.0 明亮版），人物/背景不再固定，每次按主题自动派生「一个美女主体 + 与主题相关的合适背景」，左上角超大主标题=主题。主题自定义，画风永远参考原始提示词。

## 触发
- 用户给主题并要求「复古犯罪」「Pulp Crime」「黑色电影」「Neo-noir」「美女」「70年代美式」「胶片颗粒」「高对比硬光」风格
- 用户发来主题/歌名，要求「按 picgirlkt 出图」——自动派生美女主体+相关背景
- 注意：输出**只要提示词内容**；人物外貌/服装/背景场景由主题派生；画风关键词全部保留

## 模板结构（主题派生式，画风固定）

<主题>（可附：主题相关画面内容提示），复古犯罪片电影感，styled cinematic realism，retro pulp crime cinema，1970s America mixed with 1990s independent crime film aesthetic，gritty neo-noir atmosphere，35mm analog film look，photochemical color grading，可见细胶片颗粒，柔和光晕，soft highlight bloom，烟雾氛围，有机瑕疵，暖钨丝灯为主光源，高调布光，画面整体明亮通透，背景明亮不压暗，浅阴影，柔光漫射，cinematic lighting，无大面积死黑，配色为 faded crimson red，mustard yellow，tobacco brown，dirty cream，muted teal——浓郁但略褪色，1个<由主题派生的美女外貌：发型发色/五官气质/年龄感>，<由主题派生的服装与姿态>，<由主题派生的合适背景场景>，画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、复古犯罪片标题艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点，仰视角度，面部特写，真实皮肤纹理，细腻毛孔，通透光影，眼神明亮有高光，cool detached characters，stylish rebellious mood，dark humor，电影级构图，色彩明快，复古怀旧。

### 派生规则
- **主体**：1 个美女，外貌（发型/发色/气质）和服装按主题合理设计——主题是歌名/地名/概念时，用其氛围联想人设（如「富士山下」→和服少女+樱花；「海阔天空」→海边风衣女子；「华侨节」→复古裙装女子+唐人街庆典）
- **背景**：与主题强相关的合适场景，一句话点明（地点/天气/元素），不脱离主题
- **标题（参考 picbpnew）**：左上角超大主标题=主题，bold 立体艺术字+描边+投影，第一视觉焦点，不能写错字
- **画风固定保留**：复古犯罪片/neo-noir/70年代美式/褪色绯红芥末黄烟草棕脏奶油柔和青蓝/35mm 胶片颗粒光化学调色/暖钨丝灯高调布光明亮通透浅阴影/背景明亮不压暗/烟雾氛围/写实皮肤纹理（这串永远不动）
- **构图固定**：仰视角度 + 面部特写（保留 picgirl 原始视觉语言）

## 画风基准（复古犯罪片，源自 picbpkt v1.1.0 明亮版）
- **定义**：styled cinematic realism, retro pulp crime cinema——1970s America mixed with 1990s independent crime film aesthetic，gritty neo-noir atmosphere
- **人物**：realistic human characters（写实人物）、natural skin texture（自然皮肤纹理）、cool detached characters（冷静疏离角色）、stylish rebellious mood（时尚叛逆氛围）、dark humor（黑色幽默）
- **环境**：vintage American environments（复古美式环境）、raw and authentic production design（粗粝真实的制作设计）、tactile textures（可触质感）
- **配色**：faded crimson red（褪色绯红）、mustard yellow（芥末黄）、tobacco brown（烟草棕）、dirty cream（脏奶油）、muted teal（柔和青蓝）——rich but slightly desaturated colors（浓郁但略褪色）
- **光效（v1.1.0 改高亮）**：warm tungsten lighting（暖钨丝灯）为主光源，**高调布光（high-key lighting）**——画面整体明亮通透、背景明亮不压暗、浅阴影、柔光漫射、soft highlight bloom，人物面部与背景都清晰可见，无大面积死黑；cinematic lighting（电影感布光）
- **质感**：35mm analog film look、photochemical color grading（光化学调色）、visible fine film grain（可见细胶片颗粒）、subtle halation（柔和光晕）、soft highlight bloom（柔和高光泛光）、smoky atmosphere（烟雾氛围）、organic imperfections（有机瑕疵）

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
- **2026-10-20 创建**：内容生成方式参考 picgirl（主题派生式：美女主体+相关背景随主题、画风冻结、左上角主题标题）；画风取自 picbpkt v1.1.0（复古犯罪片，明亮版）
- **2026-10-20 v1.1.0 光影再调高亮**：夜景主题实测仍偏暗（用户指定「画面明亮一些」）——加 high-key lighting 高调布光、背景明亮不压暗、无大面积死黑；仅「明亮通透」对夜景不足
- **核心记忆点**：复古犯罪片 + neo-noir + 70年代美式 + 褪色绯红芥末黄烟草棕脏奶油柔和青蓝（浓郁略褪色）+ 35mm 胶片颗粒光化学调色柔光晕烟雾 + 写实角色自然皮肤纹理 + 冷静疏离时尚叛逆黑色幽默 + **高调布光整体明亮背景不压暗**
- **主题替换技巧**：主题=歌名/地名/概念时嵌入开头并附一句画面内容，人设与画风关键词全部保留；主题是歌名/人物事件时可作「犯罪/悬疑/叛逆」联想
- **安全提示（继承 picgirl）**：写实人物主题避开「紧身/身材线条」等描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny；触发时按模板区分
