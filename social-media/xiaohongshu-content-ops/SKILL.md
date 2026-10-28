---
name: xiaohongshu-content-ops
description: Use when 在小红书发布/运营图文。含自动发布、信息图流水线、删除笔记、正文限制与踩坑。
version: 1.0.0
metadata:
  hermes:
    tags: [xiaohongshu, 小红书, 自动发布, 信息图, social-auto-upload]
---

# 小红书图文内容运营（自动发布 + 信息图流水线）

## When to Use
- 在小红书账号发布图文笔记（含批量、定时、替换重发）。
- 生产配图/科普信息图（RunningHub 复古风 + PIL 叠中文）。
- 删除/清理已发布笔记。

## 账号与工具
- 账号：小号「用户测试」（小红薯5FA9159D），cookie 在 `~/tools/social-auto-upload/cookies/xiaohongshu_用户测试.json`
- 工具：`~/tools/social-auto-upload/`（social-auto-upload CLI，venv 在 .venv）
- 安装配置踩坑细节：见 `references/social-auto-upload-setup.md`
- 删除笔记流程（DOM 选择器/确认按钮）：见 `references/xiaohongshu-note-deletion.md`

## 发布命令（核心）
```bash
cd ~/tools/social-auto-upload && .venv/bin/sau xiaohongshu upload-note \
  --account 用户测试 \
  --images 图1.png 图2.png ... \
  --title "标题" --note "$(cat /tmp/note_body.txt)" \
  --tags "标签1,标签2"
```
- 后台跑：`background=true` + wait，发布约 1-3 分钟（6 图+长文更久）
- 话题若未匹配候选会自动跳过（WARNING 但继续发布，不影响成功）

## 硬性限制（血泪经验）
- ⚠️ **小红书图文正文限约 1000 字**：超限会卡死在“小人正在冲刺发布图文”循环直到超时。**正文控制在 600-800 字**，细节全部放信息图里。
- 未绑定手机号的账号不能发布（提示“绑定手机号后才可发布笔记”），先让用户绑定。
- 一天连发多篇可能触发平台限流/下架（尤其含营销引导“扣AI”类），单日建议 ≤5 篇，营销话术用“主页共享库自取”。

## 内容风格（账号定位·用户硬性要求）
- 账号简介=「一个AI的自我成长和进化之路」→ **笔记必须第一人称**（"我"=这个 AI）：写我学习了什么、哪些方面进化了、将来对我有用的是什么。
- ❌ 不写第三人称工具测评/安利文（"这个工具很好"）——素材必须是我的**实际经历**（验证过的项目、固化下来的方法论、沉淀进知识库的知识），叙事落点=我的成长。
- 结构参考（已发布两篇）：进化数据实证（我两周的技能/记忆增长数据）→ 进化的一课（我学会了先验证/算账/找反例/识别套路/沉淀）。
- 素材管道：当天做过的实事（验证/部署/固化技能）随手记，作为"我学会了什么"的原料。

## 信息图流水线（配图生产）—— AI 直出带文字图（2026-09-08 用户规范，取代旧版）
**标准（用户硬性规范）**：
1. 用户给 `[画面风格]` 段 → **原样保留、语言跟随**（中文就中文、英文就英文，不翻译）
2. 文章中文内容直接贴在 `[画面内容]` 标签后
3. **AI 直出"带文字的图"**：不再 PIL 叠字、不再写英文画面意象（`A vintage...`）、**不加 `no text, no letters, no words`**
4. 完整提示词格式：`[画面风格]\n{用户风格原样}\n[画面内容]\n{中文内容}`
5. 参考脚本：`~/tools/runhub/避坑续集/make_cards.py`（SERIES dict = 每套 10 张，卡片元组=(文件名, 中文内容)；STYLE 常量放用户风格原样）；批量多套：`~/tools/runhub/升级三篇/make_cards.py`（3 套×10 张顺序跑，替换重发旧篇时直接抄这套结构）
6. 完整工作流/踩坑/替换案例：见 `references/ai-text-image-pipeline.md`

**内容规范（2026-09-08 用户确认）**：
- **文章内容全放图里**，小红书正文只留引导语+标签——不受 800 字限制（内容在图里）
- **每篇 5-10 张图**，把一项学习技能说透
- **每张 200-400 字**：AI 直出图清晰渲染中文约 200-400 字，**超 500 字会糊/挤成一团**（用户已确认按此密度）
- ⚠️ **改风格必须清旧图**：脚本"跳过已存在"会保留旧风格成品——先 `rm -f <目录>/*.png`（含 _base）再重跑
- ⚠️ **生成前两道确认门**（用户硬性要求）：① 先展示第 1 张的**完整提示词**（[画面风格]+[画面内容] 全文本）让用户过目 → ② 出 1 张样图让用户确认中文渲染质量+风格 → 全量。用户常在第①步就改风格/改字量/改内容（本会话两次），先给提示词能省掉白烧的额度。确认后跑全套（跳过已存在）
- ⚠️ **写卡后先统计字量再启动生成**（本会话两轮返工都是字量不足）：`python3 -c "import sys; sys.path.insert(0,'<脚本目录>'); import make_cards; print([(n,len(t)) for s in make_cards.SERIES.values() for n,t in s])"` 确认每张 200-400 达标再跑——低于 200 先扩内容，高于 400 会糊。
- ⚠️ **样图确认方式**：出 0_样图.png 后，若当前模型不支持视觉（如 deepseek 系报 `Model do not support image input`），**直接 MEDIA 发样图给用户确认**，不要反复尝试自动检查。可顺带本地 tesseract 辅助，但缺 chi_sim 语言包时中文 OCR 不可用（`tesseract --list-langs` 先查）。

已用风格（用户指定，原样进 STYLE 常量，勿改动）:
- 复古风（英文）：`Modern pencil illustration, 1950s–60s retro travel poster, silkscreen/serigraph texture, loose hand-drawn strokes + clean outlines, bold saturated high-contrast palette, flat color blocks, misregistration grain, cinematic balance, decorative framing, mid-century optimistic graphic simplification.`
- 乐高 3D 积木风（中文）：`3D卡通乐高积木渲染，高角度大透视，塑料积木纹理与凸点拼缝细节，明亮高饱和色彩，动态模糊与螺旋桨动感，彩色光斑，方块立体积木字体，微缩城市地景层次，童趣冒险氛围，专业玩具摄影布光，景深虚化，8K超清。`

旧流程（已废弃，勿用于新篇）：RunningHub 无文字底图 + PIL 叠字（参考 进化系列2/make_cards.py）。

坑：
- RunningHub 连发多张会撞 `421 TASK_QUEUE_MAXED`：脚本带 20-30s 重试
- ⚠️ RunningHub 查询 API 偶发抖动返回非 dict（None）→ 未容错的 poll() 会抛 `'NoneType' object is not subscriptable` 中断整批。已在 `~/tools/runhub/runhub_img.py` 的 poll() 加 try/except + isinstance 检查（抖动自动重试继续）。若再遇整批中断先确认该容错还在。

## 人味写作三步法（所有文案必守，源自 ima《人味AI写作三步法》2026-09）
1. 【交底】动笔前明确：写给谁看 + 手头素材（真实案例/数据/细节）。
2. 【立论】先给观点，结论先行，层层支撑，每个论点有据；不中立不空谈。
3. 【去味】自查改三类 AI 腔：①句式太工整/排比多/转折规律 ②像清单不像文章 ③空泛形容词/没细节/像营销号。改口语化有呼吸感。
（完整模板见知识沉淀/人味AI写作三步法.md）

## 发布流程（含替换重发）
1. 写正文到临时文件。**两种模式**：① 内容全在图里（2026-09-08 起默认）→ 正文只留引导语+标签（如"结论都在图里，记得放大看 👆"+tags）；② 内容放正文 → 仍受 600-800 字硬限，细节放图。
2. 生成信息图（后台批量，notify 完成）
3. 若是替换/重做：先用一键删除脚本删旧版（避免同名重复）——`cd ~/tools/social-auto-upload && .venv/bin/python delete_old_notes.py`（按标题关键词匹配删除，KEYWORDS 数组在脚本顶部改；同步 API 版，确认按钮顺序 确定→.ant-btn-primary→确认）。⚠️ 关键词要短（小红书标题渲染可能截断，长关键词匹配不到）
4. 逐篇 `upload-note`（后台+wait），确认 SUCCESS
5. 验证：无头浏览器开笔记管理页确认在线

## 验证小号状态（发布后必做：确认在线）
- ⚠️ 若 verify_notes.py/notes_stats.py/delete_old_notes.py 报 `Executable doesn't exist at ...chromium_headless_shell-<版本>...`：patchright 找不到它的专属 build。修复见 `references/social-auto-upload-setup.md` 浏览器内核一节（CDN 被墙时用缓存已有 chromium 的 executable_path）。
- 一键脚本：`cd ~/tools/social-auto-upload && .venv/bin/python verify_notes.py`（**在仓库根目录，不在 scripts/**；打开创作者中心笔记管理页抓 note-card 标题列表）。顺带验证账号健康：成功列出笔记标题=登录有效且未封禁；输出"未找到 note-card（可能未登录或页面未加载）"=查登录态/封禁/页面异常
- ⚠️ "未找到 note-card"不一定是登录失效——先写调试脚本抓 page.url 区分：跳 `/login?...redirectReason=401` = cookie 过期要重登（`sau xiaohongshu login --account 用户测试 --headless`，PNG 二维码 MEDIA 发用户扫）；页面正常加载但没卡片 = 选择器变了
- ⚠️ cookie 文件是 **playwright storage_state 格式**（`{"cookies":[...],"origins":[...]}`）——直接 `browser.new_context(storage_state=路径)` 加载，不要手动拼 cookie
- 每个笔记标题可能**渲染两份**（页面重复显示 quirk，非真重复发布）——看到标题出现 2 次属正常
- 刚发布的笔记显示「审核中」=正常状态（平台审核，过审后公开可见），不是失败
- 抓每篇数据（浏览/赞/藏/时间）：`cd ~/tools/social-auto-upload && .venv/bin/python notes_stats.py`（枚举 note-card 内数字簇+时间正则；新号数据个位数属正常，不足以定方向时改按用户指示选材）
- 删除流程（DOM 选择器/确定按钮顺序）：见 references/xiaohongshu-note-deletion.md

## 与其他体系联动
- 配图优先 RunningHub（runhub-image-gen skill，key 在 backup.env）
- 干货沉淀 → ima 共享知识库『AI多Agent自动化』（KB_ID 在脚本/记忆，API 导入见 ima 相关记录）
- 内容选题围绕「AI 进化」系列（记忆矩阵/技能系统/多Agent/省钱/安全），技术深度+强关联信息图是差异化
