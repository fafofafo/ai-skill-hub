---
name: picbpghost5
description: Use when 要复古编辑摄影幽魅海报提示词（给主题，picbpnew 骨架 + 柔和自然光+暗调情感阴影+花卉静物+低饱和暖调，3:4）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 幽魅, 复古编辑摄影, 柔和自然光, 花卉静物, 低饱和暖调, picbpnew骨架, 3:4]
    related_skills: [picghost5, picbpnew, pic-poster-family]
---

# picbpghost5 — 复古编辑摄影幽魅海报（picbpnew 骨架版）

2026-10-24 创建：`picghost5` 的 **picbpnew 骨架版**（场景向），画风全盘继承 `picghost5`（反向推理自 RunningHub **lilia** LoRA：浪漫复古编辑摄影 / 绘画电影构图 / 柔和自然光 / 暗调情感阴影 / 花卉静物氛围 / 低饱和暖调 / 真实质感 / 梦幻情绪），排版换成 `picbpnew` 四要素骨架。

## 触发
- 用户要求「picbpghost5」「picbpnew 骨架的复古编辑摄影幽魅海报」
- 主题要「复古编辑摄影 / 柔和自然光 / 暗调情绪 / 花卉静物 / 低饱和暖调 / lilia 风」且需骨架排版（左上大标题 + 底部署名 + 右上 FAFO）
- 与 `picghost5` 区别：`picghost5` 是纯画面提示词（无底部署名、无 1086×1448 全串），本技能是完整骨架版

## 骨架标准（picbpX 四要素，缺一不合格）
1. **主题嵌入开头**：「请生成一张以「<主题>」为主题的…」
2. **左上角超大主标题**（bold 立体挤压感艺术字 + 利落描边 + 清晰投影 + 第一视觉焦点 + 不能写错字）
3. **底部或角落小号署名**「AIXZD ZHAPU PROJECT SERIES」
4. **末尾标注**：右上角粗体字标注：FAFO工作室

**第五要求（内容层）**：主题必须驱动画面实体——主体身份/服装/姿态/场景空间/静物摆设/环境氛围全由主题派生；**只有画风三段（画质/色调/风格）+ 3:4 尺寸固定不变**。

## 画风定义（lilia 系，勿改）
| 要素 | 内容 |
|---|---|
| 摄影语言 | 浪漫复古编辑摄影（romantic vintage editorial photography）|
| 构图 | 绘画般的电影构图（painterly cinematic composition）|
| 光 | 柔和自然光（soft natural light），单侧窗光斜射 |
| 影 | 暗调情感阴影（dark moody shadows），明暗过渡细腻 |
| 环境 | 花卉静物氛围（floral still life atmosphere）——干花/花瓶/植物标本 |
| 色调 | 低饱和暖调（muted warm color grading）：米白/浅灰/棕褐/暖赭 |
| 质感 | 写实材质纹理 + 轻微胶片颗粒 + 绘画与摄影之间 |
| 情绪 | 梦幻而富有情绪（dreamy emotional mood）——宁静/专注/诗意/怀旧 |

## 模板结构（中文，3:4 骨架）

请生成一张以「<主题>」为主题的复古编辑摄影风格情绪海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体采用浪漫复古编辑摄影风格（romantic vintage editorial photography），绘画般的电影构图，写实摄影质感而非插画或3D渲染。画面主体为 1 个<由主题派生的女性人物：身份/年龄/气质/发型/服色/姿态/神情>，<由主题派生的动作或与静物的互动>，置身于<由主题派生的室内空间与年代氛围>。周围环绕<由主题派生的静物摆设：花卉/花瓶/织物/器物/书卷/工作道具>，形成浓郁的花卉静物氛围（floral still life atmosphere）。光线为柔和自然光从侧窗斜射进来，落在人物的侧脸与手部，形成暗调情感阴影（dark moody shadows），明暗过渡细腻柔和，无硬光无闪光。整体色调为低饱和暖色调（muted warm color grading），以米白、浅灰、棕褐、暖赭为主色，色彩克制不艳丽。材质真实：皮肤的细腻纹理、布料的褶皱与光泽、木质与陶瓷的肌理清晰可辨；画面带轻微胶片颗粒与绘画/摄影之间的质感，梦幻而富有情绪。整体构图留白克制，人物为第一视觉中心，静物为其情绪延伸。画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、复古编辑风艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。右上角用粗体简体中文标注：FAFO工作室

### 派生示例（主题 → 画面）
| 主题 | 主体 | 场景/静物 |
|---|---|---|
| 倩女幽魂 | 墨黑长直发古典女子、素白纱衣、低首抚白兰花、神情怅然 | 古旧木窗/深色木案/青瓷花瓶/白瓷茶盏/旧书卷 |
| 老范要结婚了 | 短发新娘、正红嫁衣、手持红玫瑰束、甜笑 | 老洋房客厅/红绸/喜字贴/蕾丝桌布/银器 |
| 夜上海 | 墨黑波浪卷、正红旗袍、侧身倚窗回眸 | 石库门洋房/留声机/琉璃灯/白玫瑰瓶 |
| 红颜白发 | 雪白长发女子、浅灰长裙、垂眸持枯枝 | 旧书房/木质书架/铜镜/干枯花枝 |

## 量化特征（lilia 基准 + picghost5 实测，2026-10-24）
| 维度 | 基准值 |
|---|---|
| 饱和度 | 18-30%（实测 23.6% / 27.4%）|
| 高饱和像素 S≥60% | <8% |
| 锐度 Laplacian | 186-320（柔）|
| 边缘>40 | <3%（1.1% / 2.21%）|
| 明度 | 灰度 30-45%、V 35-45% |
| 柔度指数 | <0.06（0.031 / 0.045 很柔）|
| 色温 R-B | +8~+25（+16.5 / +15.7 微暖）|
**验收**：以上 7 项全落区间 → 画风成立；文字另需 VL 逐字复核。

## 与家族其他成员的区别
| 技能 | 骨架 | 画风 |
|---|---|---|
| picbpghost / picbpghost2 | picbpnew | 国风奇幻低饱和+灯笼暖光 / 青橙冷调 |
| picghost5 | 无骨架（纯画面） | 复古编辑摄影 + 花卉静物 + 低饱和暖调 |
| **picbpghost5（本技能）** | **picbpnew 骨架** | **同上 lilia 复古编辑摄影** |

## 固定标注
每次生成提示词，末尾必须带：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用）。

## 交付规则（2026-10-12 用户定）
- 生成的图片**直接发当前频道**（MEDIA: 路径）
- 图片**保留在服务器**不清理；中间产物落 /tmp 可清

## 出图
- **默认生图工具 = 全能图片 G_image2.5 sunburst**（app `2098218128315609089`，~0.036 元/张，输出约 880×1184≈3:4）：`python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out xxx.png`
- 备选（仅当需要 2160×2896 高清大图）：Z-image 模板 `2055930575931887617`（字段 7.height=1448 / 7.width=1086 / 7.batch_size=1 / 21.text）
- 长中文提示词写文件再 `$(cat)` 传入，避免 shell 转义

## 实测记录（2026-10-24，主题「倩女幽魂」）
| 指标 | 验收区间 | 实测 | 判定 |
|---|---|---|---|
| 饱和度 | 18-30% | 28.8% | ✅ |
| 高饱和像素 S≥60% | <8% | 13.94% | ⚠️ 超 |
| 锐度 Laplacian | 186-320 | 372.8 | ⚠️ 略高 |
| 边缘>40 | <3% | 2.46% | ✅ |
| 明度 | 30-45% | 47.7% | ⚠️ 略高 |
| 柔度 | <0.06 | 0.041 | ✅ |
| 色温 R-B | +8~+25 | +22.3 | ✅ |
输出 2160×2896（≈3:4），9 币/41s。VL 复核：白衣古风女子侧坐木案抚白兰、青瓷花瓶茶盏书卷、柔侧光暖棕米白幽梦感；**左上「倩女幽魂」/ 底部「AIXZD ZHAPU PROJECT SERIES」/ 右上「FAFO工作室」全部逐字正确，零错字零乱码**。

**骨架版系统性偏差（vs picghost5 纯画面版）**：主标题艺术字 + 系列署名带来额外高对比边缘与亮色块 → 锐度（320→373）、高饱和像素（5→13.9%）、明度（36.8→47.7%）整体上浮。属排版元素导致的可解释偏差，非画风失守；要求严格落区间时可在提示词加「整体压暗一档、降低文字周围高饱和」或后期调。

## 经验
- **2026-10-24 创建**：由 picghost5 转骨架版；画风三段与 3:4 尺寸固定，主体/场景/静物全主题派生
- **lilia 风格三要素**：①柔和单侧窗自然光 + 暗调情感阴影 ②低饱和暖调（S≈24%、R-B≈+16）③花卉静物氛围 + 轻微胶片颗粒
- **写实人物安全**：避开「紧身/身材线条」措辞防 image2.5 1501 拦截
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picsunny2 + picbpsunny2 + picgirlsunny2 + picskyfo + picbpskyfo + picgirlskyfo + picghost5 + picbpghost5 + picreal + picreal2 + picreal3；触发时按模板区分
