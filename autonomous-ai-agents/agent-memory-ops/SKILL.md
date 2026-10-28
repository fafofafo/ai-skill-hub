---
name: agent-memory-ops
description: Use when 审计/维护 agent-memory 记忆库。含三指标体检与安全清理。
version: 1.0.0
metadata:
  license: MIT
  tags: [agent-memory, 记忆, 审计, 清理, prune, 运维]
---

# Agent Memory 运维与审计

> 针对**已上线**的 agent-memory 实例（`~/密钥目录/agent-memory/hermes_lite.py`，数据根 `~/.hermes/agent-memory-data`）做体检与安全维护。实现/搭建见受保护技能 `agent-memory`。

## 何时用
- 给记忆库做质量体检、清理过期记忆、排查"某主题 recall 不到"、评估记忆系统健康度。

## 三指标审计流程（体检）
1. `agent-memory stats` + `vectors`：总量 / 验证率 / 热冷分布 / 向量后端与熔断状态（jina 熔断降级 local 属预期，不必修）。
2. **召回抽测**：对 6-8 个已知主题跑 `agent-memory recall '<主题>' --top-k 3`，看命中率与 rerank 合理性；**污染测试**（问内部事务不应串出敏感系统）；**敏感测试**（问"密码/密钥"应只返回 `[已脱敏:...]`；`grep -rE 'sk-[A-Za-z0-9]{8}|password[=: ]' store/` 应为空）。
3. **生命周期**：备份连续性（`backups/auto_index.*.bak`）、store/索引一致性（`索引有条目但 store 缺文件` 应为 0）、未验证超期堆积数。
4. **成本运维**：沉淀 cron 在跑（`hermes cron list`）、`.env` 三个 key 齐全（只列名不打印值）、`vectors.json` 体积。

## 安全清理铁律（最重要）
**⚠️ 直接 `prune` 会删掉"未验证但高价值"的记忆。** 沉淀产生的事实几乎都未手动 verify（实测验证率仅 ~18%），naive prune 会把三省六部架构/身份/权限矩阵等核心事实全删（实测 31 条候选里 27 条是高价值）。

正确顺序：**先批量验证重要性>=7，再 prune 低值垃圾**：
```bash
python3 - <<'PY'   # 列出未验证且 imp>=7 的 id
import json
idx = json.load(open('/home/ubuntu/.hermes/agent-memory-data/index.json'))
for e in idx:
    if not e.get('execution_verified') and e.get('importance',0) >= 7: print(e['id'])
PY
while read id; do agent-memory verify "$id"; done < ids.txt
agent-memory prune --dry-run   # 确认只剩低值才 --yes
```

**7 天边界坑**：`find_expired` 用 `days_between >= retention`（`>=7` 天即过期），自查筛选别用 `>7`，否则第 7 天边界的高价值条目会漏过保护然后被 prune 误删。

**用重要性当验证规则**（沉淀平均 imp≈7.6，>=7 视为可信）：生产环境挂智能周清 cron——脚本 `~/.hermes/scripts/agent_memory_prune.sh` = 自动 verify imp>=7 → prune 低值（imp<=6），无清理静默；cron 周日 23:40 no_agent 零 token。

## 覆盖缺口排查
某主题 `recall` 0 命中时：
1. 先确认索引真缺该主题：`python3 -c "import json;print('kw' in json.load(open('/home/ubuntu/.hermes/agent-memory-data/index.json')))"`（拼内容全文）。
2. 缺因二：**沉淀时序差**（当日 23:30 前的事实当晚才沉淀，上午查不到属正常）；或**整条线从未被提取**（某业务线外部事实缺失）。
3. 对关键稳定事实直接 `agent-memory remember '<事实>' --category <type> --importance 8-9 --verified` 补记，立即可命中。

## Pitfalls
- execute_code 内核 PATH 无 `agent-memory`（在 `~/.hermes/bin/`）；批量 CLI 操作走 shell 循环，别在 execute_code 里调。
- 每条 `verify` 重写 index.json（原子写 + 自动备份），几十条循环没问题；`--dry-run` 永远先跑。
- `prune` 归档到 `backups/prune_*.json`，删了也可恢复；但高价值被删的"恢复"成本高——预防优于补救。
