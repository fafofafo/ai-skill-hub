---
name: metatrader5
description: Use when 部署/运行 MT5 或接入 AI agent。含无头 Docker 部署已验证路径与踩坑。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mt5, metatrader5, trading, 交易, forex, docker, wine, mcp]
    related_skills: [agent-reach, hermes-agent]
---

## When to Use
- 要在 Linux/无头/云服务器上部署 MT5 交易终端。
- 要把 MT5（行情/下单/持仓）接入 Hermes 或 AI agent 团队。
- 排障：Wine 直装、Docker 镜像、MetaTrader5 Python 库、RPyC/8001 端口、numpy 版本。

## 核心事实（实测）
- MT5 是 MetaQuotes 的**免费交易终端软件，不是券商**；账户从券商开（先 demo → 验证 → 小资金实盘）。
- **终端必须先登录一个账户**（demo 也行），`MetaTrader5.initialize()` 才返回 True。`INIT: False` = 没登录账户。
- **MT5 Build 6060+（2026-07）官方原生支持 MCP**，可连外部 AI agent（Claude Code / Codex / Hermes 均可）。
- 风控铁律先行：单笔风险 ≤1%、日亏上限、总回撤 >15% 暂停复盘；绝不上真钱裸奔。

## 网络硬约束（已验证）
- **腾讯云/国内云访问 MetaQuotes 全被墙**（download.mql5.com、券商站超时）。MT5 必须跑在能访问国际网络的机器上（海外 VPS / 用户本地 / 能直连 GitHub 的机器如七牛云）。
- 国际可达机器上 `https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe` 返回 200（24MB）。

## 已验证路径：Docker 部署（推荐，跳过 Wine 直装的坑）
1. 前提：Docker、能访问国际网络、内存 ≥1.5G（建议加 2G swap）。
2. `docker pull gmag11/metatrader5_vnc:latest`（~6.7GB，内置 wine + MT5 自动安装）。
3. 启动（端口 3000 = noVNC 网页界面，8001 = mt5linux RPyC）：
```
docker run -d --name mt5 \
  -p 3000:3000 -p 8001:8001 \
  -v /opt/mt5_config:/config \
  -e CUSTOM_USER=<user> -e PASSWORD=<pass> -e TZ=Asia/Shanghai \
  --restart unless-stopped gmag11/metatrader5_vnc:latest
```
4. 首次启动自动装 MT5（5-10 分钟，日志 [1/7]..[7/7]），完成后 `terminal64.exe` 运行。
5. **开 demo / 手动操作 → 浏览器打开 `http://<host>:3000`** 用 CUSTOM_USER/PASSWORD 登录 noVNC，在 MT5 界面里 File→Open an Account→MetaQuotes-Demo。GUI 手动开 demo 比无头自动化稳得多。

## 关键踩坑（全部实测）
1. **mt5setup.exe 是引导器**（bootstrapper），非完整包；Wine 直装会卡死在下载（连接 CLOSE-WAIT 挂起），7z 解包只得到 18MB 的 `[0]` 数据块。→ 用 Docker 镜像绕过。
2. **mt5linux 库有 Python 3.11 不兼容的跨行 f-string**（PEP 701 仅 3.12+），报 `SyntaxError: unterminated string literal`。修复：把 `{\n  expr\n}` 压成 `{expr}`（正则 `\{\s*\n\s*([^}\n]+)\}` 全局替换）。涉及 metatrader5.py(6处)、_runtime.py、_base_runtime.py(2处)。
3. **Windows 侧 numpy 2.x 与 MetaTrader5 库冲突**：`numpy.core.multiarray failed to import` / `_ARRAY_API not found`。修复：`wine python.exe -m pip install "numpy<2"`（1.26.4 可用）。
4. **`.wine` 所有权**：容器内 `.wine` 归容器用户（KasmVNC 镜像为 `abc`），root 跑 wine 报 `'...wine' is not owned by you` → 用 `docker exec -u abc`。
5. **8001 RPyC 启动参数**：镜像 start.sh 用 `-w wine python.exe`，新版 rpyc_classic 不认 → 需绕过或用自建 HTTP 桥（详见 references）。
6. 容器截图诊断：Xvnc `:1`，用 `ffmpeg -f x11grab -i :1` 抓屏看界面。

## 接入 Hermes / Agent
- 首选：MT5 原生 MCP（Build 6060+，终端内配置）。
- 备选：mt5linux RPyC（8001，需先修上面的坑）或自建 HTTP 桥封装 `wine python.exe -c "import MetaTrader5..."`。
- 架构：Agent 团队（大脑）→ MCP/RPyC → MT5 终端（手）→ 券商。

## 支持文件
- `references/mt5-2026-08-session.md` — 本次完整实测命令链（部署/修库/验证），续接此项目先读它。
