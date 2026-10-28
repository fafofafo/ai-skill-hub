# 远程桌面 MCP 控制（AI 操作远端 Windows/macOS 主机）

## When to Use

Hermes（Linux 大脑）要「看见并操作」远端 Windows/macOS 桌面的 GUI——无人值守运维、批量设备编排、接单演示「AI 操作远程电脑」。
与本地 computer_use 互补：本地桌面走本 SKILL 的动作词表；**远程桌面走 MCP client**（Hermes 原生 MCP client 连远端工具的 HTTP MCP server，工具自动注册为 `mcp_<server>_*`）。

## 已验证链路（QuickDesk，官方文档双向核验）

- 被控端：Windows/macOS 装 QuickDesk（host 内置 Chromium Remoting，WebRTC P2P + TURN 兜底）。⚠️ **无 Linux 客户端**——Linux 只能当「大脑」，不能当被控/主控端。
- 接入模式二选一：stdio（AI 侧 spawn quickdesk-mcp Rust 桥，须与 QuickDesk GUI 同机）；**HTTP/SSE（QuickDesk 托管，绑定 0.0.0.0:18080/mcp，支持多 AI 客户端 + 远程 IP 访问——Hermes 用这个）**。
- Hermes 侧配置（通用 MCP HTTP 传输细节见 hermes-agent 的 native-mcp 参考）：
```yaml
mcp_servers:
  quickdesk:
    url: "http://<win-ip>:18080/mcp"
```
重启 Hermes 生效（MCP 无热加载）；工具自动注册为 `mcp_quickdesk_*`（connect_device / screenshot / click / type / shell 等 40+）。
- 安全（必须）：18080 暴露 = 谁连上谁能操作桌面。官方防线：`--readonly-token`（只读）/ `--allowed-devices` 白名单 / `--rate-limit`；私部署信令 + TURN 端口别裸奔公网，走内网/VPN。

## 评估任何「AI 远程控制」工具的检查单

1. 平台支持表对照**实际主机**（无 Linux 客户端 = 判 🔮 不判 ✅）
2. MCP 模式：stdio 需同机，HTTP/SSE 才支持 Hermes 远程接入
3. 认证/白名单/限流措施是否够挡公网暴露
4. 私有化（自建信令/TURN）是否全套，数据能否自持
