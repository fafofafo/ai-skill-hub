---
name: free-claude-code-fcc
description: "Use when 安装/运维 FCC 免费模型网关或给 Hermes profile 接 FCC 通道。"
version: 1.0.0
author: Hermes
tags: [fcc, free-claude-code, model-gateway, provider, agnes, deepseek]
---

# free-claude-code (FCC) 网关接入 Hermes

## 是什么
FCC 是本地模型路由网关：把 Claude Code/Hermes 等 12 种编码工具接到 61 家模型的免费/付费额度，额度用完自动切换 fallback。仓库 `Alishahryar1/free-claude-code`（★63.8k）。非破解，遵守各平台条款。

## 关键事实（2026-10-27 实测）
- 版本 6.18.1，要求 **Python ==3.14.9**（uv 可自动装，`uv python install 3.14.9`）
- 服务端口 **8082**（env PORT 可改）；本地代理端点：`/v1/responses`(OpenAI Responses)、`/v1/messages`(Anthropic)、`/v1beta/models`、`/health`；**无 /v1/chat/completions**
- 配置目录 `~/.fcc/.env`（provider key 放这里，权限 600）；Admin UI `http://127.0.0.1:8082/admin`（仅本机）
- provider 识别：`.env` 里有对应 `*_API_KEY` 即启用（DEEPSEEK/AGNES/OPENROUTER/GROQ/NVIDIA_NIM...）
- 免费模型：**agnes/agnes-2.5-flash 等**（配 AGNES_API_KEY，key 在 ~/.hermes/.env 有）；DeepSeek 需余额否则 402
- 模型枚举：`GET /v1/models`（200）；管理 API `GET /admin/api/models`
- 上游 402=key 余额不足；503=对应 key 未设置
- **网关层无默认模型**：`/v1/responses` 缺 `model` 字段直接 400（Field required），模型必须由客户端 profile 显式指定；「FCC 默认模型」= 各 profile 的 model.default

## 安装（GitHub 被墙走镜像）
```bash
git clone --depth 1 https://ghfast.top/https://github.com/Alishahryar1/free-claude-code /tmp/fcc
uv python install 3.14.9   # uv<0.13 无此版本下载，先 uv self update
cd /tmp/fcc && UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv tool install --python 3.14.9 --editable . --refresh
# 腾讯云镜像 mirrors.tencentyun.com 部分 wheel 下载慢/失败，清华镜像更稳
```
装完 `~/.local/bin/fcc-server` + fcc-hermes 等 17 命令。**不要用 install.sh**（会顺带装 9 个 agent CLI）。

## 配置 provider
```bash
mkdir -p ~/.fcc && chmod 600 ~/.fcc/.env
# 从 ~/.hermes/.env 提取 key 写入 ~/.fcc/.env：DEEPSEEK_API_KEY / AGNES_API_KEY ...
# 重启服务后生效
```

## 接 Hermes（独立 profile，2026-10-27 实测可用）
```bash
hermes profile create fcc --description "FCC 免费模型通道"
hermes -p fcc config set model.provider "custom:custom"
hermes -p fcc config set model.default "agnes/agnes-2.5-flash"
hermes -p fcc config set model.base_url ""
hermes -p fcc config set model.api_key ""
hermes -p fcc config set model.api_mode "codex_responses"
hermes -p fcc config set providers.custom.transport codex_responses
hermes -p fcc config set providers.custom.api "http://127.0.0.1:8082/v1"
hermes -p fcc config set providers.custom.default_model "agnes/agnes-2.5-flash"
hermes -p fcc config set providers.custom.discover_models false
```
**坑**：只设顶层 model.api_mode 不够，Hermes 仍发 /v1/chat/completions 404；必须加 providers.custom.transport + model.provider 用 `custom:custom` 引用 providers 段。

测试：`hermes -p fcc chat -q "执行 date 命令并告诉我时间"`（验证对话+工具调用）。

## 状态（2026-10-27 晚）
- fcc / workfcc 测试 profile **已删除**（备份 `~/.hermes/_deleted_profiles/fcc_20261027_154318.tar.gz`、`workfcc_20261027_154318.tar.gz`，可随时恢复）
- FCC 网关（fcc-server :8082）**保留运行**；需要时按上节命令重建 profile 即可
- workbuddy 本体曾临时切 FCC 免费链测试（备份 `scratch/workbuddy_config_bak_fcc_20261027.yaml`），**恢复 PlanC 原链后**才算完全还原

## 用生产角色测 FCC（克隆 or 本体，workfcc/workbuddy 实测）
用户说「用某生产 role/profile 测这条链」时**先确认克隆还是本体**：克隆零破坏（workfcc），但实测用户说「用 workbuddy 角色测」指的是**本体直接切**——别自作主张克隆，先按用户原话走。

### 克隆路径（零破坏，适合长期对比）
用户说「用某生产 role/profile 测这条链」且可接受克隆时，克隆角色到测试 profile：
```bash
hermes profile create <test> --clone-from <生产profile> --description "<角色> · FCC免费链测试"
# 然后按上节命令把模型切到 FCC（custom:custom + codex_responses + 127.0.0.1:8082）
```
必做四步（缺一步就踩坑）：
1. **清空克隆来的 fallback_providers**（`hermes -p <test> config set fallback_providers '[]'`）——`--clone-from` 会把生产 key 的 fallback 链一起复制，不清则 FCC 挂时静默回落生产配额，测试不纯净还白烧生产 token
2. **patch SOUL**：标题加「测试」标注 + 模型切换规则段整段替换为「固定走 FCC、无 fallback、不静默切换」（源 SOUL 的切换规则会按旧链切 key）
3. **记忆重写最小测试版**（身份+硬约束+模型说明；沿用「克隆不复制记忆」硬性规则，克隆来的 MEMORY.md/USER.md 含生产积累必须覆盖）
4. **实测验收**：`hermes -p <test> chat -q "执行 date 命令告诉我当前时间，然后自我介绍：你是谁、模型走的什么通道"`——三项全验：工具调用 OK + 角色自称引用 SOUL + 通道认知正确（说出 FCC/agnes）

### 本体切换路径（用户点名某生产 profile 本体，2026-10-27 workbuddy 实测）
1. **备份**：`cp <p>/config.yaml <scratch>/<p>_config_bak_fcc_<日期>.yaml`（含原链+fallback）
2. `config set` 切 FCC（命令同上节）
3. **patch 删 `fallback_providers`**（备份里留原链；不删则 FCC 挂时静默回落生产配额）
4. **patch SOUL「模型切换规则」段**：标注「临时 FCC 测试中 + 恢复预案」（不 patch 则 bot 认知错位——自称旧通道 Plan C，fallback 行为也按旧链）
5. **验证**：新会话 `chat -q "你现在模型走什么通道？主模型？fallback？"`——必须说出 FCC/agnes/无 fallback；认知错位=SOUL 没同步（CLI chat 每次新建会话读新 SOUL，无需重置会话）
6. **测完恢复**：`cp` 备份回 config.yaml + 还原 SOUL 规则段
切换后该 profile 的企微新消息也走新链——测试期间别派生产任务。

## systemd 托管（开机自启+崩溃重启）
service 文件见 `~/.config/systemd/user/fcc-server.service`；EnvironmentFile=%h/.fcc/.env。
```bash
systemctl --user daemon-reload && systemctl --user enable --now fcc-server
curl -s http://127.0.0.1:8082/health  # {"status":"healthy"}
```
**坑**：systemd 环境干净，`.env` 里缺 key 会导致 503（手动启动时 shell 环境有 key 掩盖了问题）；改 .env 后必须 `systemctl --user restart fcc-server`。

## fallback 链
`hermes fallback add` 是**交互式选择器**（无位置参数），无头环境会直接报 `unrecognized arguments` —— 改用 `config set` 写 JSON 数组（数组顺序即优先级），再回读验证：
```bash
hermes -p fcc config set fallback_providers '[{"provider": "custom:custom", "model": "deepseek/deepseek-flash"}]'
hermes -p fcc fallback list   # 验证链：Primary + fallback 顺序
```
fallback 目标必须走同一 FCC provider（`custom:custom`），模型 id 用 FCC 目录里的 wire slug（如 `deepseek/deepseek-flash`）；fallback 前先确认该 provider 的 key 有余额，否则备档静默失联。

## 免费模型的真实身份与预期
- Agnes 系列是免费第三方模型（自称 Sapiens AI），**不是 Claude**：能力/行为与 Claude 不同，别拿 FCC 免费通道当 Claude 用；验收标准 = 对话 + 工具调用（如 `hermes -p fcc chat -q "执行 date 命令并告诉我时间"`）都能完成
- 免费可用与否看 provider key 余额：DeepSeek 官方 API key 无余额即 402（区别于 ark 三池）；诊断上游 402 直接看 error.message，别猜
- **同任务 A/B 质量结论（agnes-2.5-flash vs deepseek-v4-flash）**：agnes 能完成中等任务（写脚本）但明显低一档——首轮语法错误（能自修）、缺大小换算/权限处理/CSV 截断/扩展名不归一化；deepseek 一次通过且更鲁棒。pic/mv 技能的可执行性：确定性流程（ffmpeg/脚本/API）agnes 工具调用没问题，纯语言环节（提示词模板）也能遵循（picbpnew 实测模板全对）；适合零成本轻量任务，生产主力留 deepseek

## 运维速查
- 日志：`journalctl --user -u fcc-server -n 50`；请求日志 ~/.fcc/logs/fcc-server.log
- 503 诊断：直接 curl `/v1/responses` 看 error.message 缺哪个 key
- 服务重启：`systemctl --user restart fcc-server`
- 内存：fcc-server 常驻 ~120MB
- **停服务用 pgrep 拿 PID 再 kill，别用 `pkill -f fcc-server`**：`-f` 匹配完整命令行，会连正在执行这条命令的 shell 一起杀掉（命令串里含同样字样）——同一教训适用于任何用 `nohup … &` 或 `bash -lic …` 启动的后台服务。
