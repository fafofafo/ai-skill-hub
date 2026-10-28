---
name: pic5
description: Use when 要求输出 paper-craft diorama 纸艺立体模型提示词。含英文模板与出图流程。
version: 1.0.0
metadata:
  license: MIT
---

# pic5 — paper-craft diorama 纸艺立体模型提示词

把任意主题（歌名/概念/城市）改写为「纸艺立体模型」提示词（image2.5 英文模板风格）。2026-10-11 由用户验证：主题「睫毛上的心跳」→ 纸艺眼眸+心跳波形流程可用。

## 触发
- 用户给主题并要求「paper-craft」「diorama」「纸艺立体模型/手工立体」风格
- 用户发来英文模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；原模板为英文，保留英文结构，主题文字可中英混排

## 模板结构（英文，保留原句法）

Create a highly detailed miniature "<主题英译>" paper-craft diorama emerging from a torn opening in a rustic wooden crafting table. Feature <主题核心意象清单>，blended with <补充意象>。Add a textured <光带/水流意象>，tiny <小元素>，bridges <桥意象>，and lush <花/植物意象>。Surround the scene with realistic crafting tools, paper supplies, glue, scissors, and decorative tape. Add elegant text reading 「<中文主题>」, 「<英文主题>」, and 「<英文标语>」. Use warm natural window light, realistic shadows, intricate layered paper textures, handcrafted details, and a cozy premium miniature-art aesthetic, photographed from a slightly elevated close-up perspective.

## 出图（完整流程最后一步）
提示词生成后直接调默认文生图工具出图（RunningHub，见 runhub-image-gen 技能）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 3:4）
- 长提示词写入文件再 $(cat) 传入，避免 shell 转义；t2i 前把 markdown 符号清理为纯文本更稳
- 2026-10-11 实测：主题「睫毛上的心跳」→ 纸艺立体模型 → 生成成功

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic1-5 全部适用）。

## 经验
- 纸艺立体模型精髓：木桌破口+层叠纸纹理+暖窗光+手工工具（胶水/剪刀/装饰胶带）环绕，体现手作感与 premium 感
- 城市模板的 landmark/河流/船 → 换成主题意象（例：睫毛/心跳波形/羽毛/花瓣/光带河流/纸心/纸桥），保持 diorama 的「微型世界」气质
- 文字三件套保留：中文主题 + 英文主题 + 英文标语（例 EVERY BLINK IS A HEARTBEAT.）
- pic 技能族：pic1 通用（禁人物）/pic2 中轴夹景/pic3 字体穿透/pic4 国潮插画/pic5 纸艺立体模型；触发时按模板区分
