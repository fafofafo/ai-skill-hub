---
name: douyin-voice
description: Use when 要接入火山豆包语音 TTS/STT 或合成中文语音。含插件安装、key、补丁、排错。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [火山, 豆包, doubao, volcengine, tts, stt, 语音合成, 情绪指令]
---

# 火山豆包语音（douyin-voice / volcengine-voice）

把火山引擎豆包语音接到 Hermes Agent 的完整指南。TTS（语音合成）+ STT（语音识别）双能力，60+ 中文音色、情绪指令、方言、说话人区分。

## When to Use
- 用户要"用火山/豆包语音"、"换语音引擎"、"合成中文语音"、"TTS 带情绪"。
- Hermes TTS 需要国内可达、音色丰富、带情绪控制的方案（替代 Kitta/Fish Audio 等）。

## 架构（为什么是插件 + monkey-patch）
- 插件：`~/.hermes/plugins/volcengine-voice/`（GitHub: linxichen/hermes-volcengine-voice）。
- 原理：monkey-patch 拦截 Hermes `tools/tts_tool.py` 的 `text_to_speech_tool` 和 `tools/transcription_tools.py` 的 `transcribe_audio`，当 `tts.provider == "volcengine"` 时路由到火山 API，否则走原逻辑。
- 插件不注册新工具，而是替换现有工具函数引用 → LLM 无需学习新工具名。

## 安装（GitHub 被墙时走镜像）
```bash
# 直连失败（TLS 被掐）时用 ghfast.top 镜像：
git clone --depth 1 https://ghfast.top/https://github.com/linxichen/hermes-volcengine-voice.git ~/.hermes/plugins/volcengine-voice
# 或 hermes plugins install linxichen/hermes-volcengine-voice（需网络可达）
```

## 启用与配置
```bash
# 1. 修 plugin.yaml：kind 必须是合法值（backend/exclusive/model-provider/platform/standalone）
#    原版写 kind: provider 是无效值 → 改成 kind: standalone（否则每轮加载打 WARNING）

# 2. 启用插件（热加载，日志见 patched text_to_speech_tool ← volcengine provider）
hermes plugins enable volcengine-voice

# 3. 写 key 到 ~/.hermes/.env（插件读 os.getenv("VOLCENGINE_VOICE_API_KEY")）
echo 'VOLCENGINE_VOICE_API_KEY=<语音专用key>' >> ~/.hermes/.env

# 4. 切换 provider（用 hermes config set，勿手改 config.yaml）
hermes config set tts.provider volcengine
hermes config set tts.volcengine.speaker zh_female_shuangkuaisisi_uranus_bigtts

# 5. 重启网关：systemd 环境直接
sudo systemctl restart hermes-gateway   # 一机一网关，勿用 hermes gateway restart（root 权限检查会卡）
#    若旧网关非 systemd 托管，用切换脚本 ssh -f localhost 派发（脚本内 sleep 150s 等当前回复送达再杀旧网关）
```

## Key 获取（关键坑）
- **必须用语音专用 key，不能复用方舟 Ark LLM key**。Ark key（前缀 `ark-`）调语音端点返回 `401 Invalid X-Api-Key`（code 45000010）。
- 获取：火山控制台 https://console.volcengine.com/speech/new/overview?projectName=default → 登录（手机号）→ 一键开通豆包语音服务（新用户送免费礼包）→ 左侧「API Key 管理」→ 创建 API Key。
- 免费额度：豆包语音合成 2.0 = **20000 字符，半年有效**（后付费 3 元/万字符；资源包 10 万字 28 元）。

## API 要点
- 端点：`POST https://openspeech.bytedance.com/api/v3/tts/unidirectional`
- 认证：`X-Api-Key` + `X-Api-Resource-Id: seed-tts-2.0`
- **请求体必须是嵌套格式**（踩坑）：
```json
{"user":{"uid":"hermes-agent"},"req_params":{"text":"...","speaker":"zh_female_shuangkuaisisi_uranus_bigtts","audio_params":{"format":"mp3","sample_rate":24000}}}
```
- 平铺格式（`{"voice_type":...}` 等）会报 `55000000 resource ID is mismatched with speaker related resource`。
- 响应是 NDJSON 流：每行 `{"code":0,"data":"<base64音频块>"}`，最后 `code:20000000` 为 OK；逐行 base64 解码拼接成 mp3。
- 错误 `45000030 requested resource not granted` = 该 resource/音色未开通，需回控制台开通。

## 音色预设（短名 → voice_type）
| 短名 | voice_type | 描述 |
|---|---|---|
| zh_female_conversation | zh_female_shuangkuaisisi_uranus_bigtts | 爽快思思 2.0（默认） |
| zh_female_gentle | zh_female_vv_uranus_bigtts | Vivi 2.0 温柔女声 |
| zh_female_sweet | zh_female_tianmeixiaoyuan_uranus_bigtts | 甜美小源 2.0 |
| zh_male_ruya | zh_male_ruyayichen_uranus_bigtts | 儒雅逸辰 2.0（男声） |
| zh_male_conversation | zh_male_M392_conversation_wvae_bigtts | 对话男声（1.0，resource 用 seed-tts-1.0） |

## 情绪指令（仅 2.0 音色）
- 文本开头加 `[开心] [伤心] [生气] [严肃] [温柔] [快速]` 等标记，可叠加 `[开心][快速] 你好`。
- 标记经 `context_texts` 字段传给火山，**不计费**；正文方括号（引用/链接）原样朗读。
- 实现：`tts.py` 的 `extract_emotion_and_clean_text()` 剥离标记 → `_as_instruction()` 包装成"用X的语气说"。
- 不同音色响应差异大：Vivi 响应明显，有些音色几乎无感，需实测。

## 兼容补丁（Hermes v0.22，必须打）
原版插件 patch 函数签名 `(text, output_path=None)` 不接收 Hermes 新版的 `speed`/`instructions`/`provider` 参数，调用即报 `TypeError: patched_text_to_speech() got an unexpected keyword argument 'speed'`。

修复（`__init__.py` 的 `register()` 内）：
1. `patched_text_to_speech` 改为完整签名 `(text, output_path=None, speed=None, instructions=None, provider=None)`。
2. 非 volcengine 分支：`return _original_tts(text, output_path, speed=speed, instructions=instructions, provider=provider)` 透传。
3. 顶部加 `from typing import Optional`。
4. `tts.py` 的 `_volcengine_tts` 加参数 `speed_ratio: float | None = None`，payload 加 `if speed_ratio is not None: payload["req_params"]["speed_ratio"] = float(speed_ratio)`（Hermes speed 0.25-4.0 直接映射）。

## 验证
```bash
# 独立环境测插件函数（不依赖网关）：模拟 hermes_plugins 命名空间 + 设 env + importlib 加载 tts.py，调 _volcengine_tts
# 网关内验证：调 text_to_speech 工具，返回 provider: volcengine 即成功
```
- 网关日志应出现：`volcengine-voice: patched text_to_speech_tool` / `patched transcribe_audio` / `registered pre_llm_call hook`。

## STT（可选）
- 配置 `hermes config set stt.provider volcengine` 即可切火山 ASR（WebSocket 流式，支持方言、说话人区分），key 与 TTS 通用。
- 当前主服 stt 未配置段，走 Hermes 自动检测（本地 faster-whisper 优先）。

## Pitfalls
- **别用 ark key**：401 Invalid X-Api-Key，语音要专用 key。
- **别用平铺 JSON**：55000000 mismatched，必须 `req_params.speaker` 嵌套。
- **别手改 config.yaml**：用 `hermes config set`。
- **网关重启**：systemd 一机一网关，`hermes gateway restart` 会撞 root 权限检查；`sudo systemctl restart hermes-gateway` 最稳；旧网关非托管时用切换脚本 + `ssh -f localhost` 派发避免自杀。
- **切换脚本的坑**：脚本最后 `hermes gateway run` 会被 systemd 拦截（"already running under systemd"），但旧网关已死 → systemd auto-restart 会拉起新进程，等 30s 后插件代码已是新版，无需手动再起。
- **免费额度**：2 万字符半年，超了自动转后付费（3 元/万字符），量大会花钱，注意用量。
- **插件升级覆盖补丁**：hermes update / 插件重新 clone 会覆盖 `__init__.py` 补丁，升级后按上述补丁语义重打。
