---
name: picghost5
description: Use when 要复古编辑摄影幽魅海报提示词（给主题，柔和自然光+暗调情感阴影+花卉静物+低饱和暖调，3:4）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 幽魅, 复古编辑摄影, 柔和自然光, 暗调, 花卉静物, 低饱和暖调, 3:4, image2.5]
---

# picghost5 — 复古编辑摄影幽魅海报提示词（主题派生式，3:4）

2026-10-24 创建：反向推理自 RunningHub 模型 **lilia**（LoRA / Z-image-base / `Liliia_c1-st6000.safetensors`）的风格定义——**浪漫复古编辑摄影 + 绘画般电影构图 + 柔和自然光 + 暗调情感阴影 + 花卉静物氛围 + 低饱和暖色调 + 写实质感 + 梦幻情绪**。用户指定 3:4 比例重画，主题「倩女幽魂」。

## 触发
- 用户给主题并要求「复古编辑摄影」「浪漫复古」「柔和自然光」「暗调情绪」「花卉静物」「低饱和暖调」「lilia 风」幽魅版
- 用户要求「按 picghost5 出图」
- 注意：输出**只要提示词内容**；人物/场景按主题派生；画风三段完全保留；**固定 3:4**

## 画风定义（lilia 风格，勿改）
| 要素 | 内容 |
|---|---|
| 摄影语言 | 浪漫复古编辑摄影（romantic vintage editorial photography）|
| 构图 | 绘画般的电影构图（painterly cinematic composition）|
| 光 | 柔和自然光（soft natural light），单侧窗光斜射 |
| 影 | 暗调情感阴影（dark moody shadows），明暗过渡细腻 |
| 环境 | 花卉静物氛围（floral still life atmosphere）——干花、花瓶、植物标本 |
| 色调 | 低饱和暖色调（muted warm color grading）：米白/浅灰/棕褐/暖赭 |
| 质感 | 写实材质纹理 + 轻微胶片颗粒 + 绘画与摄影之间的质感 |
| 情绪 | 梦幻而富有情绪（dreamy emotional mood）——宁静、专注、诗意、怀旧 |

## 模板结构（主题派生式，3:4 固定）

<主题>（可附：主题相关画面内容提示），浪漫复古编辑摄影风格，绘画般的电影构图，1个<由主题派生的女性主体>，<由主题派生的服装与姿态>，<由主题派生的场景与静物摆设>，柔和自然光从侧窗斜射进来，暗调情感阴影，明暗过渡细腻，花卉静物氛围——<由主题派生的干花/花瓶/枝叶/陶器>，低饱和暖色调调色，米白浅灰棕褐暖赭为主色，真实皮肤与布料质感，轻微胶片颗粒，绘画与摄影之间的质感，梦幻而富有情绪，3:4 竖版构图，光圈柔和浅景深，画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、复古编辑风艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。右上角用粗体简体中文标注：FAFO工作室

### 派生规则
- **主体**：1 个女性，外貌/服装/姿态按主题派生（如「倩女幽魂」→ 墨黑长发白纱长衣、低首抚花；「老范要结婚了」→ 红色嫁衣持花）
- **场景与静物**：由主题派生的室内空间 + 干花/花瓶/画稿/陶器/织物等静物
- **画风固定保留**：浪漫复古编辑摄影/绘画电影构图/柔和侧窗自然光/暗调情感阴影/花卉静物氛围/低饱和暖调/真实质感/胶片颗粒/梦幻情绪（这串永远不动）
- **比例固定**：3:4 竖版（1086×1448 或 1152×1536）
- **构图固定**：人物为主体 + 静物环绕 + 左上超大主标题

## 量化特征（lilia 实测基准，2026-10-24）
| 维度 | 实测值（2160×3840 版）|
|---|---|
| 饱和度 | 23.6%（低饱和）|
| 高饱和像素 S≥60% | 5.7% |
| 锐度 Laplacian | 186.7（柔）|
| 边缘>40 | 1.1%（极干净）|
| 明度 | 灰度 37%、V 39% |
| 对比 std | 57.4、动态范围 201 |
| 柔度指数 | 0.031（很柔）|
| 色温 R-B | **+16.5（微暖）** |
**验收区间**：饱和 18-30%、柔度 <0.06、R-B +8~+25、边缘>40 <3%、明度 30-45%

## 与 ghost 家族的区别
| 技能 | 画风 |
|---|---|
| picbpghost / picbpghost2 | 国风奇幻低饱和+灯笼暖光 / 青橙冷调 |
| **picghost5（本技能）** | **复古编辑摄影 + 柔和自然光 + 花卉静物 + 低饱和暖调（lilia 风）** |

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用）。

## 交付规则（2026-10-12 用户定，pic 全部适用）
- 生成的图片**直接发当前频道**（MEDIA: 路径），不再只发邮箱
- 图片**先不清理**、保留在服务器（用户 2026-10-14 更新：暂不删，后续可能复查/复用）
- 长提示词/中间产物落 /tmp 的可清理，图片文件保留

## 出图（完整流程最后一步）
**默认生图工具 = 全能图片 G_image2.5 sunburst**（app `2098218128315609089`，~0.036 元/张，输出约 880×1184≈3:4）
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
备选（仅需 2160×2896 高清大图时）：Z-image 模板 webappId `2055930575931887617`（字段 7.height=1448 / 7.width=1086 / 7.batch_size=1 / 21.text）
```bash
- image2.5 sunburst（2098218128315609089）也支持，输出约 880×1184（3:4），~0.036 元/张
- 长中文提示词写入文件再 $(cat) 传入，避免 shell 转义

## 经验
- **2026-10-24 创建**：反向推理自 lilia LoRA 风格定义；Z-image base + 风格提示词一次命中（低饱和暖调/柔和侧窗光/干花静物/复古编辑摄影质感全到位）
- **lilia 风格三要素**：①柔和单侧窗自然光 + 暗调情感阴影（明暗过渡细腻）②低饱和暖调（米白浅灰棕褐暖赭，S≈24%、R-B≈+16）③花卉静物氛围（干花/花瓶/枝叶/陶器）+ 轻微胶片颗粒
- **3:4 出图**：默认 image2.5 sunburst 输出 880×1184≈3:4；需高清走 Z-image 模板 width=1086/height=1448
- **写实人物安全**：避开「紧身/身材线条」措辞防 image2.5 安全审查 1501 拦截
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picsunny2 + picbpsunny2 + picgirlsunny2 + picskyfo + picbpskyfo + picgirlskyfo + picghost5 + picreal + picreal2 + picreal3；触发时按模板区分
