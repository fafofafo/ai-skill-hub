---
name: picbpbackroom
description: Use when 要后室阈限空间海报提示词（给主题/歌名，Backrooms Aesthetic）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 后室, Backrooms, 阈限空间, Liminal, 黄墙, 荧光, 恐怖氛围, image2.5]
---

# picbpbackroom — 后室阈限空间海报提示词（Backrooms Aesthetic）

2026-10-20 用户提供风格定义并固化：Backrooms Aesthetic 后室美学 / Liminal Space 阈限空间——无尽重复建筑、黄墙米地毯、荧光灯、非欧空间、诡异熟悉感、安静心理恐怖。内容形式照搬 picbpnew（主题嵌入开头/左上超大主标题/系列署名/FAFO标注），画质/色调/风格换 Backrooms 三段。

## 触发
- 用户给主题并要求「后室」「Backrooms」「阈限空间」「Liminal Space」「liminal」「黄墙荧光」「无限走廊」「诡异熟悉感」「心理恐怖氛围」风格
- 用户发来完整模板 + 主题，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；主题嵌入开头；主题是歌名/地名/概念时自动联想后室场景

## 风格核心（用户提供的固定描述）
- **定义**：Backrooms Aesthetic 后室美学 / Liminal Space 阈限空间——uncanny familiarity 诡异熟悉感
- **画面元素**：endless repetitive architecture（无尽重复建筑）、yellow-beige wallpaper（黄米色墙纸）、mustard yellow walls（芥末黄墙）、stained beige carpet（污渍米色地毯）、old commercial interiors（老商业室内）、fluorescent ceiling lights（荧光天花板灯）、endless corridors（无尽走廊）、impossible architecture / non-Euclidean space（不可能建筑/非欧空间）
- **光效**：flat fluorescent illumination（扁平荧光照明）、weak shadows（弱阴影）、washed-out colors（褪色）
- **氛围**：oppressive emptiness（压迫性空虚）、quiet psychological horror（安静心理恐怖）、nostalgic yet disturbing（怀旧又不安）、surreal liminal atmosphere、uncanny realism（诡异写实）
- **质感**：1990s-2000s digital camera aesthetic（千禧年数码相机）、low-resolution CCD photography（低分辨率 CCD 摄影）、VHS texture（VHS 纹理）、analog video noise（模拟视频噪点）、chromatic aberration（色差）、subtle lens distortion（轻微镜头畸变）、compression artifacts（压缩伪影）、slight motion blur（轻微运动模糊）、found footage aesthetic（发现录像美学）
- **禁止**：no obvious monster（无明显怪物）、no gore（无血腥）

## 模板结构（中文，主题嵌入开头）

请生成一张以「<主题>」为主题的 Backrooms 后室阈限空间海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用 Backrooms Aesthetic 后室美学 / Liminal Space 阈限空间——无尽重复建筑、黄米色墙纸、芥末黄墙、污渍米色地毯、老商业室内、荧光天花板灯、无尽走廊、不可能建筑/非欧空间，uncanny familiarity 诡异熟悉感，surreal liminal atmosphere，quiet psychological horror，nostalgic yet disturbing，uncanny realism。画面主体为<由主题联想的主体，如人物/物件/歌名意象>，置于<由主题联想的后室场景，如无尽走廊/老商业空间/黄色房间>中，场景包含<主题相关的阈限空间细节，如重复墙纸、荧光灯管、污渍地毯、老式门、旧海报、角落阴影>，压迫性空虚，无逻辑但和谐。画面左上角放置超大主标题「<主标题>」，字体为 bold、立体挤压感、低像素数字艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。光效为扁平荧光照明、弱阴影、褪色 washed-out colors。质感为 1990s-2000s 数码相机美学、低分辨率 CCD 摄影、VHS 纹理、模拟视频噪点、色差、轻微镜头畸变、压缩伪影、轻微运动模糊、found footage 发现录像美学。画面中无明显怪物、无血腥，安静的心理恐怖与怀旧不安氛围。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的 Backrooms 后室阈限空间海报，诡异熟悉、怀旧不安、安静压抑。

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
- **核心记忆点**：后室 Backrooms + 无尽重复走廊 + 芥末黄墙黄米墙纸污渍地毯 + 荧光灯扁平照明弱阴影褪色 + 非欧空间不可能建筑 + 千禧年低像素 CCD/VHS 噪点色差压缩伪影 found footage + 安静心理恐怖怀旧不安；**无怪物无血腥**
- **主题替换技巧**：主题=歌名/地名/概念时嵌入开头并附一句画面内容，后室元素与质感光影关键词全部保留；主题是歌名/概念时可把「无尽走廊」当作「走不出的空间」隐喻
- **风格差异**：与 picbpretro（欧美复古未来电影感，老车+宇宙+冷调胶片）不同——本技能是室内阈限空间+黄墙荧光+低像素录像质感，安静压抑；与 picbpclean（梦核治愈温柔怀旧）不同——本技能是梦核的阴暗面（怀旧+不安）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picgirly2k + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny；触发时按模板区分
