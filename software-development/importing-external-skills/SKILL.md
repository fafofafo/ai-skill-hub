---
name: importing-external-skills
description: Use when 学习/导入外部AI技能（GitHub找'XX skill'）。搜→克隆→实测→迁入→适配→验证。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, import, github, migration, learning]
    related_skills: [hermes-agent-skill-authoring, hermes-bot-fleet]
---

# Importing External Skills（学习/导入第三方 AI 技能）

用户常下"学习 XX skill，在 github 上找找"——把开源仓库里的 AI 技能（SKILL.md 形式）吸收进本机技能库（`~/.hermes/skills/` 真相源）。完整流程与坑。

## When to Use
- 用户要求学习某个具体 skill（含名字，可能来自 Codex/Claude/开源技能集合）。
- 用户说"在 github 上找找"某类技能。

## 流程（顺序执行）

1. **定位仓库**：`web_search "<skill名> skill github"`；结果常是技能聚合仓库（如 vibeshotclub/vsc-skills）或独立 repo。先看搜索结果里的 README/SKILL.md 链接确认它是 Agent Skill（不是普通代码库）。
2. **克隆/下载**：`git clone --depth 1 <url>` 到 /tmp。GitHub 直连失败时的回退链（按序试）：① ghfast.top 前缀 `git clone https://ghfast.top/https://github.com/...`；② 小文件（SKILL.md/脚本）用 `curl --socks5-hostname 127.0.0.1:1080 <raw.githubusercontent url>` 经七牛代理拉单个文件；③ **大文件（release 预编译二进制等，>5MB）不要在代理链上硬拉**——SSH/scp 传大文件也常超时，改成：七牛主机 `curl` 直接下到 /tmp → 七牛起临时 HTTP（`python3 -m http.server 18888 --bind 0.0.0.0`）→ 本机 `curl http://<七牛IP>:18888/<file>` 直连拉回 → sha256 校验（release 常附 `.sha256`）。④ **HTTP 回退返回 0 字节（服务没起/被拦）时改 base64 单会话搬运**：`ssh <host> 'base64 /tmp/<file>' > /tmp/<file>.b64` 一次会话流式拿回，本机 `base64 -d` 还原——实测 512KB 仓库 tarball 约 77s 完成、字节数与原文件一致；传输后用 `ls -l` 核对文件大小（或 sha256）判断完整性，**别把 0 字节/被截断的文件当成功**。
3. **深读**：按 SKILL.md → README.md → scripts → references 顺序读。SKILL.md 是工作流；scripts 决定可执行性；references 是数据/深度。先理解再动手，别直接复制。
4. **实测（关键，自报完成≠完成）**：从仓库目录跑它的脚本，**多种模式/参数都试**（如产品+人物+海报+json 格式），确认输出真实可用。只看 README 声称能跑不算验证。
5. **迁移**：`cp -r <仓库>/<skill> ~/.hermes/skills/<name>/`（保持目录结构：scripts/ references/ 原样搬，脚本常以 `Path(__file__).resolve().parents[1]` 找 references，拆散结构就废）。删除平台专用文件（如 `agents/openai.yaml` 是 Codex 专用，Hermes 无用）。
6. **适配 SKILL.md**：frontmatter 的 `description` 改中文触发式（前 57 字符自包含触发词：`Use when <触发>. <一句话行为>`）；正文加一节「本机集成」写脚本绝对路径、标准用法、与现有技能的关系（互补/替代）。**小改动用 patch 不用 write_file**——write_file 覆盖已 cp 的文件会被拒（若之前分页读过）。
7. **同步 learn 副本**：`python3 ~/.hermes/scripts/sync_learn_skills.py`（技能回流规则：真相源 default 有 learn 缺 → 复制）。
8. **验证**：`hermes skills list` 可见 + **从新路径再实测一次脚本**（`python3 ~/.hermes/skills/<name>/scripts/...`）。
9. **汇报**：是什么/能干什么/价值（做事+进化双视角，用户偏好格式）。

## Pitfalls
- **ghfast.top 不是万能**：实测对部分仓库也返回 403；下载 release 大文件比 git clone 更麻烦，直接走七牛 HTTP 回退链（流程第 2 步）。
- **传输成功与否用字节数/sha256 判定，不靠命令退出码**：`curl` 对连接异常可能仍以 0 退出并留下 0 字节文件；还原后必须与远端 `ls -l` 或官方 `.sha256` 对比再进入下一步。
- **大支持文件不能走 skill_manage write_file**：几百 KB 的 JSON/数据文件（如 620 条风格库 588KB）无法塞进 write_file 的 content 参数——直接 `cp -r` 整目录，SKILL.md 用 skill_manage patch/create。
- **第三方 skill 常带 Codex/Claude 专用件**（`agents/`、`~/.codex` 安装说明、`--sref` 等外部平台参数）：Hermes 不消费，删掉或改写，避免后续会话照着无效路径操作。
- **迁移后必须从新路径实测**：原仓库能跑 ≠ 迁入后能跑；脚本相对路径假设（ROOT = 脚本上级的上级）在目录结构保持时成立，但改了结构立刻崩——实测兜底。
- **description 触发词要本地化**：英文触发式 description 在中文会话里命中率低；改成中文触发词后 `skills_list`/运行时才容易被正确加载。

## 关联
- 技能格式规范见 `hermes-agent-skill-authoring`；技能库同步机制（external_dirs/learn 回流）见 `hermes-bot-fleet` 的「技能库跨 profile 同步」节。