---
name: picgirlwjw
description: Use when 要王家卫×杜可风电影感POV美女海报提示词（给主题，折叠春园+不可能阶梯+广角畸变+晨光过曝+褪色胶片，主题派生式）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 电影感, 王家卫, 杜可风, POV, 广角畸变, 美女, 主题派生, image2.5]
---

# picgirlwjw — 王家卫 × 杜可风电影感 POV 美女海报提示词（主题派生式）

2026-10-23 创建：**内容生成方式参考 picgirl（主题派生式）**——画风固定为王家卫 × 杜可风电影感 POV（折叠春园/多重不可能阶梯/超广角畸变/荷兰角/刺眼晨光过曝/动态漏光彩色bokeh/褪色胶片颗粒低饱和高对比/空灵治愈，源自 picbpwjw），人物/背景按主题自动派生「一个美女主体 + 与主题相关的折叠春园场景」，左上角超大主标题=主题。

## 触发
- 用户给主题并要求「王家卫美女」「杜可风」「电影感 POV 美女」「漏光胶片」「空灵治愈」风格
- 用户发来主题，要求「按 picgirlwjw 出图」——自动派生美女主体+折叠春园 POV 场景
- 注意：输出**只要提示词内容**；人物外貌/服装/背景场景由主题派生；画风关键词全部保留

## 模板结构（主题派生式，画风固定）

<主题>（可附：主题相关画面内容提示），王家卫 × 杜可风式主观 POV 电影感镜头，观者仿佛刚走过这个场景，情绪化构图与叙事感强烈，1个<由主题派生的美女外貌：发型发色/五官气质/年龄感>，<由主题派生的服装与姿态>，身处一座折叠的春日花园<或由主题派生的室内外空间>，被大片盛开的粉白花朵与绿色植物包围，假山、水池、柔和树影与飘落花瓣交织，空间里存在多重不可能的阶梯——向上的金属旋梯与向下的曲折石阶走向互不自洽，像折纸般错位连接不同梦境层，镜头为超广角畸变前景花朵被放大边缘拉伸远处结构变形空间向内塌陷，构图采用荷兰角倾斜整个空间从一角向对角倾斜，右侧大片玻璃透入刺眼晨光太阳几近完全过曝形成强烈光晕与高光溢出，画面有动态漏光——橙黄光斑与绿色光晕，前景与边缘散布柔和彩色 bokeh，画质为褪色胶片质感——胶片颗粒明显低饱和高对比暗部深邃亮部耀眼，像一段被时间洗过的记忆，整体氛围朦胧超现实空灵治愈，画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、电影感艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点，细腻皮肤质感，发丝边缘逆光通透，眼神明亮有高光，浅景深，真实自然。

### 派生规则
- **主体**：1 个美女，外貌（发型/发色/气质）和服装按主题合理设计——主题是歌名/地名/概念时，用其氛围联想人设（如「倩女幽魂」→白衣空灵女子；「春光乍泄」→复古衬衫文艺女子；「FAFO工作室」→手拿画稿的创作者）
- **背景**：折叠春园/花植占领的空间，随主题微调（花种/水体/建筑残迹）
- **标题**：左上角超大主标题=主题，bold 立体电影感艺术字+描边+投影，第一视觉焦点，不能写错字
- **画风固定保留**：POV/折叠春园/不可能阶梯/超广角畸变/荷兰角/晨光过曝/动态漏光彩色bokeh/褪色胶片颗粒低饱和高对比/空灵治愈（这串永远不动）
- **构图固定**：POV 主观视角 + 荷兰角倾斜（与 picgirl 仰视面部特写的区别=此处是沉浸式环境人像）

## 画风基准（王家卫 × 杜可风语言，源自 picbpwjw）
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
- **2026-10-23 创建**：内容生成方式参考 picgirl（主题派生式）；画风取自 picbpwjw（王家卫×杜可风 POV）
- **与 picbpwjw 区别**：picbpwjw=场景向（纯空间无人物主体）；picgirlwjw=美女向（1 个美女主体 + 折叠春园 POV 环境）
- **与 picgirl 区别**：picgirl=仰视面部特写；picgirlwjw=POV 沉浸式环境人像+荷兰角倾斜
- **安全提示（继承 picgirl）**：写实人物主题避开「紧身/身材线条」等描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picgirlgd + picgirlbookroom + picgirlwjw + picpp + pic1960pp + picbpgd + picbpbookroom + picbpwjw + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picreal + picreal2 + picreal3；触发时按模板区分
