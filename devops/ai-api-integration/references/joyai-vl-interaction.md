# JoyAI-VL-Interaction（京东云 MaaS）对接速查

- 定位：京东探索研究院开源 8B 实时视频交互模型（Apache-2.0，模型/数据/训练配方/系统全开源，全球首个全栈开源 interaction 模型）。
- API 托管：京东云 JoyBuilder MaaS，已上线（OpenAI Chat Completions 兼容）。
- Key：注册京东云 → JoyBuilder MaaS → Get API Key（docs.jdcloud.com/cn/jdaip/Get API-Key）。

## 接口速查
| 项目 | 值 |
|---|---|
| Base URL | `https://joyrouter.jd.com` |
| 聊天端点 | `POST /v1/chat/completions` |
| 会话重置 | `POST /v1/streaming/reset?model=JoyAI-VL-Interaction` |
| 模型名 | `JoyAI-VL-Interaction` |
| 协议 | OpenAI Chat Completions 兼容，同步 JSON，**不支持流式** |
| 鉴权 | `Authorization: Bearer $JOYAI_API_KEY` |

## Headers
- `x-streaming-session`：会话隔离（字母数字`._-`，≤120 字符，不传=共享 default 串台）。
- `x-system-prompt-key`：`DEFAULT_SYSTEM_PROMPT_EN`（带后台委派）/ `DEFAULT_SYSTEM_PROMPT_NO_DELEGATION`。
- `x-frame-time-range`：单帧时间范围，如 `"10.0 seconds ~ 12.0 seconds"`。

## Body / 输入
- `messages`：OpenAI 标准结构，最后一条 user 消息**文本=用户问题**（传空文本=主动交互，模型自主决定说不说）。
- 图片：content 数组多个 `{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,..."}}` = 批量帧。
- `frame_time_ranges`：批量帧时间范围数组，与图片一一对应。
- `max_tokens` / `temperature` / `top_p`：常规采样参数。

## 输出归一化（关键）
- `</silence>` → 沉默；`</response> 一句话` → 回复（取第一行）。
- 原始输出在 `streamingharness.raw_content`；延迟在 `streamingharness.timing.adapter_total_ms`。
- 会话 ID 优先级：`x-streaming-session` > `x-session-id` > body `user` > `default`。

## 能力与评测口径
- 能力：监控预警（火灾/摔倒/红牌）、实时计数（健身/飞镖）、实时翻译、实时解说、APP 引导、后台 Agent 委派（OpenClaw/Claude Code 桥接）；离线视频理解 26 benchmark 平均领先 Qwen3-VL-8B 3.2 点。
- 人评胜率：豆包 77.6% / Gemini 87.9%（**窄场景**）；弱项：超长记忆 30%、视觉触发指令遵循 40%；官方局限声明：豆包/Gemini 更大，长尾闲聊难超越。对外不吹过头。

## 接单场景
- 门店/仓库监控预警（摔倒、烟火、异常闯入）→ "AI 替你盯，出事秒级喊你"。
- 健身/训练计数 → 手机/摄像头对着人自动数动作。
- 直播实时解说/翻译（球赛、游戏、跨境字幕）。
- 报价参考：POC 1-3k；持续监控告警系统 5-15k（按路数）；API 费客户自理或 +20% 管理费。

## 自部署（客户要私有化时）
- 官方给 RTX 3090/5090 调优配置 + INT4/INT8/FP8/NVFP4 量化版（HF：jdopensource/JoyAI-VL-Interaction-*）。
- 系统 5 服务：vLLM + webinfer(:8070) + webui(:8099) + ASR(:8994) + TTS(:8992) + background-agent(:8079)。
- vLLM-Omni day-0 支持（recipes/JD/JoyAI-VL-Interaction.md）。

## 实测状态（2026-10-13）
- 代码就绪：`~/项目目录/projects/joyai-vl-api/`（joyai_vl_client.py + demo_stream_watch.py + README.md），本地语法+逻辑测试通过。
- 待 Key 实测：用户注册京东云拿 JOYAI_API_KEY 后跑冒烟（纯文本 + 一帧图 + 视频抽帧推流），测 silence/response 与 timing。
