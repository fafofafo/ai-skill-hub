---
name: picgirl
description: Use when 要日系写实少女阳光风海报提示词（给主题，URI Dream Lab）。含模板与出图流程。
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [海报, 日系写实, 少女, 阳光, 逆光, 高饱和, image2.5]
    related_skills: [picbpnew, picsunny, picbp, pic-poster-family]
---

# picgirl — 日系写实美女阳光风海报提示词（URI DREAM LAB 视觉，主题派生式）

原 picsun，2026-10-20 用户重命名为 picgirl（对齐 picgirly2k 命名，picsuny2k→picgirly2k）。

2026-10-20 升级 v2.0.0：**画风保留原始 URI DREAM LAB 全套，人物/背景不再固定——每次按主题自动派生「一个美女主体 + 与主题相关的合适背景」**。主题自定义，画风永远参考原始提示词。

## 触发
- 用户给主题并要求「日系写实」「美女」「阳光」「URI Dream Lab」「逆光」「治愈」「高饱和」风格
- 用户发来主题/歌名，要求「按 picgirl 出图」——自动派生美女主体+相关背景
- 注意：输出**只要提示词内容**；人物外貌/服装/背景场景由主题派生；画风关键词全部保留

## 模板结构（升级版：主题派生式，画风固定）

<主题>（可附：主题相关画面内容提示），高饱和，高曝光，杰作，最佳质量，8K分辨率，真实3D渲染，素描线条，高对比色彩，浓墨重彩，超精细细节，日系写实风，URI DREAM LAB风格，1个<由主题派生的美女外貌：发型发色/五官气质/年龄感>，<由主题派生的服装与姿态>，<由主题派生的合适背景场景>，画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、现代艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点，仰视角度，面部特写，真实皮肤纹理，细腻毛孔，通透光影，阳光侧逆光，眼神明亮有高光，干净线稿，电影级构图，色彩明快，治愈氛围。

### 派生规则
- **主体**：1 个美女，外貌（发型/发色/气质）和服装按主题合理设计——主题是歌名/地名/概念时，用其氛围联想人设（如「富士山下」→和服少女+樱花；「海阔天空」→海边风衣女子）
- **背景**：与主题强相关的合适场景，一句话点明（地点/天气/元素），不脱离主题
- **标题（2026-10-20 新增，参考 picbpnew）**：左上角超大主标题=主题，bold 立体艺术字+描边+投影，第一视觉焦点，不能写错字
- **画风固定保留**：高饱和高曝光/真实3D渲染/日系写实/URI DREAM LAB/逆光通透/真实皮肤质感/明亮眼眸高光/电影级构图/治愈氛围（这串永远不动）
- **构图固定**：仰视角度 + 面部特写（保留原始视觉语言）

## 原始版模板（画风基准参考，v1.x 固定人设版）

<主题>，高饱和，高曝光，杰作，最佳质量，8K分辨率，真实3D渲染，素描线条，高对比色彩，浓墨重彩，超精细细节，日系写实风，URI DREAM LAB风格，1个少女，浅棕色微卷长发，发丝飞扬，戴着黄色飞行员头盔＋护目镜，橙色冲锋衣，仰视角度，面部特写，清澈蓝天＋白云背景，真实皮肤纹理，细腻毛孔，通透光影，阳光侧逆光，眼神明亮有高光，干净线稿，电影级构图，色彩明快，治愈氛围。

## 英文原版模板（备用，语义同中文版，实测效果一致）

<Theme> (optionally add theme-related scene description), high saturation, high exposure, masterpiece, best quality, 8K resolution, realistic 3D rendering, sketch lines, high contrast colors, vivid and rich colors, super fine details, Japanese realistic style, URI DREAM LAB style, 1 girl, light brown wavy long hair, hair flying, wearing yellow pilot helmet + goggles, orange parka, upward angle, close-up of face, clear blue sky + white clouds background, real skin texture, delicate pores, transparent lighting, sunside backlighting, bright eyes with highlights, clean line art, cinematic composition, bright colors, healing atmosphere.

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
- **2026-10-20 双版实测通过（v1.0.3）**：中文直译版 + 英文原版各出图 1 张，image2.5 sunburst 均完美还原——人设（浅棕卷发/黄头盔/橙夹克）、逆光通透、高饱和高曝光、蓝天白云全到位；FAFO 标注清晰无乱码；英文版模型自动加 FAFO/URI DREAM LAB 元素在头盔/夹克上。结论：**中英两版可互换，提示词通用，无需 MJ 原生接口**
- **2026-10-20 修正 v2**：提示词改为全中文直译版（高饱和/高曝光/杰作/最佳质量/8K/真实3D渲染/素描线条/高对比色彩/浓墨重彩/超精细细节/日系写实/URI DREAM LAB风格/1个少女/浅棕微卷长发发丝飞扬/黄飞行头盔+护目镜/橙冲锋衣/仰视面部特写/蓝天白云/真实皮肤纹理细腻毛孔/通透光影/阳光侧逆光/明亮眼眸高光/干净线稿/电影级构图/色彩明快/治愈氛围）
- **风格记忆点**：高饱和高曝光 + 真实3D渲染+素描线条 + 逆光通透 + 蓝天白云 + 治愈氛围 + 真实皮肤质感 + 黄飞行头盔护目镜+橙色冲锋衣（固定人设：浅棕微卷长发、发丝飞扬、仰视特写、明亮眼眸高光）
- **主题替换技巧**：主题=歌名/概念时嵌入开头并附一句画面内容，人设与画风关键词全部保留
- **安全提示（2026-10-19 实测）**：写实人物主题避开「紧身/身材线条」等描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl；触发时按模板区分
