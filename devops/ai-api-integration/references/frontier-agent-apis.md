# 前沿 AI 代理产品 API 接入速查（Grok / Muse / Dots）

> 场景：用户问"能不能用 Grok/Muse/Dots"、接单要不要用这三家、小G 素材包更新。
> 核心分辨：Grok Bot / Muse / Dots 是三家各自推出的**代理产品**（自带云电脑/会自己动手办事），
> 产品本体大多不开放；**能对接的是它们背后的模型 API**。先分清"接大脑"还是"接身体"。

## 三家一览

| 产品 | 厂商 | 产品本体开放度 | 可对接的 API | Hermes provider |
|---|---|---|---|---|
| Grok Bot | xAI | 产品封闭 | xAI API（Grok 4.x） | xai（内置） |
| Muse | Meta | App 不开放；有连接器平台（muse.ai/platform，审核制） | Meta Model API（Muse Spark/Wonder） | meta-ai（v0.21.0+ 内置） |
| Dots | OpenAI | 仅 ChatGPT Pro/企业订阅，无公开 API | OpenAI API（GPT-6 Astra）+ OpenAI Agents API（托管 Codex harness） | openai / openai-codex |

## 接入参数（价格/地区限制会变，报价前重验）

### Grok（xAI API）
- base_url `https://api.x.ai/v1`，key `XAI_API_KEY`，模型 Grok 4.x 系。
- Hermes `hermes model` 选 xai 即可，内置 provider。

### Muse（Meta Model API）
- base_url `https://api.meta.ai/v1`，key `MODEL_API_KEY`（dev.meta.ai 注册，**预览期仅美国区**）。
- 模型：`muse-spark-1.3`/`1.2`/`1.1`，**100 万 token 上下文**，OpenAI/Anthropic 双格式兼容（Responses/Chat Completions/Messages）。
- 定价参考：标准档约 $1.25/$4.25 每 M；contributor 档约 $0.10/$0.20 每 M（**Meta 可能用 contributor 数据训练**——客户数据敏感就别推这档）。
- 替代通道：OpenRouter `meta/muse-spark-1.3`；开源权重 `meta/muse-glimmer-30b`（约 $0.30/$1.20 每 M，131K 上下文，可本地/第三方托管）。

### Dots（OpenAI）
- 产品本体（个人 dot、云电脑、4000+ 应用连接）**无公开 API**，只在 ChatGPT Pro/Business/Enterprise 订阅内。
- 底层模型 GPT-6 Astra 走 OpenAI API。
- **OpenAI Agents API**（`/v1/agents/sessions`，`OpenAI-Beta: agents=v1` 头）：OpenAI 托管 Codex harness——云端沙箱、持久会话、自动上下文压缩、多子代理、MCP 支持、可 resume。适合给商家搭"托管 AI 员工"，做订阅制收费。

## 对接/接单要点
- **卖铲子定位**：别自费买这三家 API 给自己用；帮商家封装成 MCP/业务工具/托管代理，API 成本转嫁（客户自理或 +20% 管理费），收搭建费+维护费。
- 三家 API 情报、Fiverr Gig 文案、三档报价（约 $200/$600/$1500 + 托管订阅 $200/$500 月）素材在 小G 项目 `ai-agent-api-pack/`（项目目录 项目目录，进度.md 有索引）。
- **价格/地区限制会变**（预览期、免费额度常调整）：对外报价前重验官方定价页，别拿旧数字报价。
- 封装形态优先 MCP server + Agent 工作流组合（参考老王餐厅方案：工具总数 3-4 个、描述 ≤2 行）。
