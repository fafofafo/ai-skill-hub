---
name: picupfoodout
description: Use when 要食物飞溅特效提示词（图生图，基于上传图）。含 i2i 流程。
version: 1.0.0
metadata:
  hermes:
    tags: [图生图, i2i, 食物飞溅, 超写实, 广告质感, 高速摄影]
    related_skills: [runhub-image-gen, pic-poster-family]
---

# picupfoodout — 食物腾空飞溅特效（图生图 i2i）

2026-10-26 用户提供完整中文模板固化：**图生图（i2i）技能**——用户上传「人物手持怼在镜头前的食物/饮品」照片，保持原图完全不变，仅把食物/饮品做成超写实腾空飞溅瞬间。非文生图（无主题派生），基于上传图编辑。

## 触发
- 用户要求「picupfoodout」「食物飞溅」「饮品飞溅」「腾空飞溅特效」
- 用户上传人物手持食物/饮品的图片，要求做飞溅特效
- 注意：**必须 i2i 图生图**（需要上传原图），不能文生图；输出**只要提示词内容**（用于 i2i 的编辑指令）

## 模板结构（中文，i2i 编辑指令，直接发给图生图工具）

请根据我上传的图片，保持图片完全不变，仅以人物手持怼在镜头前的食物或饮品为中心，制造超写实的腾空飞溅瞬间。根据原有内容自然表现：固体翻腾散开，液体形成舒展的飞溅弧面与细小液滴，配料随之悬浮。动势从容器内部向上、向外并朝镜头展开，突出近大远小的透视与扑面而来的冲击感。保持容器完整，不添加无关食材，不遮挡人物面部。材质、光线与阴影融入原照片，呈现高速摄影定格般的清晰细节与广告质感，避免卡通感。

## 图生图流程（i2i）
**默认工具 = 全能 image2 图生图/文生图 V1.0**（app `2047883048150110209`，~0.108 元/张）：
```bash
python3 ~/tools/runhub/runhub_img.py i2i "$(cat prompt.txt)" 上传图.png --out 输出.png
```
- 上传图：用户发来的手持食物/饮品照片
- 若需更高清：image2.5 Sunburst i2i（app `2097970230151704577`，~0.22 元/张）

## 固定要求（用户 2026-10-26 定，勿改）
- **保持图片完全不变**（仅食物/饮品区域做飞溅）
- **保持容器完整**、不添加无关食材、**不遮挡人物面部**
- 材质/光线/阴影融入原照片，高速摄影定格清晰细节+广告质感，**避免卡通感**
- 动势从容器内部向上/向外/朝镜头展开，近大远小透视+扑面冲击感

## 经验
- **2026-10-26 创建**：用户提供完整 i2i 模板固化（图生图技能，需上传原图）
- **2026-10-26 实测**：用户上传图 i2i 成功（重试14次后提交成功，输出 880×1184）；**i2i 无五元素验收**（特效图以「保持原图+飞溅效果+无卡通感」为准），跑通即可交付
- **注意**：文生图工具（image2.5 sunburst）不能用于本技能，必须走 i2i app；上传图片走 `/openapi/v2/media/upload/binary`（脚本自动处理）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpfgnew2 + picbpy2k + picbpbackroom + picbpkt + picgirlkt + picgirly2k + picbpgd + picbpbookroom + picbpwjw + picgirlgd + picgirlbookroom + picgirlwjw + picgirlskysea + picpp + pic1960pp + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picsunny2 + picbpsunny2 + picgirlsunny2 + picsunny3 + picbpsunny3 + picgirlsunny3 + pichybf + picdjgirl + picdiscoboy + picrainnight + pichkdlj + pictry + picfacebustketball + picupfoodout + picskyfo + picbpskyfo + picgirlskyfo + picghost5 + picbpghost5 + picreal + picreal2 + picreal3；触发时按模板区分
