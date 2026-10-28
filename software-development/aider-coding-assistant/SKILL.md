---
name: aider-coding-assistant
description: Use when 需要编码副手/改现有代码库/让 Aider 干活（已装，接 DeepSeek key）。
---

# Aider 编码副手（已装，接 DeepSeek，零额外账号）

Aider = 终端 AI 结对编程（Aider-AI/aider，Apache-2.0 全开源）。用用户已有 DeepSeek key，不需 OpenAI 账号（对比 Codex CLI：开源的是壳，模型仍要 OpenAI 账号付费）。

## 本机环境（已配好）
- venv: `/data/tmp_work/aider-venv`（uv 建，接腾讯云镜像装 aider-chat）
- key: 从 `~/.hermes/.env` 的 `DEEPSEEK_API_KEY` 读（不硬编码）
- 一键脚本: `bash ~/tools/aider_run.sh "需求" [工作目录]`（脚本已读 key、设 --yes-always --no-show-model-warnings）
- 成本：约 $0.0007/消息（DeepSeek 极便宜）

## 调用
```bash
bash ~/tools/aider_run.sh "给 xx.py 增加/修复..." [目录]
```
等价手工：
```bash
export DEEPSEEK_API_KEY=$(grep "^DEEPSEEK_API_KEY=" ~/.hermes/.env | cut -d= -f2- | tr -d '"')
cd <git仓库> && aider --model deepseek/deepseek-chat --file <文件> --message "需求" --yes-always --no-show-model-warnings
```

## 铁律
- **必须 `--file <文件>` 显式把文件加进 chat**——不加文件模型会说"我没有文件内容"然后空转（只回复不干活）。这是 Aider 改代码的第一步，忘掉它=白跑一轮。
- **必须在 git 仓库内运行**：Aider 靠 git 提交记录每次改动（自动 commit + 可回滚），非 git 目录先 `git init`。
- **自动 git 提交是它的核心价值**：每次改动自动 commit（`fix: ...`/`feat: ...`），改坏了 `git log` + `git revert` 即可回滚——这是派它干活比直接改安全的关键。

## 分工（什么活派 Aider，什么活自己干）
| 任务类型 | 谁做 | 理由 |
|---|---|---|
| 改现有代码库（多文件/有结构） | **Aider** | 代码地图+自动提交+可回滚 |
| 修 bug + 跑测试验证 | **Aider** | 它改完自己跑测试确认 |
| 从零写小脚本/一次性任务 | **自己** | 更快，无启动开销 |
| 需业务上下文（"给客户做X"） | **自己** | Aider 不懂你的业务/记忆 |
| 大项目重构 | Aider 改+自己审核 | 它改，我把关 |

派活时把需求讲清楚（它不知道会话背景）：改哪个文件、加什么功能、什么边界条件。

## 验证（别信它自报）
- 改完必须实测：跑改动后的代码/脚本，确认功能符合预期（它自报"Applied edit"不代表结果对）。
- 用 `git log --oneline` 确认提交存在。
- 复现路径：给它一段有 bug 的代码（如递归爆栈）→ 让它修 → 跑通验证，是最快的冒烟测试。

## 相关
- 不开源替代对比：Codex CLI（壳开源模型付费）→ 见 external-content-verification 的"开源壳≠免费能用"规则。
