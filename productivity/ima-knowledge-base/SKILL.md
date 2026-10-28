---
name: ima-knowledge-base
description: Use when 操作腾讯 ima 知识库（创建/导入/积累/备份）。含 OpenAPI 调用与批量导入。
version: 1.0.0
metadata:
  hermes:
    tags: [ima, 知识库, 腾讯, openapi, 备份]
---

# ima 知识库 API 操作（腾讯 ima.copilot）

## When to Use
- 向用户 ima 知识库积累/导入内容（共享知识库引流、脱敏备份）。
- 创建个人/共享知识库、批量导入笔记。
- **读取 ima 知识库内容/学习某路径下全部笔记**（用户要求"学习 ima 里 XX"时）。
- 排查 ima 同步失败（API key 失效）。

> 读取知识库全文的完整工作流（定位→列条目→提 docid→读正文 + 批量脚本 + 权限边界）见 `references/reading-kb-content.md`。

## 认证
- 凭据在 `~/.hermes/agent-memory-data/backup.env`：`IMA_CLIENT_ID` + `IMA_API_KEY`（source 后用于 curl）
- 请求头：`ima-openapi-clientid` + `ima-openapi-apikey`，`Content-Type: application/json`
- Base：`https://ima.qq.com`
- ⚠️ **API key 约半月失效**：报 `200002 skill auth failed`(401) 时，让用户到 ima 客户端重新生成 key，勿当脚本故障排查。
- ⚠️ **用户经企微粘贴的 key 会被截断/改写**（TikHub/Agnes 两次实锤）：接入任何用户提供的外部 API key 前先 curl 连测（同接口连测 3 次，一次成功一次失败 = 复制损坏，**非限流非配置**）；处理=让用户到平台「重新生成 + 完整复制」（key 只在创建时显示一次），尽量不经二次转发直接贴，必要时逐字符核对。已验证 key 优先用七牛 `/root/tikhub_key`（60 字节）这类本机可靠来源，别用企微贴来的。
- 📦 **接口权威来源 = 官方 skill 包**：`https://app-dl.ima.qq.com/skills/ima-skills-1.1.9.zip`（解压后 `ima-skill/{notes,knowledge-base}/references/api.md` 含全部接口+参数+数据结构）。**先查它再试接口**——ima 接口名不直观（get_doc_content 不是 get_note），瞎猜全 404 浪费时间。

## 核心接口
- **读取笔记正文**（2026-09-08 打通，之前以为不可读）：`POST /openapi/note/v1/get_doc_content`，body `{"note_id":"<短docid>","target_content_format":0}`（0=纯文本）
  - ⚠️ 知识库条目 media_id 是长 ID（note_<hash>_<docid><kb_folder_id>），**必须先用 `POST /openapi/wiki/v1/get_media_info`（body `{"media_id":...}`）取 url_info.url 里的短 docid** 再调 get_doc_content；传长 ID 会报 `210005 not author`
  - ⚠️ 仅能读"本人笔记"（API Key 对应账号创建的）；他人笔记报 not author
- 浏览知识库内容：`POST /openapi/wiki/v1/get_knowledge_list`，body `{"cursor":"","limit":50,"knowledge_base_id":"<kb>","folder_id":"<folder>"}`（folder 省略=根目录；文件夹条目 media_type=99）
- 搜索知识库内容：`POST /openapi/wiki/v1/search_knowledge`（返回标题级，highlight_content 常为空）
- 测试连通：`POST /openapi/note/v1/list_notebook`（注意：不带 limit 会报 invalid range，limit 需 1-20）
- 创建知识库：`POST /openapi/wiki/v1/create_knowledge_base`，body `{"name":"<名>","description":"...","type":"KBT_SHARED_KB"}`
  - **type 必填且必须小写**：`KBT_MINE_KB`（个人）/ `KBT_SHARED_KB`（共享，可分享引流）/ `KBT_SUBSCRIBED_CREATE_KB`
  - name 正则：非空、无首尾空格、≤25 字符
- 导入笔记：`POST /openapi/note/v1/import_doc`，body `{"content_format":1,"content":"<markdown>","folder_name":"<夹名>"}` → 返回 note_id
- 加入知识库：`POST /openapi/wiki/v1/add_knowledge`，body `{"media_type":11,"title":"<标题>","knowledge_base_id":"<kb_id>","note_info":{"content_id":"<note_id>"}}`
- 查库：`POST /openapi/wiki/v1/search_knowledge_base` / `get_addable_knowledge_base_list`

## 批量导入模式（已验证）
对每个 md 文件：import_doc 建笔记 → add_knowledge 加入目标 KB。标题取文件首个 `# `。脱敏：只放可对外内容，不含路径/凭据/客户 token。

## 共享知识库（引流用途）
- API 创建共享库 + 导入内容 ✓；**分享链接/二维码/成员管理只能 ima 客户端操作**（API 无分享接口，`get_share_link`/`share_knowledge_base` 等均 404）。
- 现有共享库：「AI多Agent自动化」（kb_id 在导入脚本/记忆可查），含 9 篇 AI 进化干货。

## 相关脚本
- 记忆备份：`~/密钥目录/agent-memory/ima_backup.py --upload`（周日 cron）
- 工作日志：`~/密钥目录/agent-memory/worklog.py --upload`（每日 cron）
- 知识库同步：`~/.hermes/scripts/vault_sync_ima.py --upload`（周日，Obsidian→ima）
  - ⚠️ **新增篇目后同步会被去重跳过**：脚本对同内容合并笔记去重，输出 `⏭ 已存在跳过` 时**新篇未入 ima**（旧合并笔记仍含旧内容）。新增篇目后必须 `vault_sync_ima.py --upload --force` 强制重建；`--force` 会重建合并笔记（note_id 会变，属正常）。
