---
name: picskyfo
description: Use when 要史诗佛教神话巨佛海报提示词（给主题/造像，毗卢遮那佛+莲座+背光+微缩僧人，英文 CGI 模板）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 佛教, 巨佛, 毗卢遮那, 唐代, 史诗, CGI, 巨物, 英文模板, image2.5]
---

# picskyfo — 史诗中国佛教神话巨佛海报提示词（英文 CGI 模板）

2026-10-23 用户提供英文提示词固化：史诗中国佛教神话电影感、超写实电影级 CGI、16:9、戏剧性低角度 24mm 镜头。一尊不可思议体量的唐代毗卢遮那佛结跏趺坐于深青瓷莲座之上，占据画面 80%，上半身延伸出画面上缘。宁静对称的东亚面容、优雅低垂的眼、流动的衣褶、深色古鎏金铜表面带岁月金高光与暖铜阴影。背后巨大圆形背光（mandorla），饰火焰形莲花纹与绿松石镶嵌。金色头光；无量象牙金佛光普照四周巨型墨绿石台与云海。前景石台上立着 ONE 个极微小的僧人，身披深朱砂袈裟，手持 ONE 支直立的中国佛教锡杖（笔直铜杖、小型环状金属杖头）。澄澈蓝宝石天空、暖阳、冷蓝绿阴影、极端尺度、PBR 材质。禁止：塑料金、大理石、多余人物、动漫、文字。

## 触发
- 用户给主题/造像概念并要求「佛教」「巨佛」「毗卢遮那」「唐代造像」「史诗神话」「超写实 CGI」风格
- 用户要求「按 picskyfo 出图」
- 注意：输出**只要提示词内容**；模板为英文；主题/造像嵌描述位置

## 模板结构（用户提供的固定模板，英文）

Epic Chinese Buddhist mythological cinema, ultra realistic cinematic CGI, 16:9, dramatic low angle 24mm shot. An impossibly colossal Tang dynasty Vairocana Buddha seated in meditation on a dark celadon lotus pedestal, occupying 80% of the frame, upper body extending beyond the edge. Serene symmetrical East Asian face, elegant lowered eyes, flowing robe folds, dark antique gilt bronze surface with aged gold highlights and warm bronze shadows. A massive circular mandorla behind, decorated with flame shaped lotus patterns and turquoise inlays. Golden head halo; immense ivory gold Buddha rays illuminate surrounding colossal black green stone terraces and cloud ocean. ONE microscopic monk in dark cinnabar kasaya stands on a foreground terrace holding ONE upright Chinese Buddhist khakkhara - straight bronze shaft, small ringed metal head. Clear sapphire sky, warm sunlight, cool blue green shadows, extreme scale, PBR materials. No plastic gold, no marble, no extra figures, no anime, no text.

## 关键比例与要素（不可替换的设计核心）
| 元素 | 规格 |
|---|---|
| 巨佛占画面 | **80%**，上半身延伸出画面边缘（裁切感强化体量）|
| 微缩僧人 | **ONE 个**，前景石台，持 **ONE 支**直立锡杖 |
| 镜头 | 24mm 低角度仰拍（戏剧性透视）|
| 背光 | 巨大圆形 mandorla + 火焰莲花纹 + 绿松石镶嵌 + 金色头光 |
| 光照 | 无量象牙金佛光 + 澄澈蓝宝石天空 + 暖阳 + 冷蓝绿阴影 |
| 材质 | PBR、深色古鎏金铜（带岁月金高光与暖铜阴影），**非塑料金、非大理石** |

## 主题替换技巧
- 主题/造像嵌开头（如「<主题>」并保留 Tang dynasty Vairocana Buddha 语汇），可换佛尊（释迦/观音/文殊）、朝代造像风格、背光纹样、石台环境
- **不动的部分**：巨佛 80% 占画面+出画裁切 / 一个微缩僧人+一支锡杖 / 24mm 低角度 / 圆形 mandorla+绿松石 / 极端尺度对比 / 禁塑料金大理石动漫
- **禁止项默认保留**：no plastic gold, no marble, no extra figures, no anime, no text（**no text 与 FAFO 标注冲突**：需要品牌文字时必须从禁止项移除 no text，或后期另加）

## 固定标注（所有输出必须带）
每次生成提示词，在提示词末尾（或合适位置）补充一句：**右上角粗体字标注：FAFO工作室**（2026-10-11 用户指定，pic 全部适用）。**注意**：本模板末尾明确 `no text`，两者冲突——若必须保留 FAFO 标注，从 `no text` 中移除该项并在正文写「右上角粗体简体中文标注：FAFO工作室」；若追求画面纯净（宗教庄严感），可省略 FAFO 标注并说明。

## 交付规则（2026-10-12 用户定，pic 全部适用）
- 生成的图片**直接发当前频道**（MEDIA: 路径），不再只发邮箱
- 图片**先不清理**、保留在服务器（用户 2026-10-14 更新：暂不删，后续可能复查/复用）
- 长提示词/中间产物落 /tmp 的可清理，图片文件保留

## 出图（完整流程最后一步）
提示词生成后直接调默认文生图工具出图（RunningHub，见 runhub-image-gen 技能）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- **默认生图应用固定为 image2.5 sunburst (2098218128315609089)**：https://www.runninghub.cn/ai-detail/2098218128315609089（用户 2026-10-11 指定默认，~0.036元/张，不支持 ratio/res，输出约 880×1184 即 3:4——**本模板要求 16:9 横版**，默认 app 出 3:4，严格比例需换支持 ratio 的 app）
- 长提示词写入文件再 $(cat) 传入，避免 shell 转义

## 经验
- **2026-10-23 创建**：用户提供史诗佛教神话 CGI 模板——巨型唐代毗卢遮那佛（80% 占画面/上半身出画）+深青瓷莲座+圆形 mandorla（火焰莲花纹/绿松石）+金色头光+象牙金佛光普照+墨绿石台云海+一个微缩朱砂袈裟僧人持锡杖+24mm 低角+蓝宝石天空暖阳冷影+PBR
- **巨物感原理**：巨佛占 80% 且上半身裁出画面 vs 极微小僧人+锡杖，这个极端体量对比是模板灵魂
- **材质红线**：深色古鎏金青铜（aged gold highlights/warm bronze shadows），**禁塑料金、禁大理石**
- **禁止项**：no plastic gold / no marble / no extra figures / no anime / no text
- **模板类型**：英文电影级 CGI 模板（独立模板型，非 picbpnew 骨架；无 --ar/--style 参数，但正文写死 16:9）
- **2026-10-23 裸测通过（原模板、未加 FAFO 文字）**：巨佛占画面主体、唐代毗卢遮那坐姿、上半身略出画框；深色古鎏金铜+岁月金高光+暖铜衣褶柔影（非塑料金）；圆形曼荼罗背光+火焰莲花纹+绿松石+金色头光；云海+悬空石台+极微小僧人持锡杖；蓝宝石天空+暖阳+冷蓝绿阴影；无文字无多余人物，宗教肃穆感强。唯一偏差=默认 app 出 880×1184（3:4）而非 16:9
- **实测要点**：巨佛「上半身出画」的裁切感是体量关键，提示词保留 `upper body extending beyond the edge`；僧人必须写 `ONE microscopic monk` 才不会被生成成多人
- 可派生：picbpskyfo（picbpnew 骨架场景版）、picgirlskyfo（美女向）、mvp/skyfo（MV 配图）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picskyfo + picreal + picreal2 + picreal3；触发时按模板区分
