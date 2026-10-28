---
name: picreal3
description: Use when 要王家卫×杜可风电影感POV海报提示词（给主题/画面，折叠春园+不可能阶梯+广角畸变+晨光过曝+褪色胶片，英文 Midjourney 参数模板）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 电影感, 王家卫, 杜可风, POV, 广角畸变, 光斑, 英文模板, image2.5]
---

# picreal3 — 王家卫 × 杜可风电影感 POV 海报提示词（英文 Midjourney 参数模板）

2026-10-23 用户提供英文提示词模板固化：王家卫 × 杜可风（Wong Kar-wai × Christopher Doyle）电影感 POV、折叠的春日花园、多重不可能的阶梯、超广角畸变、刺眼晨光、过曝负空间、褪色胶片颗粒、低饱和高对比、动态漏光、彩色光斑、朦胧超现实、荷兰角、空灵治愈氛围——（--ar 16:9 / --style raw / --stylize 500 / --chaos 25 / --v 6.1 / --no 排除项）。**独立模板型（英文 Midjourney 参数模板，非 picbpnew 骨架）**。

## 触发
- 用户给主题/画面并要求「王家卫」「杜可风」「电影感 POV」「广角畸变」「漏光」「胶片颗粒」「空灵治愈」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为英文；主题/画面嵌入描述位置

## 模板结构（用户提供的固定模板，英文）

Wong Kar-wai x Christopher Doyle cinematic POV, folded spring garden, multiple impossible staircases, ultra-wide distortion, blinding dawn glare, overexposed negative space, faded film grain, desaturated high contrast, dynamic light leaks, colorful bokeh, hazy surreal, Dutch angle, ethereal healing mood --ar 16:9 --style raw --stylize 500 --chaos 25 --v 6.1 --no text, watermark, logo, cartoon, anime, 3d render

## 主题替换技巧
- 主题/画面嵌入开头描述（如「<主题画面描述>」+ 后续镜头语言元素），末尾保留 --ar/--style/--stylize/--chaos/--v/--no 参数
- 可微调：折叠春园→对应空间（园林/楼梯间/走廊/庭院）、阶梯→对应结构（楼梯/廊桥/层叠台阶）、晨光→对应光源（晨光/夕照/逆光）
- **--no 排除项默认保留**：text, watermark, logo, cartoon, anime, 3d render

## 风格要点（王家卫 × 杜可风语言）
- **镜头**：超广角畸变（ultra-wide distortion）、荷兰角（Dutch angle）、POV 主观视角
- **光**：刺眼晨光（blinding dawn glare）、过曝负空间（overexposed negative space）、动态漏光（dynamic light leaks）、彩色光斑（colorful bokeh）
- **质感**：褪色胶片颗粒（faded film grain）、低饱和高对比（desaturated high contrast）
- **空间**：折叠春日花园、多重不可能的阶梯（超现实纵深）
- **氛围**：朦胧超现实（hazy surreal）、空灵治愈（ethereal healing mood）

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用；本模板 --no text 排除文字，FAFO 标注冲突时省略或画面外处理）。

## 交付规则（2026-10-12 用户定，pic 全部适用）
- 生成的图片**直接发当前频道**（MEDIA: 路径），不再只发邮箱
- 图片**先不清理**、保留在服务器（用户 2026-10-14 更新：暂不删，后续可能复查/复用）
- 长提示词/中间产物落 /tmp 的可清理，图片文件保留

## 出图（完整流程最后一步）
提示词生成后直接调默认文生图工具出图（RunningHub，见 runhub-image-gen 技能）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 3:4——**注意**：本模板要求 16:9 横版（--ar 16:9），默认 app 输出约 3:4，严格比例需换支持 ratio 的 app 或提示用户）
- 长提示词写入文件再 $(cat) 传入，避免 shell 转义

## 经验
- **2026-10-23 创建**：用户提供英文电影感 POV 模板——Wong Kar-wai x Christopher Doyle cinematic POV/折叠春园/多重不可能阶梯/超广角畸变/刺眼晨光/过曝负空间/褪色胶片颗粒/低饱和高对比/动态漏光/彩色光斑/朦胧超现实/荷兰角/空灵治愈/--ar 16:9/--style raw/--stylize 500/--chaos 25/--v 6.1/--no 排除文字水印卡通动漫3D
- **与 picreal/picreal2 关系**：同族英文 Midjourney 参数模板；picreal=温暖亭阁古董柜、picreal2=14mm 超广角书房纵深、picreal3=王家卫×杜可风电影感 POV（唯一带 --chaos 25、--stylize 500、--style raw）
- **核心记忆点**：王家卫杜可风 + 折叠春园 + 不可能阶梯 + 超广角畸变 + 晨光过曝 + 褪色胶片 + 漏光彩色光斑 + 荷兰角 + 空灵治愈
- **模板类型**：英文 Midjourney 参数模板（独立模板型，非 picbpnew 骨架）；画幅 16:9 与默认 app 3:4 不符，出图前说明
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- **2026-10-23 实测「FAFO工作室」**：画风全通过（POV/折叠春园粉花绿植占领室内/多重不可能阶梯/超广角畸变+荷兰角倾斜/右侧刺眼晨光过曝/橙黄绿色漏光+彩色 bokeh/褪色胶片颗粒低饱和高对比/朦胧超现实空灵治愈）；文字「FAFO / 工作室」成功出现且无乱码（前提：把 text 从 --no 排除项移除）；默认 app 实际输出 880×1184（约 3:4，非 16:9）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpy2k + picpp + pic1960pp + picbpgd + picbphuge + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbp3d + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + picbp2 + picbp2sunny + piclove + piclovesunny + picgirl + picsunny + picbpfood + picbpghost2 + picbpqinyong + picgirlghost2 + picmanstory + picmanface + picbookface + piccar + picfgcity + picclimb + picrun + picbprun + picgirlrun + picreal + picreal2 + picreal3；触发时按模板区分
