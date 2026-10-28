# JoyAI-VL-Interaction（京东开源实时视频交互模型）API 对接

- 客户端/README/监控 demo：`~/项目目录/projects/joyai-vl-api/`（joyai_vl_client.py 本地逻辑测试已过）
- 网关：`https://joyrouter.jd.com`，OpenAI Chat Completions 兼容，**同步 JSON 不支持流式**
- 端点：`POST /v1/chat/completions`；会话重置 `POST /v1/streaming/reset?model=JoyAI-VL-Interaction`
- 模型名：`JoyAI-VL-Interaction`（8B 视觉语言交互模型）
- 鉴权：`Authorization: Bearer <sk-开头的 key>`
- 关键 header：
  - `x-streaming-session`：会话隔离（字母数字._-，≤120 字符；不传共享 default 会串台）
  - `x-system-prompt-key`：`DEFAULT_SYSTEM_PROMPT_EN`（带后台委派）/ `DEFAULT_SYSTEM_PROMPT_NO_DELEGATION`
- 图片输入：`content` 数组 `image_url` + data URL；批量帧用 body `frame_time_ranges`（如 `"10.0 seconds ~ 11.0 seconds"`）与图片一一对应
- 输出归一化：`</silence>`（沉默）| `</response> 一句话`（回复，取第一行）；原始输出在 `streamingharness.raw_content`，时序在 `streamingharness.timing`

## Key 获取坑（实测 401）
- 用户给的 `pk-` 开头 key 是京东云 **Token Plan 专属 APIKEY**（文档原文：仅供 Token Plan 专属调用，无法用于 JoyBuilder 平台其他模型 API）——喂给 joyrouter 网关被拒
- 服务端报错原文：`LiteLLM Virtual Key expected. Received=pk-…, expected to start with 'sk-'`
- 正确来源：京东云 **JoyBuilder 2.0 控制台 → API-KEY**：`https://joybuilder-console.jdcloud.com/system/api-key/list` 创建（要求实名认证 + 账户余额 > 50 元，后付费）
- 官方 API 文档：`github.com/jd-opensource/JoyAI-VL-Interaction` 的 `doc/api.zh-CN.md`

## 应用场景（接单弹药）
门店/仓库监控预警、健身计数、直播实时解说/翻译、APP 引导。API 模式零 GPU 成本；自部署需 RTX 3090+ 另案。
