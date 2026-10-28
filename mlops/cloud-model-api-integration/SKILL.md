---
name: cloud-model-api-integration
description: Use when 对接云厂商大模型API做接入/凭证/冒烟/鉴权排障。含多套凭证与网关坑。
---

# 云厂商大模型 API 对接

## 接入流程（按序）
1. **官方 API 文档优先**：确认 Base URL / 端点 / 协议（是否 OpenAI Chat Completions 兼容）/ 鉴权头 / 模型名 / 是否支持流式。文档在 GitHub 仓库 doc/ 目录的常是最新（如 jd-opensource 的 doc/api.zh-CN.md），比平台产品页更具体。
2. **凭证来源确认**：记录 key 是从哪个平台菜单/套餐拿的，以及文档对该凭证用途的原文说明——云厂商常有多套凭证，拿错一套必然 401。
3. **最小冒烟**：纯文本请求 → 带图/批量 → 业务场景（如监控循环）。冒烟请求体照抄官方示例，先验证通路再改参数。
4. **客户端封装**：写成项目目录下的可复用客户端（会话 ID、输出归一化解析、抽帧工具等），Key 用环境变量，绝不硬编码进文件；本地用 mock 测纯逻辑（输出解析/参数拼装），网络部分标「待 Key 实测」。

## 鉴权排障（重要）
- **401 先读服务端响应 body**：网关（尤其 LiteLLM 系）的错误 JSON 会直接告诉你凭证格式要求（实测：`LiteLLM Virtual Key expected... expected to start with 'sk-'`）。先看 body 再怀疑 key 失效/网络/账号——服务端鉴权报错是最高权威，胜过任何文档推断。
- **云厂商多套凭证是常态**：京东云为例——订阅套餐专属 key（Token Plan 个人版「专属 APIKEY」，`pk-` 开头）仅供该套餐自己的 BaseURL，文档明说不能用于平台其他模型 API；官方托管网关（joyrouter.jd.com 等 LiteLLM 网关）要平台通用 API-KEY（JoyBuilder 2.0 控制台 → API-KEY 创建，`sk-` 开头虚拟 key）。先分清「你手里的 key 是给哪个入口的」。
- **API-KEY 创建前置条件常被忽略**：实名认证 + 账户余额校验（后付费模型服务，如京东云要求余额>50元）。指引用户时提前说明，避免用户白跑一趟。
- **文档可能滞后**：GitHub 文档给的入口/Key 获取位置可能过期，以服务端实际校验结果为准（401 body 会纠偏）。

## 边界
- 延迟/成本/稳定性调参（DeepSeek/火山）见 `deepseek-api-usage`；本技能管接入与凭证。
- 本地推理/部署类见 `local-decision-models`/`llama-cpp`；本技能管托管 API。

## 已知实例速查
- **京东云 JoyAI-VL-Interaction**：OpenAI 兼容、同步 JSON 不支持流式、`x-streaming-session` 会话隔离、输出归一化 `</silence>`/`</response>`、批量帧+`frame_time_ranges`。客户端与方案：`~/项目目录/projects/joyai-vl-api/`（README + joyai_vl_client.py + demo_stream_watch.py）。
