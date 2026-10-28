---
name: picgirlfgnew
description: Use when 要新复古主义美女海报提示词（给主题/歌名，New Retro Style）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 新复古主义, 美女, 圆润几何, 奶油焦糖撞色, 高光塑料, 主题派生, image2.5]
---

# picgirlfgnew — 新复古主义美女海报提示词（New Retro Style，主题派生式）

原 picsunfgnew，2026-10-20 用户重命名为 picgirlfgnew（对齐 picgirl 系列命名）。

2026-10-20 创建：**内容参考 picgirl（原 picsun）生成方式（主题派生式）**——画风固定为 New Retro Style 新复古主义（源自 picbpfgnew），人物/背景不再固定，每次按主题自动派生「一个美女主体 + 与主题相关的合适背景」，左上角超大主标题=主题。主题自定义，画风永远参考原始提示词。

## 触发
- 用户给主题并要求「新复古」「New Retro」「美女」「Mid-century」「Space Age」「圆润几何」「奶油焦糖撞色」风格
- 用户发来主题/歌名，要求「按 picgirlfgnew 出图」——自动派生美女主体+相关背景
- 注意：输出**只要提示词内容**；人物外貌/服装/背景场景由主题派生；画风关键词全部保留

## 模板结构（主题派生式，画风固定）

<主题>（可附：主题相关画面内容提示），New Retro Style 新复古主义，当代设计重新诠释 20 世纪 60-90 年代复古美学，Mid-century Modern，Space Age，70s retro，80s graphic design，90s commercial photography，圆润流线型工业设计，soft geometry，rounded geometry，capsule shapes，bubble forms，拱形结构与模块化几何，大胆几何排版，棋盘格，条纹，圆点，渐变与复古印刷图形，现代商业摄影与复古广告融合，高精度 3D 渲染，干净精致，1个<由主题派生的美女外貌：发型发色/五官气质/年龄感>，<由主题派生的服装与姿态>，<由主题派生的合适背景场景>，画面左上角放置超大主标题「<主题>」，字体为 bold、粗体无衬线、复古广告艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点，仰视角度，面部特写，真实皮肤纹理，细腻毛孔，柔和棚拍光，眼神明亮有高光，硬质阳光与长阴影，柔和 Bloom，轻微胶片颗粒，复古印刷色偏，电影级构图，色彩明快，怀旧精致。

### 派生规则
- **主体**：1 个美女，外貌（发型/发色/气质）和服装按主题合理设计——主题是歌名/地名/概念时，用其氛围联想人设（如「富士山下」→和服少女+樱花；「海阔天空」→海边风衣女子；「时光之城」→复古裙装少女+拱门场景）
- **背景**：与主题强相关的合适场景，一句话点明（地点/天气/元素），不脱离主题
- **标题（参考 picbpnew）**：左上角超大主标题=主题，bold 立体艺术字+描边+投影，第一视觉焦点，不能写错字
- **画风固定保留**：New Retro Style/圆润胶囊几何/奶油白焦糖棕撞番茄红青蓝/高光塑料磨砂金属亚克力铬/棋盘格条纹圆点渐变/棚拍光长阴影/Bloom/胶片颗粒（这串永远不动）
- **构图固定**：仰视角度 + 面部特写（保留 picgirl 原始视觉语言）

## 画风基准（New Retro Style，源自 picbpfgnew）
- **定义**：New Retro Style 新复古主义——当代设计重新诠释 20 世纪 60-90 年代复古美学：Mid-century Modern、Space Age、70s retro、80s graphic design、90s commercial photography、retro futurism
- **形态**：圆润流线型工业设计、soft geometry、rounded geometry、capsule shapes、bubble forms、拱形结构与模块化几何
- **配色**：奶油白、米黄、焦糖棕、芥末黄、番茄红、橙色、橄榄绿、薄荷绿、复古青蓝，局部高饱和撞色
- **材质**：高光塑料、磨砂金属、透明亚克力、彩色玻璃、搪瓷、胡桃木、拉丝铝、chrome metal
- **图形语言**：大胆几何排版、粗体无衬线字体、棋盘格、条纹、圆点、渐变与复古印刷图形
- **光效/质感**：现代商业摄影与复古广告融合，柔和棚拍光、硬质阳光与长阴影、柔和 Bloom、轻微胶片颗粒、复古印刷色偏
- **氛围**：干净精致、高级、时尚、怀旧但不陈旧——retro nostalgia with contemporary aesthetics

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
- **2026-10-20 创建**：内容生成方式参考 picgirl（主题派生式：美女主体+相关背景随主题、画风冻结、左上角主题标题）；画风取自 picbpfgnew（New Retro Style 新复古主义）
- **核心记忆点**：New Retro（圆润胶囊几何/棋盘格条纹/奶油焦糖撞番茄红青蓝/高光塑料铬亚克力）+ 棚拍光长阴影 + 仰视面部特写 + Bloom/胶片颗粒 + 复古印刷色偏 + 怀旧精致
- **主题替换技巧**：主题=歌名/地名/概念时嵌入开头并附一句画面内容，人设与画风关键词全部保留
- **安全提示（继承 picgirl）**：写实人物主题避开「紧身/身材线条」等描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpy2k + picgirlfgnew + picgirly2k + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny；触发时按模板区分
