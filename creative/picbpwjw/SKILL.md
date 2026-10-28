---
name: picbpwjw
description: Use when 要王家卫×杜可风电影感POV海报提示词（给主题/画面，折叠春园+不可能阶梯+广角畸变+晨光过曝+褪色胶片，picbpnew 骨架）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 电影感, 王家卫, 杜可风, POV, 广角畸变, 光斑, picbpnew骨架, image2.5]
---

# picbpwjw — 王家卫 × 杜可风电影感 POV 海报提示词（picbpnew 骨架版）

2026-10-23 创建：**生成方式参考 picbpnew**（主题嵌入开头/左上角超大主标题/底部系列署名/右上 FAFO 标注），内容保留 picreal3 的电影感画风（王家卫 × 杜可风 POV/折叠春园/多重不可能阶梯/超广角畸变/刺眼晨光过曝/褪色胶片颗粒/低饱和高对比/动态漏光/彩色光斑/朦胧超现实/荷兰角/空灵治愈）。

## 触发
- 用户给主题/画面并要求「王家卫」「杜可风」「电影感 POV」「广角畸变」「漏光」「胶片颗粒」「空灵治愈」风格
- 用户发来主题，要求「按 picbpwjw 出图」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头 + 左上主标题

## 模板结构（picbpnew 骨架 + picreal3 画风，中文）

请生成一张以「<主题>」为主题的电影感海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体为王家卫 × 杜可风式的主观 POV 镜头语言——观者仿佛刚走过这个场景，情绪化构图与叙事感强烈。画面是一座折叠的春日花园<或由主题派生的室内外空间>，被大片盛开的粉白花朵与绿色植物占领，假山、水池、柔和树影与飘落花瓣交织；空间里存在多重不可能的阶梯——向上的金属旋梯与向下的曲折石阶走向在空间中互不自洽，像折纸般错位，连接不同梦境层。镜头为超广角畸变，前景花朵被放大、边缘拉伸、远处结构变形，空间向内塌陷；构图采用荷兰角倾斜，整个空间从一角向对角倾斜。右侧大片玻璃透入刺眼晨光，太阳几近完全过曝形成强烈光晕与高光溢出；画面有动态漏光——橙黄光斑与绿色光晕，前景与边缘散布柔和彩色 bokeh。画质为褪色胶片质感——胶片颗粒明显、低饱和高对比、暗部深邃亮部耀眼，像一段被时间洗过的记忆。整体氛围朦胧超现实、空灵治愈。画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、电影感艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。右上角粗体字标注：FAFO工作室

## 风格要点（王家卫 × 杜可风语言）
- **镜头**：超广角畸变（ultra-wide distortion）、荷兰角（Dutch angle）、POV 主观视角
- **光**：刺眼晨光（blinding dawn glare）、过曝负空间（overexposed negative space）、动态漏光（dynamic light leaks）、彩色光斑（colorful bokeh）
- **质感**：褪色胶片颗粒（faded film grain）、低饱和高对比（desaturated high contrast）
- **空间**：折叠春日花园、多重不可能的阶梯（超现实纵深）
- **氛围**：朦胧超现实（hazy surreal）、空灵治愈（ethereal healing mood）

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
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 880×1184 即 3:4）
- 长中文提示词写入文件再 $(cat) 传入，避免 shell 转义

## 经验
- **2026-10-23 创建**：picreal3 的 picbpnew 骨架版——主题嵌入开头+左上超大主标题+底部系列署名+FAFO；内容保留王家卫×杜可风 POV 画风（折叠春园/不可能阶梯/广角畸变/晨光过曝/褪色胶片/漏光光斑/荷兰角/空灵治愈）
- **与 picreal3 区别**：picreal3=英文 Midjourney 参数模板（--ar 16:9/--style raw/--stylize 500/--chaos 25/--v 6.1/--no 排除）；picbpwjw=中文 picbpnew 骨架（3:4/左上主标题/系列署名/FAFO）
- **实测（picreal3 原版·2026-10-23）**：POV/折叠春园（粉花绿植占领室内）/多重不可能阶梯/超广角畸变+荷兰角/右侧刺眼晨光过曝/橙黄绿色漏光+彩色 bokeh/褪色胶片颗粒低饱和高对比/朦胧超现实空灵治愈全到位；文字「FAFO / 工作室」成功且无乱码
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picpp + pic1960pp + picbpgd + picbpbookroom + picbpwjw + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picreal + picreal2 + picreal3；触发时按模板区分
