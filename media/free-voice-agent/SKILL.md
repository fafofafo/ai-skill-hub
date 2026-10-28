---
name: free-voice-agent
description: Use when 0 成本搭语音客服/Agent。含 edge-tts、faster-whisper 排障。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [免费, 语音, TTS, STT, edge-tts, whisper, 语音客服, 接单]
---

# 免费语音 Agent 方案（0 成本）

用全免费组件搭一套可接单演示的语音客服/语音对话 Agent：**edge-tts（微软免费 TTS）+ faster-whisper（本地免费 STT）+ DeepSeek（低价 LLM）**，全程零订阅费。

## When to Use
- 用户要"免费的语音方案 / 语音客服 / 语音对话机器人"，不想为 TTS/STT 付月费。
- 接单演示"AI 语音能力"（客服/问答/外呼），成本接近 0。
- 火山豆包免费额度（2万字符）用完后不想转付费（$3/万字符）时的回退方案。

## 组件总览
| 组件 | 方案 | 成本 | 说明 |
|---|---|---|---|
| TTS | edge-tts（微软） | 免费无限 | 中文多音色（晓晓/云希/云健等），Hermes 默认 provider |
| STT | faster-whisper（本地） | 免费 | 离线识别，CPU 可跑，whisper-small 够用 |
| LLM | DeepSeek / 硅基流动 | 极低 | 用户已有 key，零额外成本 |
| 备选 TTS | 火山豆包 2.0 | 2万字符/半年免费 | 60+音色+情绪指令，超额度 $3/万字符 |

## 免费 TTS：edge-tts（已配好，2026-10-15）
```bash
# provider 已切 edge，音色晓晓：
hermes config set tts.provider edge
hermes config set tts.edge.voice zh-CN-XiaoxiaoNeural
```
常用中文音色（`edge-tts --list-voices | grep zh-CN`）：
- `zh-CN-XiaoxiaoNeural` 晓晓（女，自然，默认）
- `zh-CN-XiaoyiNeural` 晓伊（女）
- `zh-CN-YunxiNeural` 云希（男，播音）
- `zh-CN-YunjianNeural` 云健（男，浑厚）
- `zh-CN-YunxiaNeural` 云夏（儿童）
- 广东话：`zh-HK-HiuGaaiNeural` 晓佳

### ⚠️ 关键坑：装错环境导致 403（已实测排掉）
**症状**：CLI 直调 edge_tts 成功，但 Hermes `text_to_speech` 工具报 `403 Invalid response status`。
**根因**：Hermes 网关跑在**独立 venv** `~/.hermes/installs/*/environments/*/venv` 里，不是 `~/.hermes/tools/python-current`。只往 tools 环境装新版本，网关没吃到 → 网关用旧版 edge-tts 7.2.7（微软反爬已拒）→ 403。
**修复**（用 tools pip 以 --target 装进 venv site-packages）：
```bash
VENV_SP=$(ls -d ~/.hermes/installs/*/environments/*/venv/lib/python*/site-packages | head -1)
# 备份旧版
mv $VENV_SP/edge_tts $VENV_SP/edge_tts.bak 2>/dev/null
mv $VENV_SP/edge_tts-*.dist-info $VENV_SP/edge_tts-*.dist-info.bak 2>/dev/null
# 装 7.3.1（微软反爬要求新版本）
~/.hermes/tools/python-current/bin/python3 -m pip install edge-tts==7.3.1 --target $VENV_SP --upgrade
# 验证 + 重启网关
$VENV/bin/python3 -c "import edge_tts; print(edge_tts.__version__)"  # 应显示 7.3.1
sudo systemctl restart hermes-gateway  # 从网关外派发，勿在网关内直接 restart
```
**判断装错环境的命令**：看网关进程 `ps aux | grep "gateway run"` 的 python 路径，再看那个 python 里 `import edge_tts; print(edge_tts.__file__)` 的版本。

## 免费 STT：faster-whisper（本地）
Hermes `stt.provider` 内置 `local`（faster-whisper，默认免费）与 `local_command`。装依赖：
```bash
VENV=/home/ubuntu/.hermes/installs/*/environments/*/venv
$VENV/bin/python3 -m pip install faster-whisper 2>/dev/null || \
~/.hermes/tools/python-current/bin/python3 -m pip install faster-whisper --target $VENV/lib/python*/site-packages
# 模型：Systran/faster-whisper-small 已缓存（~/.cache/huggingface/hub/models--Systran--faster-whisper-small）
hermes config set stt.provider local
# 模型规格（可选）
hermes config set stt.local.model small  # small/base/tiny，按内存选
```
无 GPU 服务器用 `small`（~460MB 内存常驻）即可，中文识别够用；`tiny` 最快但准确率略低。

### ⚠️ 兼容冲突：PyAV 19 移除 metadata_errors 参数（两种修法，首选降级）
**症状**：`faster_whisper` 加载音频报 `TypeError: open() got an unexpected keyword argument 'metadata_errors'`。
**根因**：faster-whisper 1.2.1 的 `audio.py` 用 `av.open(..., metadata_errors="ignore")`，但 PyAV 19.x 已移除该参数。
**修法一（首选，一条命令，不碰源码）**：
```bash
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python "av<19"   # 实测 18.1.0 正常
```
**修法二（版本不能动时）**：给 `$VENV/lib/python*/site-packages/faster_whisper/audio.py` 的 `decode_audio` 打补丁——解码循环提为内部 `_decode()`，外层先试带 `metadata_errors`，`TypeError` 时降级为不带参数的 `av.open()`。只改 site-packages，别改 Hermes 主代码。

### ⚠️ faster-whisper 会被 Hermes 升级清掉（重装命令）
Hermes 升级/重装会清非项目依赖，`import faster_whisper` 报 `ModuleNotFoundError` 就重装进 hermes venv（走腾讯镜像，别直连 pypi）：
```bash
UV_DEFAULT_INDEX=https://mirrors.cloud.tencent.com/pypi/simple \
  uv pip install --python ~/.hermes/hermes-agent/venv/bin/python faster-whisper
```
首次加载模型同时**走镜像 + 关掉 xet**（否则 hf 直连卡死）：
```bash
HF_ENDPOINT=https://hf-mirror.com HF_HUB_DISABLE_XET=1 python3 stt.py
# WhisperModel("small", device="cpu", compute_type="int8")
```
无 GPU 服务器 small+int8 实测中文秒级出稿，十几秒短视频够用。

## 组合：语音客服 Agent
- TTS=edge-tts 出口；STT=local 入口；LLM 走用户现有 DeepSeek key。
- Hermes 本身是多平台 Agent（企微已接），套上语音组件即：语音问答/客服/外呼演示。
- 接单话术："全免费组件搭语音客服，零月费"——低成本是差异化卖点。

## Pitfalls
- **edge 403**：几乎都是版本问题——微软反爬只认新版 edge-tts（≥7.3），且必须装进 Hermes 的 venv 而非 tools 环境。
- **网关重启**：一机一网关 systemd 管理，`sudo systemctl restart hermes-gateway` 最稳；从网关内部调用会被拒（SIGTERM 传播），用 `ssh -f localhost 'bash /tmp/x.sh'` 派发脚本到独立 shell。
- **火山免费额度**：2万字符半年，超了自动转后付费 $3/万字符——量大的话免费方案优先 edge。
- **free-voice-agent 与 douyin-voice 的关系**：douyin-voice=火山豆包专项（60+音色+情绪指令，要 key）；本技能=全免费方案（无 key）。按成本/需求选。
