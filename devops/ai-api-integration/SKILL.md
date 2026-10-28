---
name: ai-api-integration
description: Use when 对接/封装 AI 模型为 HTTP API 交付（自研或接单）。出客户端+demo+README 包。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [api, integration, 对接, 接单, delivery, maas]
    related_skills: [deepseek-api-usage, external-content-verification]
---

## When to Use
- 用户指向一个新开源/新发布的 AI 模型，决定"对接/研究怎么用"（首案：京东 JoyAI-VL-Interaction 实时视频交互模型）。
- 接单客户要"给业务加 AI 能力"（监控/视觉/语音/生成），需快速出可交付方案。
- 任何"这个模型能 API 调用吗/怎么接"类问题。

## 路线判定（第一步，先定再动手）
- 默认 **API 优先**：零硬件、分钟级起量、按调用付费。主服无 GPU（3GB 内存）→ 本地部署不可行，API 是唯一轻量路径。
- 自部署仅在：客户明确要私有化 / 客户有卡 / 超高频长期调用。自部署报价另一档（硬件 + 运维 + 多服务复杂度：vLLM/推理/ASR/TTS/agent）。
- **开源模型找厂商云 MaaS**：README 里搜 "Cloud API"/"MaaS"/"一键直达" 链接（如京东云 JoyBuilder MaaS），通常已托管且 OpenAI 兼容。

## 可交付包结构（~/项目目录/projects/<项目名>/）
1. `README.md`：API 速查表（endpoint/鉴权/协议兼容/会话机制/输出归一化/输入格式）+ 对接步骤 + 接单弹药（场景→卖点→话术→报价参考）+ 坑清单 + 待办。
2. `<name>_client.py`：客户端库（核心调用/会话管理/输出解析/便捷循环）。
3. `demo_<name>.py`：可跑 demo，留告警钩子（企微 webhook / 邮件）。
4. 交付前本地验证：`python3 -m py_compile` + 无网络逻辑测试（解析/工具函数）。**没 Key 就标"代码就绪，待 Key 实测"**，不假装对接完成。

## 关键步骤
1. **拉官方 API 文档**：web_extract 拉 GitHub 失败（"Keyless Exa extract failed"）→ `curl -sL` 直接抓 `raw.githubusercontent.com/<owner>/<repo>/main/doc/<file>.md`。
2. **提炼 4 个核心机制**（决定客户端设计）：
   - 协议兼容性（OpenAI Chat Completions？流式支持？同步 JSON？）
   - 会话机制（session header？隔离规则？不传是否共享 default？）
   - 输出归一化（主动交互模型常见 `</silence>` / `</response>` 标记 → 客户端必须有解析层）
   - 输入格式（图片 data URL/批量帧/时间范围参数）
3. **客户端设计要点**：会话 ID 显式传参（不传=共享 default 会串台）；输出解析函数返回 (action, reply)；监控循环留 on_speak 回调。
4. **接单话术**：场景→卖点→话术→报价参考；API 调用费客户自理或 +20% 管理费；POC 1-3k，系统 5-15k（按路数/场景）。

## 坑（接单交付专用）
- **没实测=没对接完**：网络端必须真实调用过才算完成；只有本地逻辑测试 = "就绪待 Key"，如实标注。
- **会话串台是事故**：多客户多 session ID 隔离；换场景必重置（如 POST /v1/streaming/reset）。
- **对客户别吹过头**：媒体宣传的"胜率 XX%"是人评窄场景，官方评测表自带弱项+官方局限声明；对外报价/方案引用打折后的口径。
- **语音不是原生**：VLM 类 API 只出文本，客户要语音播报需外接 TTS/ASR 管道（现有硅基流动 CosyVoice 链路可直接挂）。
- **海外服务器调国内云 API**：先测延迟；客户在国内则无忧。

## 参考
- references/joyai-vl-interaction.md —— JoyAI-VL-Interaction（京东云 MaaS）API 速查 + 接单场景 + 实测状态
- references/frontier-agent-apis.md —— Grok/Muse/Dots 三家 AI 代理产品的 API 接入速查（xAI / Meta Model API / OpenAI Agents API），含"接大脑还是接身体"分辨 + 接单卖铲子要点
