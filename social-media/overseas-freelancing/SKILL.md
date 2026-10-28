---
name: overseas-freelancing
description: Use when 用户在 Upwork/Guru 海外平台接单。含平台验证码墙、半自动分工与素材。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [freelance, upwork, guru, 接单, 海外变现, freelancing]
    related_skills: [content-intelligence]
---

## When to Use
- 用户要在 Upwork / Guru 等海外自由职业平台接单（AI 客服、RAG、自动化、内容营销）
- 涉及"AI 自动接单"诉求、平台访问/登录问题、写报价

## 平台访问现实（实测 2026-08，先记住别白费力气）
- **Upwork：数据中心 IP 全封（HTTP 403，Cloudflare）**。腾讯云、七牛云都试过，浏览器自动化、curl 全无效。**只有住宅 IP（用户手机/家用网）能访问**，且挂 VPN 也会被拦（提示 "network restrictions and/or traffic blocking at your location"）。
- **Guru（2026-08 实测 HTTP 200；2026-10 起 curl/urllib 全 403）**：Incapsula 反爬墙已封数据中心 IP 直连（curl/urllib/requests 都返回 403 Incapsula 拦截页）——独立脚本抓单**此路已断**。但 **Hermes web_extract 工具通道可用**（返回 head+tail 窗口，完整文本落盘 ~/.hermes/cache/web/*.md 可 read_file 读全）——找单走 web_extract 通道，由「guru」项目经理 Bot（guru_77e69c）按需拉单（原 cron 8a828015 已暂停）。注册/登录仍有 reCAPTCHA，服务器自动登录**此路不通**。
- 结论：这类平台都设了"真人墙"（验证码/IP 风控）。**"AI 全自动注册+登录+投递"做不到**——不要反复试，不要承诺。

## 半自动接单分工（本会话验证的最优解）
```
我（AI，全自动）：定时抓任务 → 筛匹配单 → 写定制英文报价 → 推送
用户（10秒）：打开单子 → 复制粘贴报价 → 点发送（过验证码那一下）
客户回复 → AI 写回复 → 用户转发 → 成交后 AI 协助交付
```
- 找单/写报价（最费脑的活）AI 全包；只剩"真人验证码"那一步必须用户。

## Guru 平台速览（付费/机制）
- 免费 Basic：10 报价/月，佣金 9%（比 Fiverr 20% 便宜）；Professional 7%（$21.95/月）
- 付款：SafePay 托管（客户先存钱，验收后放款）；收款 Payoneer/PayPal/电汇 0-7 天
- 找单：`guru.com/d/jobs/`（无需登录可看）；投递 = Send a Quote

## 素材资产（已落盘 /home/ubuntu/）
- `upwork_profile.md` — 英文 Profile 全文（AI Agent Developer | Chatbot & Automation Expert）
- `upwork_guide.md` — 注册→投递→收款→涨价全流程
- `upwork_proposal_template.md` — 定制报价模板（demo-first + 开源不锁定）
- `ai_cs_sales.md` / `ai_cs_pitch.md` / `ai_cs_client_guide.md` — 本地 AI 客服接单三件套
- `gen_business_cs.py` — 一键生成方案书（`python3 gen_business_cs.py --name "客户" ...`）
- `~/项目目录/guru_job_finder.py` — 旧版 curl 找单器（**curl 通道已废**，仅参考解析/筛选逻辑；现役找单走 web_extract 通道，见下方技术要点）

## 找单器技术要点（2026-10 起通道已换）
- 抓取：**web_extract 工具**抓 `https://www.guru.com/d/jobs/`（免登录；curl/urllib 直连已被 Incapsula 403 封死，勿再试）。返回 head+tail 窗口 + footer "Full text saved to: <路径>" → 用 read_file 读完整文件再解析
- 解析：正则匹配 `## [标题](https://www.guru.com/jobs/...链接)`，链接去掉 `&SearchUrl` 及 `?` 之后部分；主页约 20 单，翻页 2-N 扩大覆盖（每页 20 单）；分页链接丢失时用搜索逐一定位精确 URL 核验
- 关键词匹配要防误报：`"ai"` 会命中 "paid"（含子串 ai）→ 用带空格的关键词（`" ai "`）+ EXCLUDE 词表（paid/data collection/video editing 等）
- 筛选后给用户：标题 + `https://www.guru.com<job链接>`，附写好的英文报价
- **投递包交付形态**：全量找单+报价先落盘 `找单报价-<日期>.md` 留存，另抽**优先 1-2 单**（链接 + 可直接复制的英文报价 + ≤3 步投递说明 + 预算/截止/优先级标注）成独立 `今日投递包-<日期>.md` 发给用户——用户只做"打开→复制→Send a Quote"过验证码那一下，不翻长文档；投完让用户回报一句，再把 决策清单.md 该项状态改为 待投递→进行中/完成

## 报价要点（拿单关键）
- 前 1-2 单低价拿评价（$15-20/hr 或小固定价），**有评价后提价 +30-50%**（2026-09-30 NightCafe 借鉴：编排能力×服务=溢价；$15-20/hr → $25-30/hr）
- demo-first："I can show you a working prototype within 48 hours before you commit"
- 抄客户原话证明读懂了 Job；开源不锁定 + 里程碑交付
- 客户要求提交"实现方案+周期+报价"的单子优先投（有明确路径）
- **定位话术（2026-09-30）**：立"AI Workflow Engineer / 最佳模型组合+自建工作流"人设，不养模型=卖点（轻/快/无锁定）；别说"我用XX开源模型/工具"（显套壳）
- 详细模板与分阶段定价见 `upwork_proposal_template.md`

## 接单交付三原则（报价/交付纪律，多源经验沉淀）
1. **需求调研透**：动手前把需求聊透，引导客户挖真实意图，用客户听得懂的业务语言（别甩技术术语）
2. **验收标准定死**：协议里写明验收标准与修改次数（通常 3-5 次），避免完成后无休止扯皮
3. **迭代交付**：拆阶段，每阶段让客户确认，别做完才给看（及时纠偏，防大规模返工）
报价模板应带"里程碑交付 + 验收标准 + 修改次数 + 售后维护期（1-3 月）"条款。

## 平台选型（多源印证）
- 海外平台（Guru/Upwork/Freelancer/RemoteOK）性价比远高于国内——多篇独立来源印证"赚美金 > 国内平台"
- 国内备选：码市（Codemart，Coding 旗下，竞争不惨烈）、程序员客栈（对接池+面试派单，口碑好但性价比一般）
- 避坑：猪八戒类"先交会员费 + 低价竞争 + 虚假需求"平台不碰；开源众包会员制对新手不友好

## 平台 API 现实（2026-09 验证）——别指望"API 自动接单"
- **没有平台提供"浏览市场/自动投递"的公开 API**——平台故意设真人墙（验证码/IP 风控），API 开放会破坏反自动化防线
- Guru：无公开 API（搜到的 developer.getguru.com 是另一家知识管理公司）；Fiverr：Discover API 只能搜服务不能接单
- Upwork：有 API 但门槛极高（需 $25k 终身收入 + JSS 90%+ 才能申请），且官方明确"只能访问自己账户，不能搜索/浏览市场工作列表"
- RemoteOK：免费公开 API（无需 key，60req/min）——但那是**远程全职岗聚合**，不是接单平台
- 结论：自动化只能走"网页抓单 + AI 写报价 + 用户过验证码"的半自动形态，此路已被多次验证

## 避坑铁律（w2solo 5 条 + 中消协 2026-05 七类培训套路）
1. **拒绝无预付全款项目**：外包预付款 ≥30-40%；口头分成/技术入股白嫖一律不接
2. **高薪低门槛 = 骗局**："0元学/几天速成/在家接单赚钱"99% 是培训费/证书费钩子（中消协曝光第一类数字技能培训，平均涉诉超 7000 元）
3. **全职务必签劳动合同**（海外用工优先 Deel 签约，防欠薪）
4. **拒绝私人电脑装监控软件**（桌面截屏/键盘监控 = 隐私风险）
5. **海外接单不走私人转账**，一律平台托管结算（避开地下换汇被骗）

## Pitfalls
- 不要为绕过验证码用住宅代理/VPN 硬绕：Upwork 检测异常 IP 会**封号**，账号是资产，别冒险
- 定价算进平台佣金（Guru 9% / Upwork 10%）和订阅费（跟单 $30/月对 500 账户不划算）
- 本地/线下接单优先级高于海外平台（第一笔钱更快）
