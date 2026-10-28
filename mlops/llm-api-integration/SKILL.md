---
name: llm-api-integration
description: Use when 对接/封装 LLM 或云 MaaS API（对话/多模态/文生图/视频）。含鉴权坑、冒烟流程。
---

# LLM / 云 MaaS API 对接

用户业务线包含帮商家做 MCP/API 封装与 IT 接单，对接第三方模型 API 是常活。目标：一次拿对，不反复 401。

## 工作流（顺序执行）
1. **先读官方 API 文档再写代码**：GitHub README 的 doc/ 目录、云平台帮助文档——记死 5 项：Base URL、端点路径、模型名、协议（OpenAI 兼容?流式?）、鉴权方式。文档常藏在 README「最新动态」里（上线公告会给入口链接）。
2. **写最小客户端**：requests 或官方 SDK；key 走环境变量/参数，**绝不硬编码进文件**。客户端含：请求封装、输出解析、会话重置。
3. **冒烟测试逐级验证**：纯文本 → 单模态（一帧图/一张图）→ 多模态/批量 → 会话场景。每级过了再进下一级。
4. **失败先读服务端错误 body**：HTTP 状态码只是入口，错误体的 message 常直接点名原因（key 前缀、参数名、配额）。curl 打原始请求看完整返回，别只看 401 就换 key。
5. **没有 key 时**：代码本地逻辑测试（py_compile + 解析函数单测）可做，真实调用必须标注「待实测」；向用户要 key 时说明正确获取路径（控制台入口 + 前置条件，如实名/余额），并提示从哪复制。

## 鉴权坑（最贵的教训）
- **LiteLLM 网关的虚拟 key 以 `sk-` 开头**：网关会直接报 "LiteLLM Virtual Key expected... expected to start with 'sk-'"——按它说的格式找正确凭证，不要试图硬试。
- **云平台常有两套 key**：订阅套餐专属 key（如某平台 Token Plan 的 `pk-` 前缀，文档注明"仅供 XX 专属调用"）与平台通用 API-KEY（`sk-`）。发错网关 = 401，且两套 key 的用途文档写得很明确——先查文档确认哪个 key 配哪个 endpoint。
- **OpenAI 兼容 ≠ 完全一致**：可能要求额外 header（会话隔离、系统提示选择、供应商特定字段）。把官方 curl 示例的每个 header 都搬进客户端。
- 用户直接发来的 key 先验证格式（前缀/长度），不符就反馈服务端报错原文，别猜。

## 会话与输出
- **会话隔离**：多客户/多场景用会话 ID header 隔离，不传常共享 default 会话导致状态串台；换场景必须重置会话（重置端点）。
- **输出归一化**：实时交互类模型常输出标记（如 `</silence>` 沉默 / `</response> 一句话` 回复）——解析规则以官方文档为准，客户端要解析而不是透传。
- 部分模型支持批量帧 + 时间范围参数（frame_time_ranges），用于"两帧之间发生了什么"类问题。

## 已验证：硅基流动视觉 API（2026-10-16 实测通过）
- **base_url**: `https://api.siliconflow.cn/v1`，端点 `/chat/completions`（OpenAI 兼容），鉴权 `Authorization: Bearer <sk-...>`。
- **可用视觉模型**（/v1/models 列表过滤 VL/vision）：`Qwen/Qwen3-VL-32B-Instruct`、`Qwen/Qwen3-VL-8B-Instruct`、`Qwen/Qwen3-VL-30B-A3B-Instruct`、`Qwen/Qwen3-VL-32B-Thinking` 等。
- **图片传法**：base64 后 `{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,<b64>"}}` 混入 content 数组，同轮可带 text 指令；`max_tokens` 控制输出长度。
- **实测结果**：分析 405×720 JPEG 封面返回详细中文描述（画质/色调/风格/构图），无权限限制。key 存 `~/.hermes/agent-memory-data/backup.env` 的 `SILICONFLOW_API_KEY`。
- **长分析要拆问**：一次问 6 个维度（内容/画质/色调/风格/构图/复刻特征）时 max_tokens=1200 会被截断在中间，后半段丢失——拆成两次调用（第一次内容+画质，第二次色调/氛围/构图/复刻特征），或加大 max_tokens。
- **偶发读超时**（`The read operation timed out`）：大图/长 prompt 时出现，调用侧 timeout 设 150-200s。**大图先压缩再传**（≥1MB 的 PNG 直接 base64 必超时，实测 1.8MB PNG 首调即 timeout；先用 PIL 缩到宽 ≤800 + JPEG q85 再 base64，`try import PIL except: 原图直传`）——压缩后首次调用通常即成功。**若 ≤800px 压缩后仍连续超时（重试同参数无效）**：别再同参数重试，进一步缩到宽 ≤512 + JPEG q80、timeout 拉满到 300s——实测 880×1184 图 800px 两次超时、512px+300s 一次成功；超时是带宽/服务端慢，不是参数错，变小 payload 是唯一有效解。输出先写文件再读回，避免截断吞掉完整结果。
- **对比坑**：火山方舟 doubao-vision 模型列表可见但调用全 404 `InvalidEndpointOrModel.NotFound`（账号未开通视觉模型权限）——列表能看到 ≠ 能调用。
- **内置 vision_analyze 工具也走火山 doubao**：图片分析直接调它常 404 `UnsupportedModel`（不支持的模型/未开通权限）——**图片/海报分析直接用硅基流动 Qwen3-VL 脚本**（`scripts/visual_review.py <图路径> [问题]`，默认问题覆盖 pic 系列复核 6 项），不要在 vision_analyze 上耗时间。

## 参考资料
- `references/joyai-vl-interaction.md`：京东开源实时视频交互模型 API 详情（端点/key 坑/会话/输出），项目代码在 ~/项目目录/projects/joyai-vl-api/。
