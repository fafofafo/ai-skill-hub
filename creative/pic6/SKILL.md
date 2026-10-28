---
name: pic6
description: Use when 要求输出旅行报纸拼贴海报提示词（给主题/歌名/城市）。含英文模板与出图流程。
version: 1.0.0
metadata:
  license: MIT
---

# pic6 — 独立旅行报纸拼贴海报提示词

把任意主题（歌名/概念/城市）改写为「独立旅行报纸拼贴」海报提示词（image2.5 英文模板风格，2:3 竖版）。2026-10-11 由用户验证：主题「爱不释手」→ 珍爱时刻报纸拼贴流程可用。

## 触发
- 用户给主题并要求「旅行报纸」「newspaper collage」「独立报纸拼贴」风格
- 用户发来英文长模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；原模板为英文，保留英文结构与全部约束（6 类元素/文字系统/配色/质感）

## 模板结构（英文，保留原句法）

Make a vertical version of 2:3 independent travel newspaper collage poster with the theme of "<主题英译>，<副题>". Take "<TITLE>" as the main title of the only subject, and generate content according to the real moments of <主题关键词>: <核心意象清单>。Don't make a single photo, it should be like an independent travel newspaper made of real printed fragments. The whole canvas uses warm beige old newspaper bottom, with pulp fiber, creases, corner wear, slight stains, old ink penetration and uneven printing. Use modular editing collage: split into multiple photo sections of various sizes but clear order, bill fragments, postmarks, map parts, coordinates, color cards, thin lines, numbers and small description columns. There are slight misalignment, overlap, cropping and offset edges between the photo sections, like real paper being cut and retyped. Place a huge English title "<TITLE>" cut by the edge of the picture at the top or upper left, using thick vintage serifs or narrow newspaper fonts. Add short and accurate editing information around: "<档案词> FILE", "<副题> NOTES", "NO. 07", "<TITLE> · <副题>", "PEOPLE · PLACES · CULTURE · EVERYDAY LIFE". All text must be clear and spelled correctly, and fake Chinese or garbled codes should not be generated. PHOTO AND IMAGE CONTENT CONTAINS AT LEAST 6 CATEGORIES OF <主题> REAL ELEMENTS: <6类意象清单>。Add a simplified sketch map and a bill, ticket or postmark fragment. Each section serves the narrative of <主题> and avoids repeating the same angle. The whole use of old paper warm beige, charcoal black, faded brick red, dark indigo, gray green and a small amount of ochre yellow. The photos are mainly black and white, warm gray or low-saturation two-color, and a small number of sections retain the representative warm colors. Add half-tone dots, copy particles, screen printing texture, overprint offset, faded edges, paper folds and slight ink wear, but keep the subject and gesture of the photo recognisable. The composition should have a clear editing hierarchy: a giant title, 2-3 main photo sections, several auxiliary small sections, bills, maps, color cards and paper gaps.

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic1-5 全部适用，pic6 一并遵守）。

## 出图（完整流程最后一步）
提示词生成后直接调默认文生图工具出图（RunningHub，见 runhub-image-gen 技能）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 3:4）
- 长提示词写入文件再 $(cat) 传入，避免 shell 转义；t2i 前把 markdown 符号清理为纯文本更稳
- 2026-10-11 实测：主题「爱不释手」→ 旅行报纸拼贴 → 生成成功

## 经验
- 报纸拼贴精髓：暖米黄旧报纸底+多模块拼贴（照片/票据/邮票/地图/色卡/坐标）+错位重叠裁切，像真实纸被剪下重排；巨标题被画幅边缘裁切
- 城市模板的地标/街区/交通 → 换成主题意象（例：爱不释手→捧物双手/温柔姿态/暖光时刻/日常细节/自然瞬间），保持 6 类元素与城市叙事口吻
- 文字系统与配色（暖米黄/炭黑/砖红/靛蓝/灰绿/赭黄）为固定模板，不随主题变；照片以黑白/暖灰低饱和为主
- pic 技能族：pic1 通用（禁人物）/pic2 中轴夹景/pic3 字体穿透/pic4 国潮插画/pic5 纸艺立体/pic6 报纸拼贴；触发时按模板区分
