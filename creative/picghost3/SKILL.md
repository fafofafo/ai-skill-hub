---
name: picghost3
description: Use when 要风格化数字插画海报提示词（给主题，Loish画风+蓝金古装女子+玻璃压手+青绿背景+流行超现实，3:4）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 数字插画, Loish, 超现实主义, 蓝金古装, 玻璃压手, 青绿背景, image2.5]
    related_skills: [picbpnew, pic-poster-family]
---

# picghost3 — 风格化数字插画海报（Loish 画风 · 玻璃压手超现实）

2026-10-25 创建：用户给定完整提示词。**流行超现实主义数字插画**：中国女子蓝金传统服饰、单眼眨眼嘟嘴俏皮、双手按压透明玻璃面（指纹与手掌挤压变形）、鲜亮青绿背景、Loish 画风、ArtStation 热门风格。

## 触发
- 用户要求「picghost3」「Loish 画风」「玻璃压手」「蓝金古装女子」「流行超现实主义插画」
- 注意：输出**只要提示词内容**；画风要素固定，人物外貌/表情可随主题微调

## 画风定义（固定，勿改）
| 要素 | 内容 |
|---|---|
| 风格 | 风格化数字插画，流行超现实主义艺术风格，Loish 画风，ArtStation 热门风格 |
| 主体 | 1 位容貌秀美的中国女子，典雅蓝金配色传统服饰 |
| 表情 | 俏皮单眼眨眼、嘟起嘴唇 |
| 手部 | 双手按压竖直透明玻璃面（玻璃本体不可见），指纹与手掌因挤压压扁变形；双手轻盈抬至脸庞附近，姿态灵动俏皮 |
| 背景 | 鲜亮纯粹的青绿色背景 |
| 质感 | 肌肤质感顺滑，柔和电影感光影，五官刻画精致 |

## 模板结构（主题派生式，3:4）

<主题>，风格化数字插画，流行超现实主义艺术风格，Loish画风，ArtStation热门风格。一位容貌秀美的中国女子，身着典雅蓝金配色传统服饰，<由主题派生的微调：发型/头饰/表情细节>，俏皮地单眼眨眼、嘟起嘴唇。她将双手按压在一块竖直玻璃面上，双手平贴身前透明玻璃，指纹与手掌因挤压而被压扁变形；玻璃本体不可见。双手轻盈抬至脸庞附近，姿态灵动俏皮。鲜亮纯粹的青绿色背景。肌肤质感顺滑，柔和电影感光影，五官刻画精致。3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、现代波普艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面最底部中央区域以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，完整清晰不被遮挡，排版精致克制。右上角用粗体简体中文标注：FAFO工作室。除上述文字外不要生成任何其他英文文字或标语。

### 派生规则
- **必须主题派生**：主题嵌入开头、人物发型/头饰/表情细节、主标题内容
- **必须固定**：蓝金传统服饰、单眼眨眼嘟嘴、双手压玻璃（指纹手掌变形）、青绿背景、Loish 画风、肌肤顺滑、电影感光影、3:4、文字三件套
- **禁止**：照片写实、2D 平涂、阴郁暗调、多余英文标语

## 与 ghost 家族的区别
| 技能 | 画风 |
|---|---|
| picbpghost / picbpghost2 | 国风奇幻低饱和+灯笼暖光 / 青橙冷调 |
| picghost5 / picbpghost5 | 复古编辑摄影 + 花卉静物 + 低饱和暖调 |
| **picghost3（本技能）** | **Loish 数字插画 + 蓝金古装 + 玻璃压手超现实 + 青绿背景** |

## 出图（默认工具）
**默认生图工具 = 全能图片 G_image2.5 sunburst**（app `2098218128315609089`，~0.036 元/张，输出约 880×1184≈3:4）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- 仅用户要求高清大图时才走 Z-image 模板（`2055930575931887617`，2160×2896）

## 经验
- **2026-10-25 创建**：用户给定完整 Loish 画风提示词；玻璃压手（指纹手掌压扁变形）是本技能视觉锤，写提示词时必须保留「玻璃本体不可见」
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picsunny2 + picbpsunny2 + picgirlsunny2 + picsunny3 + picbpsunny3 + picgirlsunny3 + picskyfo + picbpskyfo + picgirlskyfo + picghost3 + picghost5 + picbpghost5 + picreal + picreal2 + picreal3；触发时按模板区分
