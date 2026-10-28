---
name: picbpgd
description: Use when 要写实温暖亭阁古董柜摄影海报提示词（给主题/画面，白玉青瓷+微尘薄雾，picbpnew 骨架）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 写实摄影, 亭阁, 古董柜, 白玉青瓷, 微尘薄雾, picbpnew骨架, image2.5]
---

# picbpgd — 写实温暖亭阁古董柜摄影海报提示词（picbpnew 骨架版）

2026-10-23 用户指定覆盖：**生成方式参考 picbpnew**（主题嵌入开头/左上角超大主标题/底部系列署名/右上 FAFO 标注），内容保留 picreal 的写实摄影画风（宏大有序温暖亭阁/古董柜陈列白玉摆件与青瓷花瓶/空气中漂浮微尘/微湿反光地板/远处薄雾）。原 v2.0.0 纪实摄影版（清晨渔市/鱼贩）已备份至 `/tmp/picbpgd_v2_documentary_backup.md`。

## 触发
- 用户给主题/画面并要求「写实摄影」「温暖亭阁」「古董柜」「白玉青瓷」「微尘薄雾」风格
- 用户发来主题，要求「按 picbpgd 出图」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头 + 左上主标题

## 模板结构（picbpnew 骨架 + picreal 画风，中文）

请生成一张以「<主题>」为主题的写实摄影海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。画面主体是一座宏大而有序的温暖亭阁式室内空间<或由主题派生的对应场景>，左右对称排列着深色木质玻璃古董陈列柜，柜内陈列白玉摆件、青瓷花瓶、茶具香炉、山水画卷与线装书等古典器物<按主题可替换器物>，空气中漂浮着细微微尘，在暖光下形成丁达尔光斑，地板微湿、表面反光可映出灯光与器物轮廓，远处通往庭院处笼罩一层薄雾，形成近实远虚的层次。画质为高像素写实摄影——真实材质纹理、自然光影过渡、浅景深虚化、微尘颗粒与湿润反光细节清晰。色调以深棕、暗金、暖黄为主调，局部点缀青瓷蓝、玉石白与水墨灰，沉稳内敛带复古东方意境。光影为暖黄灯笼主光+柜内射灯+局部台灯，柔和扩散、自然明暗对比、地面镜面反射，天井处透入一丝冷调自然光形成冷暖对比。画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、金属质感艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。右上角粗体字标注：FAFO工作室

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
- **2026-10-23 创建**：picreal 的 picbpnew 骨架版——主题嵌入开头+左上超大主标题+底部系列署名+FAFO；内容保留写实温暖亭阁古董柜画风（白玉青瓷/漂浮微尘/微湿反光地板/远处薄雾/深棕暗金暖黄）
- **与 picreal 区别**：picreal=英文 Midjourney 参数模板（--ar 16:9/--style raw/--stylize 300/--v 6.1/--no 排除）；picbpgd=中文 picbpnew 骨架（3:4/左上主标题/系列署名/FAFO）
- **历史沿革**：v1.0.0=深黑高对比极简壁纸风（花妞图库）→ v2.0.0=写实纪实摄影（清晨渔市）→ v1.0.0(新)=写实亭阁古董柜骨架版（2026-10-23 覆盖，旧纪实摄影备份在 `/tmp/picbpgd_v2_documentary_backup.md`，如需恢复或另建 `picbpdoc` 可取用）
- **实测（picreal 原版·2026-10-23）**：写实度到位——长廊亭阁/对称玻璃古董柜/白玉雕刻青瓷花瓶/丁达尔微尘/湿地板反光/尽头薄雾全出；暖色深棕暗金暖黄；无卡通无 3D 感；FAFO 工作室金色横匾成功（前提：MJ 参数里 text 从 --no 移除）
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picpp + pic1960pp + picbpgd + picbpbookroom + picbpwjw + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picreal + picreal2 + picreal3；触发时按模板区分
