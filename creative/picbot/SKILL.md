---
name: picbot
description: Use when 要巨大机甲机器人海报提示词（给主题，机械设计随主题派生，3:4）。含六元素验收与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 机甲, 机器人, 高达, 装甲核心, CGI, 黑色金色, 主题派生式, 六元素, image2.5]
    related_skills: [picgirly2k, pic-poster-family]
---

# picbot — 巨大两足机甲机器人海报（主题派生式·CGI 机械设计）

2026-10-26 创建：`picgirly2k` 的**机械向主题派生版**：巨大两足机甲机器人主体 + 与主题相关的背景，验收方式与 picgirly2k 一致（**独立模板型，不以 sunny 五元素区间为准，按风格意图验收**）。提示词为用户提供的完整英文 CGI 机械设计模板（高达/装甲核心美学），主题派生=机甲细节/城市场景/主标题随主题微调，画风三段固定。

## 触发
- 用户要求「picbot」「机甲」「机器人」「高达」「装甲核心」
- 主题要「机甲 / 机器人 / 巨大机械 / 战争机械」的海报
- 注意：输出**只要提示词内容**；**机甲设计与场景随主题派生**，画风要素固定

## 画风定义（固定，勿改）
| 要素 | 内容 |
|---|---|
| 画种 | 逼真 CGI 渲染、超详细机械 greeble 表面、动漫机械影响设计（高达/装甲核心美学）、电影关键艺术品质、8K 超详细 |
| 主体 | 巨大的两足机甲机器人直接走向镜头，极低蠕虫眼睛角度观看，强调它在远处城市上空的高耸规模 |
| 配色 | 主要是黑色和炮金属灰色装甲，深黑色关节/底盘/凹陷机械部分，肩/胸核心/头冠/前臂通风口/小腿/脚有光泽金色装甲板 |
| 细节 | 头/上躯干：成角度人形头部+刀片状金色波峰/鳍（像角向上向后扫）+窄眼镜式眼睛+厚装甲颈领融合宽方肩+红色面板嵌体机械通风口；手臂：右臂举弯近躯干紧握沉重拳头+金色前臂钢板+肘部黑色关节机制，左臂垂下握巨大未来步枪/大炮朝臀部垂向地面+长方形工业武器带通风口瞄准镜；躯干：宽大分层胸甲+金色中心核心面板+两侧黑钢板+白色接缝电缆机械细节+装甲腰部/臀部+金色臀部防护；腿脚：厚实承重腿+白黑镶板+金色膝踝+宽大机械脚+金色脚趾脚后跟+行走扬起灰尘碎屑云+中步暗示向前运动巨大重量；表面：密集 greeble——液压活塞/通风口/暴露接头/面板接缝/铆钉/分层装甲板，战备工业化坚硬表面科幻外观 |
| 构图 | 极低角度（蠕虫眼睛视角）仰视、主体走向镜头占画面主导、城市上空远景背景 |
| 光 | 电影关键艺术光效（远景城市+机甲高光） |

## 六元素验收（对齐 picgirly2k 方式：独立模板以风格意图为准，不以 sunny 区间）
| 元素 | 说明 | 实测（测试主题：FAFO工作室）|
|---|---|---|
| 饱和度 | 记录数值，按风格意图判断（黑灰金机械配色预期中低饱和）| **20.9% ✅**（黑灰金中低饱和符合意图） |
| R-B | 记录数值，按风格意图判断（黑灰冷+金色点缀暖）| **+14.9 ✅**（金色点缀微暖合理） |
| 明度 | 记录数值，按风格意图判断（电影关键艺术可能中低明度）| **42.6% ✅**（电影感中低明度合理） |
| 柔度 | 记录数值，按风格意图判断（CGI 机械锐利边缘正常）| **0.168 ✅** |
| 边缘 >40 | 记录数值，按风格意图判断（机械 greeble 高边缘正常）| **15.43% ✅**（机械细节高边缘正常） |
| 高饱和像素 | 记录数值（S>=60% 占比），按风格意图判断 | **3.20% ✅**（黑灰金无荧光） |

**验收**：出图后跑 `python3 ~/.hermes/scripts/img_metrics.py <图>` 记录六项；**以风格意图判断**（CGI 机械：黑灰金配色+锐利机械边缘+电影感光影），不以 sunny 区间为准（同 picgirly2k）；文字另用 VL 逐字复核。

## 模板结构（主题派生式，3:4）

<主题>，a gigantic bipedal mecha robot walking directly toward the camera, viewed from an extremely low worm's-eye angle, emphasizing its towering scale above the distant city skyline. Photorealistic CGI rendering, highly detailed mechanical greeble surfaces, anime mecha-influenced design (Gundam/Armored Core aesthetics), cinematic key art quality, 8k, ultra-detailed. Color scheme: predominantly black and gunmetal gray armor with deep black joints, under-chassis and recessed mechanical parts, glossy gold armor plates on the shoulders, chest core, head crest, forearm vents and lower legs/feet. Head/upper torso: angled humanoid head with a sharp, blade-like gold crest/fin sweeping up and back like horns; narrow visor-style "eyes"; thick armored neck collar merging into wide, boxy shoulders with red panel inserts and mechanical vents. Arms: right arm raised and bent close to the torso, gripping a heavy articulated fist, gold forearm armor plates, exposed black joint mechanisms at the elbow. Left arm lowered, holding a massive futuristic rifle/cannon hanging toward the hip, muzzle pointed at the ground; the weapon is a rectangular industrial weapon with vents and scope/sight modules. Torso: broad layered chest armor with a gold center core panel flanked by black armor plates with white seams, cables and mechanical detailing; the midsection narrows into an armored waist/hip unit with gold hip guards. Legs/feet: thick, heavy load-bearing legs with white and black paneling and gold knees and ankles; broad mechanical feet with gold-plated toes/heel, kicking up clouds of dust and debris as it walks, mid-stride pose suggesting forward motion and immense weight. Surface detail: dense greebles throughout—hydraulic pistons, vents, exposed joint mechanisms, panel seams, rivets and layered armor plates—giving it an industrial, battle-ready, "hard surface" sci-fi look. 画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、现代波普艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面最底部中央区域以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，完整清晰不被遮挡，排版精致克制，不影响主体视觉。右上角用粗体简体中文标注：FAFO工作室。除上述文字外不要生成任何其他英文文字或标语。

### 派生规则
- **必须主题派生**：**机甲（配色微调/武器/细节）与场景（城市远景/战场/环境）随主题派生**、主标题内容
- **必须固定**：巨大两足机甲走向镜头+蠕虫视角+城市上空规模、CGI 渲染+机械 greeble+高达/装甲核心美学+电影关键艺术+8K、黑灰金配色、头/臂/躯干/腿脚细节描述、文字三件套
- **禁止**：2D 平涂、卡通简化、低多边形、无机械细节、多余英文标语

## 出图（默认工具）
**默认生图工具 = 全能图片 G_image2.5 sunburst**（app `2098218128315609089`，~0.036 元/张，输出约 880×1184≈3:4）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- 仅用户要求高清大图时才走 Z-image 模板（`2055930575931887617`，2160×2896）

## 经验
- **2026-10-26 创建**：picgirly2k 机械向主题派生版（巨大两足机甲·CGI 机械设计）；验收方式继承 picgirly2k（独立模板以风格意图为准，不以 sunny 区间）；提示词为英文原模板（用户提供）
- **2026-10-26 实测「FAFO工作室」v1 达标**：S20.9/高饱和像素3.2%/R-B+14.9/明度42.6/柔度0.168/边缘15.43——黑灰金机械配色中低饱和+金色微暖+电影中低明度+机械 greeble 高边缘，全部符合 CGI 机甲风格意图，一次达标
- **提示词语言**：主体机械设计描述保留英文原文（CGI 机械风格英文更稳），仅标题/署名/FAFO 用中文
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picsunny2 + picbpsunny2 + picgirlsunny2 + picsunny3 + picbpsunny3 + picgirlsunny3 + piccitypop + picsearoad + picdacnegirl + picsinggirl + pictonghua + picrussiagirlsolider + pichybf + picdjgirl + picdiscoboy + picrainnight + pichkdlj + pictry + picfacebustketball + picupfoodout + picwhj + picskyfo + picbpskyfo + picgirlskyfo + picghost5 + picbpghost5 + picbot + picreal + picreal2 + picreal3；触发时按模板区分
