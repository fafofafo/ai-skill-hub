# ima 知识库内容读取完整工作流（2026-09-08 实测打通）

> 场景：用户要求"学习 ima 里 XX 路径下的所有内容"。ima 开放平台不仅能写，**能读本人笔记全文**。
> 实测：30 篇 76KB 全量拉取约 22 秒（含限流 sleep 0.3s/篇）。

## 一、完整链路（4 步）

1. **定位知识库**：`POST /openapi/wiki/v1/get_addable_knowledge_base_list`，body `{"limit":50}`（limit 必填 1-50，缺省报 invalid range）→ 拿 `id` + `name`（如「腾讯云主机」）
2. **列文件夹/条目**：`POST /openapi/wiki/v1/get_knowledge_list`，body `{"cursor":"","limit":50,"knowledge_base_id":"<kb>","folder_id":"<folder>"}`
   - folder 省略=根目录；**根目录的 folder_id = knowledge_base_id**
   - 文件夹条目：`media_type=99`，`media_id="folder_<id>"`；笔记条目：`media_type=11`，`media_id="note_..."`
   - 响应含 `current_path`（面包屑）与 `is_end`/`next_cursor`（分页）
3. **取短 docid**：`POST /openapi/wiki/v1/get_media_info`，body `{"media_id":"<长ID>"}`
   - 笔记类返回 `url_info.url = "chrome://note?docid=<短docid>&media_id=<长ID>"`——docid 就是真实 note_id
   - **必须用短 docid**；直接用长 ID 调 get_doc_content 会报 `210005 GetNoteContent not author`（误以为是权限问题，实为 ID 格式问题）
4. **读正文**：`POST /openapi/note/v1/get_doc_content`，body `{"note_id":"<短docid>","target_content_format":0}`（0=纯文本，1=MARKDOWN 不支持，2=JSON）→ `data.content`

## 二、media_id 结构备忘
`note_3d061d36e567fc663e044742ce4e04ac_75026565703981397503301281061751`
- 前缀 `note_` + 客户端 hash + 下划线 + 长数字
- 长数字 = 短 docid（前 16 位，如 7502656570398139）+ 知识库根 folder_id（后 16 位）
- 稳妥做法：永远走 get_media_info 取 docid，不手工截取

## 三、批量读取脚本模式（Python）
```python
# 循环：get_knowledge_list 列条目 → 每篇 get_media_info 提 docid → get_doc_content 读正文 → 存文件
# 注意：每篇之间 sleep 0.3s 防限流；失败重试一次再跳过
# 30 篇约 22s；docid 作文件名避免中文路径问题
```

## 四、权限边界（诚实告知用户）
- `get_doc_content` 仅能读**当前 API Key 对应账号创建的笔记**；他人笔记报 `210005 not author`
- `get_knowledge_list`/`search_knowledge` 可列出有浏览权限的共享库条目（标题级）
- 读不了他人正文时：让用户在 ima 客户端手动导出，或换用对应账号的 key

## 五、接口权威来源（别再猜接口名）
官方 ima-skills 包：`https://app-dl.ima.qq.com/skills/ima-skills-1.1.9.zip`
- 解压含 `ima-skill/notes/references/api.md`（笔记模块）与 `ima-skill/knowledge-base/references/api.md`（知识库模块）
- 这是 OpenAPI 的完整接口清单（含全部 Req/Rsp 数据结构），版本号可能更新，下载最新即可
- 搜网上的第三方 skill（如 man80ljm/imaskill）也可，但以官方包为准

## 六、易踩坑
- `list_notebook` 不带 limit → 报 `invalid ListNoteFolderReq.Limit`（limit 1-20）
- `search_knowledge` 返回标题级匹配，`highlight_content` 常为空——**不要指望它搜正文片段**
- 读取接口名是 `get_doc_content`（不是 get_note/get_note_detail/get_content，那些 404）
- GitHub raw 被墙时用 ghfast.top 镜像拉第三方 api.md
