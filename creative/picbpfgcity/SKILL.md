---
name: picbpfgcity
description: Use when 要复古法式旅行广告海报提示词（给城市名，picbpnew 骨架+mid-century 建筑堆叠徽章）。含模板与出图流程。
version: 1.0.0
metadata:
  hermes:
    tags: [海报, 旅行广告, 复古法式, mid-century, 城市系列, 建筑堆叠, picbpnew骨架, image2.5]
---

# picbpfgcity — 复古法式旅行广告海报提示词（picbpnew 骨架 + mid-century 城市系列）

2026-10-22 用户指定：**生成方式参考 picbpnew**（主题嵌入开头/左上角超大主标题/底部系列署名/右上 FAFO 标注），内容保留 picfgcity 的复古法式旅行广告画风（mid-century 欧洲旅行宣传画/纵向堆叠城市建筑/天空徽章/平面化色块墨线轮廓/奶油白砖红深灰蓝暖橙低饱和/优雅衬线城市名标题）。picfgcity 保留不动。

## 触发
- 用户给城市名并要求「复古旅行海报」「法式旅行广告」「mid-century」风格
- 用户发来完整模板 + 城市名，要求「按原格式重新输出一份」
- 注意：输出**只要提示词内容**；模板为中文；城市名嵌入开头 + 左上主标题（城市英文名）

## 模板结构（picbpnew 骨架 + picfgcity 内容，中文）

请生成一张以「<城市名>」为主题的复古法式旅行广告海报，3:4 竖版构图，尺寸 1086×1448，8K UHD，full-bleed，no outer border，background to canvas edge。整体风格采用复古法式旅行广告海报——20世纪中期欧洲旅行宣传画风格，mid-century graphic design质感，平面化色块、干净利落的墨线轮廓、简化的双色明暗关系，少量深藏蓝结构线增强对比，清晰锐利克制避免数字绘画感过重。画面左上角放置超大主标题「<城市英文名>」，字体为 bold、立体挤压感、优雅粗衬线艺术字，带利落描边和清晰投影，醒目且准确，不能写错字，标题是第一视觉焦点。画面主体为<城市名>代表性建筑群的纵向堆叠插画（如巴黎：深灰蓝色板岩孟莎屋顶、红陶烟囱、老虎窗、精致铁艺阳台、米灰与砖红色立面的 Haussmann 建筑），画面下半部分建筑密集层次丰富前后穿插，上半部分保留大面积浅奶油色天空留白，形成上疏下密的经典旅行海报结构，建筑之间可见远处朦胧低饱和的蓝灰色城市天际线。天空中央放置一个简洁、对称、醒目的<城市名相关徽章图形，如橙色马车徽章>作为视觉中心，干净利落优雅平衡平面化不要复杂装饰不要变形。加入少量生活化细节：阳台上的小人物、街边咖啡馆顾客、飞翔的鸽子，以及少量漂浮的红色、黄色、粉色气球，只作点缀有轻微故事感不喧宾夺主。配色以奶油白、砖红、深灰蓝、暖橙为主，加入少量低饱和粉色和黄色点缀，克制高级统一不要艳丽不要大面积高饱和色彩。光线为柔和均匀的白天漫射光，整体氛围温暖清爽，像晴朗微凉空气通透的<城市名>清晨。底部或次级信息区加入品牌文字 AIXZD ZHAPU PROJECT SERIES，清晰可读字形优雅排版平衡与复古旅行海报气质一致。不要写实摄影质感，不要照片纹理，不要数字渐变，不要镜头虚化，不要3D渲染，不要现代UI感，不要脏污墨渍，不要凌乱边框，不要畸形建筑，不要乱码，不要水印，保持锐利清晰高对比的平面图形边缘。画面底部或角落以不抢眼的方式加入小号品牌文字「AIXZD ZHAPU PROJECT SERIES」，作为系列署名，排版精致克制，不影响主体视觉。最终输出为一张完整的复古法式旅行广告海报，高级统一，系列收藏海报感。

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
- **2026-10-22 创建**：picfgcity 的 picbpnew 骨架版（用户确认「pic吧【fgcity是picbpfgcity」）——主题嵌入开头+左上超大主标题（城市英文名）+底部系列署名+FAFO；内容保留复古法式旅行广告画风（mid-century 城市建筑堆叠/天空徽章/平面化色块墨线轮廓/奶油白砖红深灰蓝暖橙低饱和）
- **与 picfgcity 区别**：picfgcity=原始模板（无左上主标题，主标题在版式中）；picbpfgcity=picbpnew 骨架（左上超大主标题=城市英文名+系列署名+FAFO）
- **核心记忆点**：picbpnew 骨架 + mid-century 城市建筑堆叠 + 天空中央徽章 + 平面化色块墨线轮廓 + 奶油白砖红深灰蓝暖橙低饱和 + 城市系列
- **安全提示**：写实题材避开违规描述（image2.5 安全审查 1501 拦截）
- pic 技能族：pic1-7 + picbp + picbpnew + picbpretro + picbpzh + picbpfgnew + picbpy2k + picpp + pic1960pp + picbpgd + picbpclean + picbpsky + picbpdarkblue + picbpnature + picbpkb + picgta6 + picbpmo + picbpmdage + picbpblue + picbpnsm + picbpmgmh + picbpsskey + picbpfirework + picbpsunny + piclove + piclovesunny + picgirl + picsunny + picbpfood + picbpghost2 + picbpqinyong + picgirlghost2 + picmanstory + picmanface + picbookface + piccar + picfgcity + picbpcar + picbpmanstory + picbpbookface + picbpfgcity；触发时按模板区分
