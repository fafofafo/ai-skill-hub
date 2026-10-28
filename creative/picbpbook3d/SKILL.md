---
name: picbpbook3d
description: Use when 要旅行立体书城市海报提示词（picbpnew骨架，城市主题派生，4:5）。含五元素验收与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 旅行插画, 3D纸雕, 立体书, 水彩, 细线墨绘, 城市地标, picbpnew骨架, 主题驱动, 五元素, image2.5]
    related_skills: [picbook3d, picbpnew, pic-poster-family]
---

# picbpbook3d — 旅行艺术插画·3D纸雕立体书（picbpnew 骨架版）

2026-10-27 创建：`picbook3d`（独立模板型·旅行插画·3D纸雕立体书）套进 **picbpnew 骨架**（2026-10-22 用户定骨架标准），新建平行技能；picbook3d 原技能保留（**用户指定先不覆盖**）。画风/城市主题派生内容原样保留，只换骨架；**五元素验收与 pichotpoolfull/picbook3d 一致（42-55%）**。

## 触发
- 用户要求「picbpbook3d」「旅行插画骨架版」「立体书城市海报（波普骨架）」
- 给城市主题，要求按 picbpnew 骨架 + 3D纸雕立体书画风输出
- 注意：输出**只要提示词内容**；主题（城市）驱动地标与场景元素，画风要素固定

## 骨架标准（继承 picbpnew，四要素缺一即不合格）
1. 主题嵌入开头（「请生成一张以「<主题>」为主题的…」）
2. 画面左上角超大主标题（bold 立体挤压感艺术字 + 利落描边 + 清晰投影 + 第一视觉焦点 + 不能写错字）
3. 底部或角落小号「AIXZD ZHAPU PROJECT SERIES」系列署名
4. 末尾补「右上角粗体字标注：FAFO工作室」

## 画风定义（继承 picbook3d，勿改）
| 要素 | 内容 |
|---|---|
| 画种 | 精致水彩与细线墨绘相结合 + 手工3D纸雕/立体书工艺质感 |
| 核心形态 | 一本古旧打开的书幻化为一座立体微型城市，书页呈浅浅V形折叠 |
| 地标 | 画面中央1座英雄级标志性地标 + 3-5处辅助地标作为背景衬托 |
| 细节 | 微型步道/公园、微小行人、地道交通工具、路灯、树木、花卉、地方特色细节 |
| 光 | 明亮自然光线、微妙阴影、富有氛围感的纵深 |
| 色彩 | 梦幻、优雅、怀旧且充满向往，顶级旅行类编辑品质 |
| 构图 | 4:5竖版，略带仰角的四分之三视角，俯拍角度约25–30°，打开的书占画面下部约30% |
| 禁忌 | 绝不写实摄影、卡通化、平面化、俯视、极端变形 |

## 五元素基准与验收（与 pichotpoolfull/picbook3d 一致，用户指定不变化）
| 元素 | 验收区间 | 实测（测试主题：FAFO工作室）|
|---|---|---|
| 饱和度 | 42-55% | 待测 |
| R-B | +15~+55 | 待测 |
| 明度 | 55-65% | 待测 |
| 柔度 | 0.10-0.22 | 待测 |
| 边缘>40 | 10-20% | 待测 |

**验收**：出图后跑 `python3 ~/.hermes/scripts/img_metrics.py <图>` 五项全落区间；文字另用 VL 逐字复核。

## 模板结构（picbpnew 骨架 + picbook3d 画风，4:5）

请生成一张以「<主题>」为主题的旅行艺术插画海报，4:5 竖版构图。风格：精致水彩与细线墨绘相结合，辅以手工打造的3D纸雕/立体书工艺。一本古旧的打开的书幻化为一座立体的微型城市。画面梦幻、优雅、怀旧且充满向往，呈现顶级旅行类编辑品质。清晰的墨线勾勒建筑轮廓，水彩填色均匀明亮饱满，高饱和色彩鲜艳，阴影浅而通透，明亮自然的高调光线，富有氛围感的纵深。绝不写实、卡通化或平面化。镜头与书籍：略带仰角的四分之三视角，俯拍角度约25–30°。打开的书占据画面下部约30%，书脊位于画面偏下中央，书页呈浅浅的V形折叠。展现真实的书页厚度与层次分明的边缘，纸张边缘清晰锐利。整组作品保持统一的拍摄角度、书籍比例、透视与构图方向，避免俯视或极端变形。城市构图：城市从书页中自然生长而出。在画面中央突出呈现<主题>标志性英雄级地标（如<由主题派生的具体地标名称>），并以3–5处可辨识的辅助地标作为背景衬托。必要时融入<主题>当地的真实河流、滨水区、海岸线、湖泊、山峦、广场或风景元素。前景添加一条微型步道或公园，点缀微小行人、地道交通工具、路灯、树木、花卉以及细腻的地方特色细节。所有建筑均保持直立姿态，结构严谨准确，边缘清晰锐利。色彩与光线：整体色调高调明亮，明亮自然的高调光线（午后阳光感），大面积柔和高光，阴影浅而通透，建筑轮廓有清爽的边缘光。高饱和色彩，饱和度42-55%，色温偏暖R-B+15~+55，明度55-65%，柔度控制在0.10-0.22，边缘清晰度10-20%。画面呈现梦幻、优雅、怀旧且充满向往的氛围，色彩明亮鲜艳、干净通透、不刺眼。画面左上角放置超大主标题「<主题>」，字体为 bold、立体挤压感、现代波普艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面最底部中央区域以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，完整清晰不被遮挡，排版精致克制，不影响主体视觉。右上角粗体字标注：FAFO工作室。除上述文字外不要生成任何其他英文文字或标语。

### 派生规则
- **必须主题派生**：城市名、地标、辅助地标、河流/湖泊/山峦等自然元素、地方特色细节、主标题内容
- **必须固定**：3D纸雕立体书工艺、水彩细线墨绘、4:5竖版、高调明亮、梦幻优雅怀旧氛围、五元素基准、骨架四要素
- **禁止**：照片写实、2D平涂、阴郁暗调、高饱和荧光、俯视、极端变形、多余英文标语

## 出图（默认工具）
**默认生图工具 = 全能图片 G_image2.5 sunburst**（app `2098218128315609089`，~0.036 元/张，输出约 880×1184≈3:4；模板要求4:5 但默认应用不支持 ratio，实际约 3:4）：
```bash
python3 ~/tools/runhub/runhub_img.py t2i "$(cat prompt.txt)" --app 2098218128315609089 --out 输出.png
```
- 仅用户要求高清大图时才走 Z-image 模板（`2055930575931887617`，2160×2896）

## 经验
- **2026-10-27 创建**：picbook3d 独立模板转 picbpnew 骨架平行技能（**用户指定先不覆盖原技能**）；五元素/画风继承 picbook3d（42-55 体系）
- **母版经验继承**（picbook3d FAFO工作室三版实测）：禁用「柔和的水彩晕染」「微妙阴影」；必加「清晰墨线勾勒」「高饱和色彩鲜艳」「高调光线」「边缘清晰锐利」
- pic 技能族：pic1-7 + picbp + picbpnew + picbpwhj + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picsunny2 + picbpsunny2 + picgirlsunny2 + picsunny3 + picbpsunny3 + picgirlsunny3 + piccitypop + picsearoad + picdacnegirl + picsinggirl + pictonghua + picrussiagirlsolider + pichybf + picdjgirl + picdiscoboy + picrainnight + pichkdlj + pictry + picfacebustketball + picupfoodout + picwhj + picskyfo + picbpskyfo + picgirlskyfo + picghost5 + picbpghost5 + picbot + picbpbot + piccat + picbook3d + picbpbook3d + picreal + picreal2 + picreal3；触发时按模板区分
