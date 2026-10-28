---
name: pic1960pp
description: Use when 要求输出 1960s 欧洲艺术电影海报提示词（给主题/歌名/人物）。含英文模板与出图流程。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [海报, 1960s, 电影海报, 拼贴, 英文, image2.5]
    related_skills: [picpp, picbpnew, pic-poster-family]
---

# pic1960pp — 1960s 欧洲艺术电影海报提示词

把任意主题（人物/歌名/电影概念）改写为「1960s 欧洲艺术电影海报」提示词（image2.5 英文模板风格，竖版）。2026-10-15 用户基于 picpp 开发：技能框架照搬 picpp（触发/模板/固定标注/交付/出图/经验），提示词用 1960s 手工拼贴电影海报英文模板。

## 触发
- 用户给主题并要求「1960s」「欧洲电影海报」「艺术电影」「手工拼贴」风格
- 用户发来英文长模板 + 主题/参考图描述，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；原模板为英文，保留英文结构与全部约束（纸张/拼贴元素/文字/配色/质感）

## 模板结构（英文，保留原句法，主题由用户给出）

Create a vertical poster composition on aged cream paper with a handmade analog feel. Use rough ripped paper edges, layered magazine cutouts, photocopy grain, halftone texture, ink bleed, and slightly imperfect screen-print registration. Keep the subject as the main black-and-white photographic portrait, placed prominently in the center or upper center. Surround the subject with graphic blocks of deep red, cobalt blue, warm yellow, black, and ivory.
Add supporting collage fragments such as <主题相关意象>: a rainy European street, film-strip borders, newspaper clippings, urban silhouettes, and cinematic details, arranged like a handmade 1960s art-house movie poster. Use bold condensed typography with a strong visual hierarchy. Add large headline text: "<主题标题>". Add smaller subtitle text: "<副标题>". Add bottom text: "<底部文字>". If needed, include a small top line reading "<TAGLINE>".
The final result should feel cinematic, intellectual, rebellious, and editorial — like a lost 1960s European film poster with a strong point of view. Keep it raw, tactile, printed, imperfect, and handmade. Avoid a glossy modern finish.

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用）。

## 出图前固定追加句（2026-10-15 用户定，picpp/pic1960pp 英文模板适用）
**重新生成提示词之后、发给 RunningHub 之前，在提示词最后补一句：`输出的英文全部翻译成中文`**（英文模板的标题/编辑信息等输出文字转为中文；模板结构/约束本身保持英文不变）

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
- 长提示词写入文件再 $(cat) 传入，避免 shell 转义；t2i 前把 markdown 符号清理为纯文本更稳

## 经验
- 1960s 海报精髓：陈年米白纸底 + 手工拼贴（杂志剪贴/复印颗粒/半调/油墨渗透/套印错位）+ 黑白人像主体居中 + 深红/钴蓝/暖黄/黑/象牙色块环绕
- 支持元素：雨夜欧洲街道/胶片边条/报纸剪报/城市剪影/电影细节——主题相关化
- 主题=歌名/人物时：主视觉黑白人像、标题用歌名/人名、副标题与底部文字按主题意境拟
- 质感关键词固定：raw, tactile, printed, imperfect, handmade, avoid glossy modern finish
- pic 技能族：pic1-7 + picbp + picbpnew + picpp（旅行报纸）+ pic1960pp（1960s电影海报）；触发时按模板区分
