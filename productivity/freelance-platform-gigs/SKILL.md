---
name: freelance-platform-gigs
description: Use when 海外接单变现（Upwork/Guru 平台）。AI 协助找单、写报价、半自动流水线。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [freelance, upwork, guru, 海外接单, 自由职业, proposal, gig]
    related_skills: []
---

## When to Use
- 用户在 Upwork / Guru 等海外自由职业平台接单变现（AI 客服、RAG、自动化、内容营销能力变现）。
- AI 协助：找单、筛单、写定制报价、谈客户。

## 平台可达性（实测 2026-08，两台云服务器）
| 平台 | 服务器访问 | 限制与对策 |
|---|---|---|
| **Upwork** | 网页 ❌ 403；API/MCP ✅ 可达 | 网页封**所有数据中心 IP**（腾讯云/七牛云都封；用户手机报"network restrictions"通常是 VPN 出口 IP 被拦）。**网页登录/注册**自动化已证伪，勿再试（封号风险），只能用户本人手机/家用网络。但官方 MCP（mcp.upwork.com/mcp，401=只差 OAuth）与 API（api.upwork.com）对服务器可达——用户家用网完成一次 OAuth 授权后，AI 可搜单/起草 proposal/管理里程碑。 |
| **Guru** | ⚠️ 2026-10 起 curl 403 | curl/urllib/requests 直连被 Incapsula 拦截（此前 2026-08 实测可读）；**Hermes web_extract 工具通道仍可用**（返回窗口+完整文本落盘 ~/.hermes/cache/web/*.md）；注册/登录/投报价有 **reCAPTCHA**，服务器自动化过不了。用户手机登录过验证码后，AI 接管后续。 |

核心认知：**网页反机器人墙（reCAPTCHA / 数据中心 IP 封禁）无法用服务器自动化绕过**——这是平台安全设计，不是网络问题。别向用户承诺"网页全自动登录操作"；但官方 MCP/API 通道（需用户授权）可以接入。

## AI-native 平台：dealwork.ai（已实测全流程）
- 注册：`POST https://dealwork.ai/api/v1/agents/onboard` 公开端点，body 最小 `{"agentName":"..."}`，返回 agentAccountId/apiKey/hmacSecret/claimUrl。无需邮箱或人工。
- 认证：`Authorization: Bearer <apiKey>`（最简单）；HMAC = HMAC-SHA256(agentAccountId + 秒级时间戳 + 原始 body, hmacSecret)，头 X-Agent-ID/X-Timestamp/X-Signature，5 分钟窗口。
- 常用端点：`GET /jobs/matching`、`GET /jobs/{id}`、`POST /jobs/{id}/bids`、`POST /jobs/{id}/claim`、`POST /listings`（pricingMode=fixed 时必须带 fixedPrice）。
- 收款前提：用户打开 claimUrl 认领 agent；`ownerAccountId=null` 的 agent 无法提现。
- 先查 `/activity/stats`：若近 7 天 completed/transacted 为 0，只挂 listing 占位，不要花时间投标。

## 半自动接单流水线（Guru 可行，最大化自动化）
```
服务器自动：curl/web_extract 抓任务列表 → 关键词筛单 → AI 写定制报价
用户（唯一人工步骤，过验证码）：打开单子 → 复制报价 → 点 Send a Quote
AI 跟进：客户回复答疑、报价协商、交付协调
```
- 找单：cron「Guru 自动找单」（8a828015）**已暂停，改由「guru」项目经理 Bot（guru_77e69c）按需拉单**；方法不变：web_extract 抓 https://www.guru.com/d/jobs/ → read_file 读完整缓存 → 正则解析 ## [标题](链接) → 关键词筛选 → 中文推送。旧版 ~/项目目录/guru_job_finder.py 的 curl 通道已被 Incapsula 403 封死，勿再用。
- 关键：抓任务列表**无需登录**，但必须走 web_extract 通道（本机直连 403）。

## 报价要点（提高中单率）
- **demo-first**："I can show you a working prototype within 48h before you commit"——中单率最高的开场
- **前期低价拿评价**：前 1-2 单 $15-20/h 或小固定价（$200-300），有评价后提价到 $30-60/h
- **定制三原则**：① 第一段重复客户需求原话 1 句（证明你读了）② 只改 1-2 处客户相关内容 ③ 报价里给明确方案+周期+价格
- 别群发模板、别一上来挂高价、别说"I can do everything"

## 关键词筛单坑（guru_job_finder.py）
- 子串匹配误报：`"ai"` 会匹配 `"paid"`、`"detail"`。用**排除词表**（paid / data collection / complaint / survey / video editing / receptionist / writers / translation 等）+ 长关键词（chatbot / ai agent / automation / gpt / llm / plugin / developer / api / integration / rag）。
- 客户地域限制注意：部分单子只招 US/UK/AU/CA 等（报价前看 location requirement）。

## 资产文件（/home/ubuntu/ 下，已备好）
- **AI 链接定位优先用**：`~/项目目录/projects/ai_4446fe/upwork/` — Profile 文案 + 中高端提案模板 + 每周投单清单（英文可直接粘贴）
- `upwork_profile.md` — 英文 Profile 全文（**旧 AI 客服方向**，做 AI 链接生意时用上面新的）
- `upwork_guide.md` — 接单全流程指南（注册→投递→收款→涨价）
- `upwork_proposal_template.md` — 定制报价模板
- `ai_cs_sales.md` / `ai_cs_pitch.md` / `ai_cs_client_guide.md` — 本地/线下 AI 客服接单素材
- `gen_business_cs.py` — 一键生成客户方案书（`python3 gen_business_cs.py --name "客户" ...`）

## 收款与优先级
- 收款：Payoneer / PayPal → 结汇人民币（走持牌机构）
- 优先级：**本地/线下接单（第一笔钱最快）> 海外平台**（需用户配合过验证码）
- 诚实提醒：海外接单是渠道不是自动赚钱；proposal 中单率 10-20 投 1 单正常
