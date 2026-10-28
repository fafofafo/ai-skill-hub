---
name: deepseek-api-usage
description: Use when DeepSeek/火山 ark API 调参优化延迟/成本/稳定性。含实测参数。
---

# DeepSeek / 火山 ark API 使用（2026-09-24 固化，实测）

## 接入形态（Hermes custom provider）
- 火山方舟 ark 作为默认模型：config.yaml provider=custom，base_url `https://ark.cn-beijing.volces.com/api/coding/v3`（Coding Plan 端点），模型当前为 `deepseek-v4.1-flash`
- 模型名/端点/密钥取火山控制台；**改模型前先按「模型名核对」节实测**，别照抄套餐页面的宣传名

## 实测性能（deepseek-v4-flash）
- 单次判断约 **2.35s**（含网络往返）——比本地 Laya（0.34s）慢 ~7x，但能力强
- 结论：**高频小判断用 Laya，深度推理用 deepseek**（成本/速度分轨）

## 调参要点
- **温度**：决策/分类 0-0.3（确定性）；内容创作 0.7-1.0（多样性）
- **max_tokens**：按需截断，长输出分页拉取，避免超时重试
- **超时**：长任务调大 timeout（terminal 或 HTTP 客户端），避免默认短超时中断
- **重试**：遇 429/5xx → 指数退避重试（retry 工具，max_attempts 3-5）

## 成本控制
- 默认 flash 级模型跑日常；需要时单次升级（不全局改配置）
- 批量文本处理：合并请求（一次多段）优于多次调用
- token 预算：长任务先估量，分批+中间摘要

## 模型路由与报错排查
Hermes 主模型带 **fallback_providers**（config.yaml 顶层）：主请求失败自动切备用 provider。
- **本机现行方案：双 ark key（两套火山 Coding Plan 账号）**，主备同端点同模型，切换无感知——比 fallback 到别家省心（别家的余额/模型名/能力都不同，切换会引出新故障面）。
- **fallback 条目支持内联字段**（`hermes_cli/fallback_config.py` 实测）：`provider` / `model` / `base_url` / `api_key` / `key_env`——条目自带 base_url+api_key 就**不必**在顶层 `providers:` 里注册，也不依赖环境变量。
- 配置写法（`hermes config set` 对列表键接受整段 JSON，整体覆盖）：
  ```bash
  hermes config set fallback_providers '[{"provider":"custom","model":"deepseek-v4.1-flash","base_url":"https://ark.cn-beijing.volces.com/api/coding/v3","api_key":"ark-..."}]'
  hermes config set fallback_providers '[]'   # 关掉 fallback
  ```
  写完用 yaml 回读校验（key 打码打印），**改完必须重启网关才生效**：`ssh -f localhost 'bash /tmp/gw_restart.sh'` → 查 `gateway_state.json` 新 pid + 各平台 connected。
- **火山 Coding Plan 会 429 限流**（`AccountRateLimitExceeded: Requests are too frequent`）：全舰队 profile 共用同一 ark key，短时间并发高就触发；**不是额度用尽——Coding Plan 有余额仍会限流**
- **402 误导链**：主 provider 429 重试失败 → 自动 fallback → 若备用通道没余额返回 `HTTP 402 Insufficient Balance`，报错文案像"DeepSeek 欠费"，实际根因是主通道限流 + 备用通道没余额（402 是拒绝请求，不扣费）
- **排查铁律**：看到 402/429 先查 `~/.hermes/logs/errors.log` 完整链路（主 provider 失败原因 → fallback 触发 → 最终错误），别只看最终报错归因
- 缓解：主通道限流 → 舰队任务错峰/降并发；fallback 通道保持有余额的 key；永远救不了就 `fallback_providers: []` 让限流直报主通道（去掉误导）

## 模型名核对（控制台切换 ≠ 配置生效）
用户在控制台把套餐切到新模型（如 V4.1）后，**实际跑的仍是 config 里 `model` 字段写的那个模型**——请求名才是决定项，控制台套餐只决定"能不能用"。改完配置前先用最小请求核实：
```bash
curl -s --max-time 30 -X POST https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions \
  -H "Authorization: Bearer ark-..." -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"hi"}],"max_tokens":1}'
```
- 判据是响应里的 **`model` 字段**（归一后的真实模型名），不是没有报错；同时说明 key 有该模型权限。
- **火山命名规律：请求名带点号、返回名点号转横杠**——`deepseek-v4.1-flash` → 实际 `deepseek-v4-1-flash`；`deepseek-v41-flash` 这类猜名报错，别用。新版本先试「点号版」。
- 主备两把 key 都要各测一次再定稿（备用账号套餐可能是另买的、权限范围不同）。

## 用量 / 套餐限额查询（ark key 查不到，要 arkcli + 登录）
- **ark API key 没有用量接口**：`/api/coding/v3/usage`、`/api/coding/usage`、`/api/v3/usage`、`/dashboard/billing` 实测全 404；`hermes usage` 只认 Codex/Anthropic/OpenRouter 之类额度窗口，custom provider 无数据。
- **官方工具 `arkcli`**（npm `@volcengine/ark-cli`）：`npm config set registry https://registry.npmmirror.com && npm i -g @volcengine/ark-cli@latest`（国内必须换镜像）。
- **它是控制面命令，`--api-key` 不适用**（报 `--api-key only applies to data-plane commands`）→ 必须登录拿控制台身份。
- 无头服务器登录（SSO 无浏览器模式，全流程可跑）：
  1. `arkcli auth login volc-sso --no-browser` → 打印 `authorize_url`（**600 秒有效**）
  2. 把 URL 交用户，在**任意设备浏览器**登录**要查的那个火山账号**并授权 → 页面显示 base64 授权码
  3. `arkcli auth login --no-browser --code <授权码>` 完成；`arkcli auth status` 查登录态
  4. `arkcli usage plan --product coding-plan` → 套餐额度快照（`--product`：agent-plan | coding-plan | agent-plan-team | coding-plan-team；不带则自动发现全部订阅）
- **两个账号要分别登录各查一次**，一个登录态只代表一个账号；查另一个前先 `arkcli auth logout`（或用 `--profile` 分开存）——**logout 会清掉该账号凭证（`identities/volc-<account_id>/`），之后要再查必须重新授权**，别以为登出只是切视图。
- **凭证是持久的，不是一次性**：`~/.arkcli/config.yaml` 每个 profile 带 `expires_at`（实测自登录起约 3 周）+ `plan_tier`，期间 `usage plan` 随时可查，到期再授权一次。被问"这个授权能一直查还是只能查一次"，答"有效期约 3 周、期间随便查"，别答一次性。
- **额度快照三个周期都要看**：`periods` 返回 `session`（约 5 小时滚动）/ `weekly` / `monthly`，各带 `percent` 与 `reset_at`。**周额度是限流先行指标**：实测 weekly 已用 86.5%（月额度才 65%）时 429 频繁出现——额度比并发更可能是主因，此时加账户/换 key 比降并发有效。定期 `usage plan` 留档，别等 429 才查。
- Coding Plan 只有套餐级 quota 快照，**没有按模型的套餐明细**（那是 Agent Plan 才有）；`arkcli usage balance --type free-quota` 查免费额度余额，`arkcli billing list` 查账单。
- **Hermes 侧只有合并统计**：`hermes insights`（近 30 天 sessions/messages/tokens，按模型分不分账号）；custom provider 无定价 → 成本显示 Unknown。要分账号就得靠 arkcli 或控制台。
- 最快路径仍是控制台（方舟 → Coding Plan → 用量/额度页），arkcli 适合要脚本化/留档时用。

## 常见问题
- 连接超时：检查网络（GitHub 被墙时走镜像；火山 API 国内直连可达）
- 返回空/格式错：加 JSON 模式或结构化提示；验证响应再使用
- key 失效：火山控制台重新生成，勿当 bug 排查
