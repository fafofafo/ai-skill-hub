---
name: wechat-articles
description: Use when 用户分享 mp.weixin.qq.com 链接要"阅读/学习/了解"。含抓取解析脚本与验证流程。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wechat, weixin, 公众号, 文章, article, 验证]
    related_skills: [blocked-page-recovery, content-intelligence, wechat-channels-scraper]
---

## When to Use
- 用户直接丢 `https://mp.weixin.qq.com/s/<ID>` 链接，要求"阅读/学习/了解一下/阅读理解"。
- 这是该用户的**高频固定工作流**（内容创作者跟踪 AI 生态），几乎每周多次。

## 用户约定（务必遵守）
- 分享外部文章/工具/视频后：**先验证真伪再讨论**，不要急于做视频；做视频需用户明确指示。
- 涉及项目/数据：用 api.github.com 查仓库（stars/created/活跃度）、对比官方文档核实。
- 结合用户体系讨论：指出"你的体系是否已有同类能力 / 哪些点值得借鉴"，有观点、不盲从、不硬装。
- **主角已覆盖时，增量在配角**：文章主角工具若本体系已有技能实测覆盖（如 HyperFrames 已有 hyperframes-ops），别再重复核验主角——把验证重心转向文中提到的相邻新项目/风格库（逐个 api.github.com 核验），学习产出落在配角上。
- **学习流程=RLT 完整闭环（用户 2026-09-16 定）**：学到 → 深读 → 迁移 → 落地 → 测试。**凡是判「现在有用」的条目，最后必须有验证细节**（实测证据：跑过命令/调过接口/对比过数据，附结果），照 2026-09-15 执行锚定验证先例；测不了的要标「未实测」并说明原因。只说不做的"有用"不算数。
- **验证后沉淀（用户偏好，不用问确认）**：结论有用 → 自动写 `~/Documents/Obsidian Vault/知识沉淀/<主题>.md`（含验证结论 + 值得吸收的点 + 与现有体系关系），vault 周日自动同步 ima 手机可看；明显不适用/无长期价值的不记。
- **第三方项目评估铁律（含 Skill 类文章）**：功能与官方/现有体系重叠的一律不装，仅吸收理念；即使文章吹得再火（star 数、"一周 XXX 星"），先 api.github.com 核实数字与 license——无 license（license: None）= 版权默认保留，可用不可转卖，评估时如实标注。

## 抓取（curl，勿用浏览器）
浏览器打开微信文章常超时卡死。curl 稳定：
```bash
curl -sL --max-time 60 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  "https://mp.weixin.qq.com/s/<ID>" -o wx.html   # 成功约 3.3MB
```
顺带提取公众号身份参数（全量学习要用）：`var biz = "..."` 和 `var user_name = "gh_..."`（正则从 HTML 取）。

⚠️ **风控验证页识别与绕过**：连续抓取频繁时微信返回 ~20KB 验证壳（无 h1/og:title，body 含 `verify`/`captcha` 标记；正常文章 3MB+）。**先看文件大小——明显小于 3MB = 大概率被风控**。换 iPhone Safari 移动 UA + `Referer: https://weixin.qq.com/` 重抓可绕过；仍失败则 sleep 15-30s 再试（限流会过）。成功后别立刻连续抓大量链接（同 IP 频率触发风控）。

⚠️ **新版文章（__moon 渲染）可能正文不在静态 HTML**：curl 返回 JS 壳（约 0.5MB 而非 3.3MB）时 `js_content` 为空、patchright 打开也 ERR_EMPTY_RESPONSE。**判断只看 js_content 是否抓得到，不要看 __moon 标志**：页面含 `__moon_initcallback` ≠ 一定失败（实测 3.57MB 完整页可同时含 __moon 和可解析的 js_content）——先按下方正则试提取，抓到就正常读；只有 js_content 确实为空才走多源补全：**①先取 og:title / og:description meta（curl 必可得）**判断主题 → **②web_search 该标题，找转载/同主题多源内容**（标题独特的公众号文几乎必有同款，如《14个国外远程工作平台盘点》→ 搜"国外远程工作平台 盘点"）→ ③web_extract 1-2 篇最系统的同主题源补全学习 → ④汇报时如实标注"原文正文抓取受限，同主题多源补全"。TikHub fetch_article_detail（biz/mid/idx/sn）对这类文章返回空，别死磕。

⚠️ **删临时目录前确认它不是当前 shell 工作目录**：rm -rf 掉 cwd 会让之后所有 terminal 命令报 `cd: ...: No such file or directory`（session cwd 卡死，cd 到哪都失败）——恢复用 terminal 的 workdir 参数指定有效目录。

⚠️ **企业微信文档（doc.weixin.qq.com）不可匿名抓取**：curl 只拿 JS 壳（标题"空白页"），patchright 只渲染出"企业身份登录/切换个人身份登录"——正文在权限墙后。别死磕（web_extract/curl/浏览器三路都到登录页），直接让用户**复制粘贴文档内容**。附带 scode 授权链接也不能匿名读。
   - 用户转来的文档文件常是**中文 Windows 导出 → GBK/GB2312 编码**：read_file 报 binary/内容为空。先 `file <f>` 看编码，GBK 用 `iconv -f GBK -t UTF-8 <f> > out.txt` 转码再读（不要直接当 UTF-8 读）。

⚠️ **微信百科（baike.weixin.qq.com/v<ID>.htm）正文在 JS 壳里**：curl 只能拿到 ~44KB 壳（title 可读但正文只有几字符），`__moon`/INITIAL 变量都不在静态 HTML。**必须用 browser_exec 渲染拿正文**：new_tab(url) → wait_for_load + sleep 3-4s → `js("document.body.innerText")`（一次拿到全文，含导航目录+正文+来源注记）。标题先 curl 拿，正文再浏览器补。

## 解析正文（js_content / js_article / og 兜底）
正文容器不统一，按序试，**先抓全标题再逐段取**：
```python
import re, html
raw = open('wx.html', encoding='utf-8', errors='ignore').read()
# 标题：h1 优先，失败用 og:title（部分文章无 h1 或 JS 渲染）
t = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.S)
title = re.sub(r'<[^>]+>', '', t.group(1)).strip() if t else (re.search(r'property="og:title" content="(.*?)"', raw) or [None,''])[1]
a = re.search(r'var nickname = "(.*?)"', raw) or re.search(r'id="js_name"[^>]*>(.*?)<', raw, re.S)  # 公众号
c = re.search(r'var ct = "(\d+)"', raw)                    # 发布时间(unix)
# 正文：js_content → js_article → og:description（短文/卡片文全文就在 og:description）
m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', raw, re.S)
if not m: m = re.search(r'<div[^>]*id="js_article"[^>]*>(.*?)</div>\s*<script', raw, re.S)
if not m: m = re.search(r'<div[^>]*id="js_article"[^>]*>(.*?)$', raw, re.S)
text = ''
if m:
    text = re.sub(r'<(br|/p|/div|/section|/h\d|/li)[^>]*>', '\n', m.group(1))
    text = re.sub(r'<[^>]+>', '', text); text = html.unescape(text)
if len(text) < 80:   # 空/纯空格（卡片文、纯图/纯链接文）→ og:description 常是全文或核心摘要
    od = re.search(r'property="og:description" content="(.*?)"', raw, re.S)
    if od: text = html.unescape(od.group(1)).replace('\\x0a','\n')
```
> 便捷：`hermes` 会话里这段脚本已多次实测，可直接复用；og:description 里 `\x0a` 需转回换行。

## 正文是图片/截图（纯图卡片文）
正文文本极短但 `data-src` 图片数 > 0 时，内容都在截图里（常见：平台清单、长图、卡片列表）：
1. 从 js_content 正则取全部 `data-src` 图片 URL（mmbiz.qpic.cn），curl 下载到本地
2. **本地 tesseract OCR 逐张识别**（chi_sim 语言包已装）：`tesseract img.jpg stdout -l chi_sim`——零成本零等待，中文截图够用；先 `file` 确认图片完整
3. 不要首选 vision_analyze（偶发"图片数据不完整"失败）或外部视觉 API（从本机调用可能超时）；OCR 失败再考虑其他
4. 截图仍读不出就如实标注"图片内容未读出"，不假装看过

## 全量学习（触发词「全量学习」+ 链接）
用户说「全量学习」+ 某公众号链接 = 学该博主全部历史文章，**不是单篇**：
1. 解析公众号身份：从链接/页面取 `gh_xxx` 或自定义微信号（`var nickname` / `js_name` / 链接 user_avatar 里的 gh_xxx / 抓取时提取的 `user_name`）
2. 拉全量文章列表（**经七牛中转，见 tikhub-api**）：`POST https://api.tikhub.io/api/v1/wechat_mp/v2/fetch_account_articles` body `{"username":"<gh_xxx或微信号>", "raw":false}`
   - **翻页：把上一页返回的 `next_offset`（base64）作为请求字段 `offset` 传入**，直到 `is_end` 为真值——不是把 `next_offset` 当请求字段（那样会无限重复第一页）；区别于视频号的 `last_buffer`，别混用
   - **去重键是 (app_msg_id, idx, title) 三元组**，不是 app_msg_id 单独——一次群发推多条子文章共享 app_msg_id（idx 1/2/3），按 app_msg_id 去重会静默丢文；83 篇级全量约 8-9 页
   - **列表有数天缓存滞后**：当天新发的文章可能不在列表里，但 `fetch_article_detail` 按 URL 仍能取到——先拿详情确认账号/标题，别因列表缺目标文就怀疑解析错了公众号
   - 列表可能含视频/音频栏目（`item_show_type`），默认 0=文章
3. 逐篇抓正文：`POST https://api.tikhub.io/api/v1/wechat_mp/v2/fetch_article_detail`，**请求体字段名必须是 `url`**（传 `link` 会返回 422 "Field required" 缺 url）；`raw:false`。返回在 `data.content`：nick_name/user_name/bizuin 可用于二次确认账号归属。
   - **混合号过滤**：全量列表常混入大量非 AI 栏目（晨报/壁纸/旧号遗留设计内容等），按标题关键词过滤只学 AI 相关，内容包头部标注「已过滤 N 条（共 M 条原始）」；拿不准的保守保留让 learn 判定。判定口径同视频号（见 wechat-channels-scraper 的 AI 关键词表）
4. API key：`~/.hermes/agent-memory-data/backup.env` 的 `TIKHUB_API_KEY`（付费路由，已充值）；Header 按 TikHub 规范（Authorization Bearer 或 x-api-key，以官方文档为准）
   - **域名**：中国大陆用户用 `https://api.tikhub.dev`（`api.tikhub.io` 被 GFW 墙）；大陆外才用 io
   - **401 不一定是 token 无效**：从被风控的数据中心 IP（如腾讯云）直连，风控可能把请求伪装成 401 返回。**先经七牛云中转重试同一 token 再下结论**——本机直连 401、同一 key 经中转 200，险些误判 key 失效。确认中转也 401 才按清单排查：复制的是 API token 菜单的 token（只显示一次）/ 邮箱已验证 / token 未过期未停用 / 账号未冻结。余额不足是 402，与 401 分开处理
5. **内容包产物流向**：标题+`digest`（摘要字段）按主题关键词聚类 → 生成 markdown 内容包 → `~/知识库目录/drafts/`；**别逐篇抓正文**（83 篇级 token 爆炸），用标题+摘要聚合，learn 抽样核验正文主张
6. 全量拉到后 → 批量审定（PROMOTE 建速查表/吸收理念/灰产识别照旧，逐篇验证结论照旧）→ 回报：核验结果 → 主题聚合 → ✅N/🔮N/❌N 统计 → 可吸收点（learn 落盘 Obsidian + 知识库目录/main，回报时确认文件存在）

触发词拿不准时默认按「单篇」处理，不擅自扩展（约定已存 MEMORY）。

## 批量抓取（用户一次丢多个链接，高频）
用户一次给 N 个 `mp.weixin.qq.com/s/<ID>` 链接（如 14 篇系列文）时：
- **不要用 `&` 后台下载**——terminal 会拒（"Foreground command uses '&' backgrounding"）；用 `xargs -P` 并行：
```bash
mkdir -p /tmp/wxN && cd /tmp/wxN
cat > urls.txt <<'EOF'
<每行一个 /s/ 后的 ID>
EOF
cat urls.txt | xargs -P 6 -I{} bash -c 'n=$(grep -n "^{}$" urls.txt | cut -d: -f1); curl -sL --max-time 45 -A "<浏览器UA>" "https://mp.weixin.qq.com/s/{}" -o /tmp/wxN/wx_${n}.html'
# 每篇约 3.2-3.4MB；14 篇并行 <2 分钟；失败篇 size 偏小，重试单篇
```
- **先查重再抓取**：收到链接先对照 Obsidian `知识沉淀/` 已有篇目与 `~/知识库目录/`（可按标题/主题关键词），用户可能**重发已学过的同一批链接**。重发时不要重新抓取学习——指出"这批已学过+沉淀位置"，问清意图（重新对照新版 / 误发 / 深入某篇）再行动。同一批链接里的重复 ID 也直接去重（`sort -u` 或 set）
- **批量解析**：循环 `wx_N.html` → `body_N.txt`（标题/公众号/时间/正文），先打印每篇标题+字数清单，再**逐批精读**（每批 4-6 篇，避免一次打印 10 万字被截断）
- 学习流程同单篇：全部读完 → 本机/官方核实关键声明（如系列文里的版本/命令/star 数可对照 `hermes --version`、`hermes kanban --help`、`api.github.com`）→ 提炼增量 → 拆高价值篇目逐篇沉淀（无增量的纯信息/已有篇目不重复，见 external-content-verification）

## 视频号链接（weixin.qq.com/sph/ 等，非 mp.weixin.qq.com/s/ 文章）
- **第一优先级：用 `wechat-channels-scraper` 技能**（TikHub+七牛中转+Isaac64 解密+ASR 全链路已通，能把视频号变成内容包：作品列表+标题/简介+核心视频 ASR 转写）。用户给视频号链接（单个或一批）时直接走该技能，**不要先告诉用户"无法处理"**
- 视频号分享页是 JS 渲染 SPA：curl 只能拿 ~2.5KB 空壳（`<div id="app">`）——不要硬逆向视频号 API（无公开接口，成本高）
- 兜底（无 TikHub/无可用 key 时）：有可用浏览器 → 打开预览页取 og:title/描述；否则如实请用户提供标题/简介/要点再学习沉淀
- 视频号本质是视频：即使拿到元信息，画面与语音内容仍需 ASR 转写或用户转述——**不假装看过了**

## 批量核验多条目归档（用户发全量学习 md/清单时）
1. 先批量 `api.github.com/repos/<owner>/<repo>` 查所有有 GitHub 的项目（stars/license/活跃度/archived）
2. 无确切 URL 的条目用 web_search 按项目名确认存在性与真实仓库
3. 对文档给的官网/链接逐一实测可达性（404/域名错 = 纠错记录）
4. 逐条判定三档：✅现在有用（必须有验证细节，测不了标未实测+原因）/ ❌现在没用（重叠或不适用，给理由）/ 🔮将来有用（给触发场景）
5. 三档统计（✅N/❌N/🔮N 合计=总条数）+ 关键纠错写入 `Obsidian/知识沉淀/<主题>核验-<日期>.md`，然后三段式汇报
6. **归档有更新版时（同一主题文件再次收到）**：只增量核验新增条目，更新原核验报告的统计与条目，不重做旧条目
7. 验证细节三档示例口径：✅=给出实测命令/接口结果；❌=重叠或不适用理由；🔮=触发场景；统一注明「未实测」及原因

## 验证清单（真伪核查）
- 项目类：`api.github.com/repos/<owner>/repo`（stars/created/updated/license/archived）。
- 能力类：对照官方文档/命令注册表（如 hermes 的 slash-commands、官方 docs llms.txt）。
- **时效性声明（并购/融资/监管/封杀）单独核最新**：深度文里"某巨头收购某公司"这类大新闻半年内可能被监管否决/反转，文章本身写时没错但已过时——先用 web_search 查最新进展再写进内容包，并在笔记里更正原文结论，别照搬。
- **软件发版类文章（尤其讲用户自己跑的平台，如 Hermes）**：除核实文章所述版本外，必须对照**本机实际版本**（`hermes --version` 等）+ GitHub 最新 release（`api.github.com/repos/<owner>/repo/releases/latest`）——这类文章发布几天后就过时（实测：讲 v0.21.6 的文章核验当天 v0.21.7 已出），适用性结论会从"吸收信息"变成"要不要升级"。
- **Hermes 正确基线（2026-10-26 实测，科普文常写错）**：官方仓库=`NousResearch/hermes-agent`（MIT，非 `NousResearch/hermes`）；官方安装=`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`（Win=install.ps1），raw.githubusercontent.com 旧链 404；装后配置=`hermes setup`（不是 `init`）；聊天=`hermes` / `hermes chat`（不是 `start`）；技能=`hermes skills list` 存在。核验版本用 `hermes --version` + `api.github.com/repos/NousResearch/hermes-agent/releases/latest`。
- **能力主张依赖硬件时先探测本机**（本地模型/推理速度/显存）：`nvidia-smi`/`free -g`/`nproc` 一条命令验完再判适用——硬件不满足（如无 GPU、仅 3GB 内存）则该主张对本机判 ❌ 并给理由，别空挂"将来有用"；硬件满足再谈迁移落地。
- **AI/Agent 类工具文章（声称"AI 可接入/自动操作"）两层核查**：①平台支持对照本机/体系**实际主机**——如远程桌面工具无 Linux 客户端而舰队全是 Linux = 直接判 🔮/❌，勿被特性列表迷惑，以官方 release/README 平台表为准；②"兼容 Claude/Cursor/GPT"是营销话术，真问题是 **Hermes 能否当 MCP client**——能：`mcp_servers` 加 `url` 指向工具 HTTP/SSE MCP 端点（重启生效，工具注册为 `mcp_<server>_*`），把这条接入路径查实写进沉淀笔记，让「将来有用」的触发场景可执行而非空挂。
- **外链实测可达性**：文档/文章给的链接可能失效或域名写错——curl HEAD/GET 实测，以实际可达域名为准（例：Lovart.art 404 → 真实服务在 www.lovart.ai）。
- **文末"了解更多"跳微信官方《名誉保护投诉指引》**：链接主题与正文无关且指向官方投诉指引 = 该文被投诉/平台处理过的痕迹，不是正常内容——该文可信度相应打折。
- **拉 GitHub 文件内容**（README/技能正文等）：用 `api.github.com/repos/<o>/<r>/readme` 或 `/contents/<path>` 端点（返回 base64 解码），raw.githubusercontent.com 从本机拉取常超时。目录型数量声明（"59 种风格""N 个模板"）用 `/contents/<dir>` 列目录计数核实，别只信 README 数字。
- 警惕点：营销号引流（"回复XX领资料"）、把 Claude Code/Obsidian 生态包装成 Hermes 专属、未核实的"案例数据"；标题带"周入X/月入X/野路子"的副业引流文=高危（正文常为极短+平台清单截图、无实操细节），截图内容仍要 OCR 读完再判合法性，别因标题就定性。
