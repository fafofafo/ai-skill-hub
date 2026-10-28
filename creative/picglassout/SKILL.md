---
name: picglassout
description: Use when 要数字插画海报提示词（给主题，picbpnew 骨架 + Loish画风+蓝金古装女子+中式古典室外场景+昭和美女式姿势，3:4）。含模板与出图流程。
version: 1.1.0
metadata:
  hermes:
    tags: [海报, 数字插画, Loish, 超现实主义, 蓝金古装, 青绿背景, picbpnew骨架, image2.5]
    related_skills: [picghost3, picbpnew, pic-poster-family]
---

# picglassout — 风格化数字插画海报（picbpnew 骨架版 · Loish 蓝金古装 · 中式古典室外）

2026-10-25 创建：`picglassin` 的**室外版**——背景改为符合人物穿着身份的中式古典室外场景（园林/庭院/亭台/廊下），画风其余继承 picglassin（Loish 数字插画 / 蓝金古装女子 / piczhgirlin 式姿势）。

## 触发
- 用户要求「picglassin」「picbpnew 骨架的 Loish 插画海报」
- 主题要「Loish 画风 / 蓝金古装 / 流行超现实」且需骨架排版
- 与 `picghost3` 区别：`picghost3` 是纯画面提示词（自由句法），本技能是完整骨架版（统一「请生成一张以…为主题」开头 + 尺寸串）

## 骨架标准（picbpX 四要素，缺一不合格）
1. **主题嵌入开头**：「请生成一张以「<主题>」为主题的…」
2. **左上角超大主标题**（bold 立体挤压感艺术字 + 利落描边 + 清晰投影 + 第一视觉焦点 + 不能写错字）
3. **底部或角落小号署名**「AIXZD ZHAPU PROJECT SERIES」（放最底部中央深色平整区域，不被遮挡）
4. **末尾标注**：右上角粗体字标注：FAFO工作室

**第五要求（内容层）**：主题必须驱动人物细节——发型/头饰/表情细节随主题派生；**画风要素固定**（蓝金传统服饰 / 单眼眨眼嘟嘴 / 双手压玻璃 / 青绿背景 / Loish 画风）。

## 画风定义（继承 picghost3，勿改）
| 要素 | 内容 |
|---|---|
| 风格 | 风格化数字插画，流行超现实主义艺术风格，Loish 画风，ArtStation 热门风格 |
| 主体 | 1 位容貌秀美的中国女子，典雅蓝金配色传统服饰 |
| 表情 | 俏皮单眼眨眼、嘟起嘴唇 |
| 姿势 | **参考 piczhgirlin/picgirlinsidefree**（2026-10-25 用户定）：紧凑半身肖像，一只手抬起轻扶墨镜边缘/脸侧，另一只手<由主题派生的手持物>，姿态灵动俏皮 |
| 背景 | 鲜亮纯粹的青绿色背景 |
| 质感 | 肌肤质感顺滑，柔和电影感光影，五官刻画精致 |

## 模板结构（中文，3:4 骨架）

请生成一张以「<主题>」为主题的风格化数字插画海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体为风格化数字插画，流行超现实主义艺术风格，Loish画风，ArtStation热门风格，不是照片不是真人摄影、不是 2D 平涂。画面主体为 1 位容貌秀美的中国女子，身着典雅蓝金配色传统服饰，<由主题派生的发型/头饰/表情细节>，俏皮地单眼眨眼、嘟起嘴唇。姿势参考昭和室内数字插画美女（piczhgirlin 系）：紧凑半身肖像，一只手抬起轻扶墨镜边缘或轻托脸侧，另一只手<由主题派生的手持物：玫瑰花束/情书/奶茶/画板等>，姿态灵动俏皮。背景为中式古典室外场景：园林/庭院/亭台/廊下/湖畔等古典空间，假山/回廊/荷塘/垂柳/灯笼/石栏/花木等中式景物，明净通透、光线充足；<与主题相关的道具与装饰细节由主题派生：花灯/纸鸢/茶席/喜字/花束等>；背景轻度虚化但保留场景元素边缘清晰可见。肌肤质感顺滑，柔和电影感光影，五官刻画精致。画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、现代波普艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面最底部中央区域以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，完整清晰不被遮挡，排版精致克制。右上角用粗体简体中文标注：FAFO工作室。除上述文字外不要生成任何其他英文文字或标语。

### 派生规则
- **必须主题派生**：主题嵌入开头、人物发型/头饰/表情细节、**中式古典室外场景（固定类型）+ 与主题相关的道具细节**、主标题内容
- **必须固定**：蓝金传统服饰、单眼眨眼嘟嘴、piczhgirlin 式半身姿势（一手扶墨镜/脸侧+一手持物）、青绿背景、Loish 画风、肌肤顺滑、电影感光影、3:4 1086×1448、文字三件套
- **禁止**：照片写实、2D 平涂、阴郁暗调、多余英文标语

## 与 ghost 家族的区别
| 技能 | 骨架 | 画风 |
|---|---|---|
| picghost3 | 无骨架（自由句法）| Loish 数字插画 + 蓝金古装 + 玻璃压手（原始画风保留）|
| picghost5 / picbpghost5 | 无骨架 / 骨架 | 复古编辑摄影 + 花卉静物 |
| **picglassout（本技能）** | **picbpnew 骨架** | **Loish 数字插画 + 蓝金古装 + 中式古典室外 + piczhgirlin 式姿势** |

## 出图（默认工具）
**默认生图工具 = 全能图片 G_image2.5 sunburst**（app `2098218128315609089`，~0.036 元/张，输出约 880×1184≈3:4）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- 仅用户要求高清大图时才走 Z-image 模板（`2055930575931887617`，2160×2896）

## 实测记录（2026-10-25，主题「笑纳」）
| 元素 | 实测 | 说明 |
|---|---|---|
| 饱和度 | 35.9% | Loish 青绿背景中等饱和 |
| R-B | +17.4 | 青绿背景偏冷中微暖（蓝金服饰）|
| 明度 | 45.5% | 中调 |
| 柔度 | 0.137 | 偏柔（Loish 顺滑质感）|
| 边缘 >40 | 11.75% | 中等细节 |
输出 880×1184（3:4）。**用户确认效果可以，覆盖原玻璃压手版正式生效**（v1.1.0 姿势=piczhgirlin 式：一手扶墨镜/脸侧 + 一手持物）。

## 实测记录 v1.2.0（2026-10-25，主题「笑纳」，中式古典室内背景）
| 元素 | 实测 | 说明 |
|---|---|---|
| 饱和度 | 31.2% | 中式室内器物中饱和 |
| R-B | +30.7 | 暖调（木质/烛台/蓝金服饰）|
| 明度 | 45.0% | 中调 |
| 柔度 | 0.142 | 偏柔 |
| 边缘 >40 | 13.15% | 室内器物细节增多 |
输出 880×1184（3:4）。**用户确认效果可接受，覆盖正式生效**（v1.2.0 背景=中式古典室内）。

## 经验
- **2026-10-25 v1.1.0**：用户要求主体人物姿势参考 piczhgirlin/picgirlinsidefree——玻璃压手姿势替换为昭和美女式半身姿势（一手扶墨镜/脸侧 + 一手持物），画风与蓝金古装保留
- **2026-10-25 v1.0.0（picglassout）**：picglassin 的室外版——背景改为中式古典室外场景（园林/庭院/亭台/廊下/湖畔：假山/回廊/荷塘/垂柳/灯笼/石栏）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picsunny2 + picbpsunny2 + picgirlsunny2 + picsunny3 + picbpsunny3 + picgirlsunny3 + picskyfo + picbpskyfo + picgirlskyfo + picghost3 + picglassin + picglassout + picghost5 + picbpghost5 + picreal + picreal2 + picreal3；触发时按模板区分
