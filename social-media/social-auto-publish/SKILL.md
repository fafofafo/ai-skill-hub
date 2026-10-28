---
name: social-auto-publish
description: Use when 用 social-auto-upload(sau) 多平台自动发布。含无头安装/扫码登录/手机号坑。
metadata:
  hermes:
    tags: [social-auto-upload, sau, 小红书, xiaohongshu, 自动发布, patchright]
---

# 社交媒体自动发布（social-auto-upload / sau）

## 这是什么 / When to use
- 用户要把内容自动发布到多平台（抖音/B站/小红书/快手/视频号/TikTok/YouTube），工具 = `social-auto-upload`（dreammis/social-auto-upload，14.6k stars MIT，本机 `~/tools/social-auto-upload/`）。
- 已验证可用：登录/上传/填标题正文全通；发布被"未绑定手机号"拦住（见下）。
- ⚠️ 风险提示：浏览器模拟+持久化 Cookie = 平台可检测→限流/封号；作者 README 自称"尽量降低平台检测风险"。用户 2026-09-07 明确"赌一把"并接受风险——用**小号+低频+先测试**落地，主号别碰。Cookie 文件 chmod 600。

## 无头服务器安装（已验证路径，Ubuntu 24.04）
```bash
cd ~/tools && git clone https://github.com/dreammis/social-auto-upload.git
cd social-auto-upload && uv sync          # 建 .venv
cp conf.example.py conf.py
# 补 playwright 包（项目代码混用 patchright + playwright import）
UV_INDEX_URL=https://mirrors.cloud.tencent.com/pypi/simple uv pip install playwright
# 装 patchright 专属 chromium build（关键！见 Pitfalls）
unset PLAYWRIGHT_DOWNLOAD_HOST
.venv/bin/python -m patchright install chromium
```
conf.py：`LOCAL_CHROME_HEADLESS = True`；`LOCAL_CHROME_PATH` 指向**真实存在的 chromium 可执行文件**（当前已验证值 = `/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome`）。留空会走 patchright 默认 headless_shell 分支，该 build 未装时 launch 直接失败（`Executable doesn't exist ... chromium_headless_shell-1208`）。

## 登录（小红书为例）
```bash
# 无头模式：输出终端二维码 + 存 PNG 到 cookies/xiaohongshu_<名>_login_qrcode_*.png
# 后台跑，把 PNG 发给用户用小红书 APP 扫码，进程等 5 分钟
.venv/bin/sau xiaohongshu login --account <名>
.venv/bin/sau xiaohongshu check --account <名>   # 校验 cookie（输出 valid）
```
- 二维码 ~5 分钟过期，过期进程自动退出（日志"等待扫码登录超时"）→ 重跑即可，别当故障。
- cookie 落盘 `cookies/xiaohongshu_<名>.json`（storage_state 格式），后续 check/upload 复用。
- 已在用的小号：account `用户测试`（小红薯5FA9159D）。

## 发布图文
```bash
.venv/bin/sau xiaohongshu upload-note --account <名> \
  --images /path/图.png --title "标题" --note "正文" --tags "标签1,标签2"
```
- 图文至少 1 张图；无图/无字体时用 PIL 生成测试卡（中文字体 `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`）。
- 发布流程：上传图→填标题→填正文→点"发布"→等成功 URL。耗时 1-3 分钟正常。

## 发布视频（小红书）
```bash
.venv/bin/sau xiaohongshu upload-video --account <名> \
  --file /path/video.mp4 --title "标题" --desc "正文" --tags "标签1,标签2" \
  --thumbnail /path/cover.jpg
```
- **同一 MV 目录常有多版本并存**（初版/风格版/新版同目录或 `-xx版` 子目录）：用户说「最近一次 / 某风格版 / 重新发」时，先 `ls -lt` 列出目录所有 mp4 按时间选最新、或按用户风格词选对应版本，把选定文件路径明示给用户确认，别凭文件名猜。
- **「发布最近生成的 N 首」= 跨目录按 mtime 选最新 N 个 mp4**：用户批量发布指令（如「最近五首」）用 `find /data/projects/p_1bab4a -maxdepth 2 -type f -name "*.mp4" -printf '%T@ %p\n' | sort -rn | head -N` 按文件修改时间倒序列出，每行附 `ffprobe` 时长；选好后面向用户逐个列「文件名+时长+拟定标题」确认平台与文案，再逐条执行。同目录的初版/风格版可能都进列表，确认时提醒用户避免重复发同一歌的旧版。
- 实测可发：880x1184 竖版 3:4、4-5 分钟、~26MB，全程约 2 分钟。
- **MV 类固定文案模式（用户已确认）**：标题 `《歌名》MV｜AI改编`（用户也可能给 `AI音乐MV，歌手《歌名》原版/版本` 格式，歌手+原版词由用户给，别自己编）；正文一句话点明风格（用户要求正文和标签**必须体现风格词**，复古版写「复古未来主义」，换了风格版本就换成对应词如「中世纪现代」）；标签 `歌名,歌手,经典歌曲,MV,AI改编,<风格>,<风格英文>,音乐视频`；封面取视频第1秒帧 `ffmpeg -y -ss 1 -i <video> -frames:v 1 -q:v 2 cover.jpg`。发布前把标题/正文/标签发给用户确认，改稿以用户当轮指令为准。
- 账号 `用户测试` = 小红书号 1074908967（昵称 FAFO）；只发这个小号。
- 成功标志：日志 `SUCCESS: 🥳 视频发布成功` + 结尾 `Xiaohongshu video upload submitted: <path>`；**命令不返回笔记 URL**，回报"已发布"以这两行日志为准，URL 需用户 APP 端看。
- 流程日志序列：check cookie → 上传前检查 → 赶往发布页 → 填标题描述话题 → 设置封面 → 来源转载已声明 → 发布成功。
- **自定义封面 `--thumbnail` 不可靠**：实测多次超时失败（等"上传"Tab / cover-plugin-preview 元素超时），自动回落用视频首帧。发布前别承诺自定义封面，如实告知可能用首帧；真要指定封面 → 发完让用户 APP 端「编辑视频→设置封面」手动换。
- **不存在的标签会被静默跳过**：日志 `话题『xx』未出现候选，跳过该标签`（如 `#AI改编` 平台没有）。发布前选平台已有话题，别用生造词；被跳过的标签不算发布失败。
- 一键封装：`scripts/publish_video.py`（清 PYTHONPATH + 后台起 sau + 轮询日志判成功），execute_code 里直接 subprocess 调，省手写轮询样板。

## 多平台（B 站等）与「小发」Bot
- sau 支持：`douyin,kuaishou,xiaohongshu,bilibili,tencent(视频号),alipay,weibo,hupu,youtube,baijiahao`（`sau --help` 确认）
- **B 站只发视频**：`sau bilibili login/check/upload-video`——登录=扫码同小红书（`sau bilibili login --account <名>` 出二维码）；**无图文动态命令**（B 站子命令只有 upload-video）。**upload-video 必须传 `--tid`（分区 ID），音乐区 tid=3**：
```bash
.venv/bin/sau bilibili upload-video --account <名> --file <视频> --title <标题> --desc <简介> --tid 3 --tags <标签1,标签2>
```
- **B 站发布成功验证**：sau 只打印 `Bilibili video upload submitted`，不发 URL。真实结果用 biliup 直接查：`~/.social-auto-upload/tools/biliup/linux-x86_64/biliup -u cookies/bilibili_<名>.json list` → 输出 `BV号\t标题\t审核中/已发布`，有 BV 号才算发成。
- **已用 B 站账号**：account `bili_82851538509`（UP 主显示名 F-A-F-O），cookie 在 `cookies/bilibili_bili_82851538509.json`。
- **B 站删稿（去重复）**：biliup/sau 都没有删除命令，curl/fetch 直调删除 API（`api.bilibili.com/x/vu/del`、`member.bilibili.com/x/vu/del`）都吃 WAF/404 的 HTML 错误页。**真实删除接口是 `member.bilibili.com/x/risk/archive/del?platform=web&bvid=<BV>`**（监听创作中心点击删除时的 XHR 才能发现；返回 JSON 而非 HTML）。可行路径 = 浏览器自动化操作创作中心：登录 `member.bilibili.com/platform/upload-manager/article`（把 biliup cookie 的 `cookie_info.cookies` 转成 storage_state 注入）→ 页面列表显示「全部稿件 N」→ **删除按钮是 hover 才显示的隐藏 button**（rect 0x0；headless/xvfb 下 hover 事件常不触发），先 `mouse.move` 到行上再找可见「删除」按钮点击；hover 不显示时 JS 强制 `btns[0].click()`——**但 `btns[0]` 是 DOM 顺序第一条（列表最新稿，可能是别的视频）**，必须先用页面文本/时间/BV 确认目标行再删，别裸用 btns[0]。弹确认框点「确定/删除」→ 删除后刷新重查「全部稿件 N」数。区分哪条是重复稿：按上传时间（列表里每个稿件行有发布时间）或 BV 号，只删确认过的旧版，别误删新版。**删除接口也可能被账号风控拦截**：响应 `{"code":340052,"message":"您的账号存在风险请先验证"}` → 自动化删不了，停止重试并让用户在 B 站 APP/网页完成验证或人工删除（频控/风控期删除与投稿都受限）。
- **B 站 MV 文案套路（用户确认）**：标题 ≤25 字（18 以内最佳）说清「歌名+类型+亮点」，版本词要体现在标题（如 `《笑纳》越南鼓版 MV`、`《黄梅戏》DJ 版 MV`、`《好心分手》citypop版`）；近期用户偏好的标题格式是 `AI音乐MV《歌名》<版本/风格>版` 前缀（如 `AI音乐MV《天涯》摇滚DJ版`、`AI音乐MV《小镇姑娘》土嗨DJ版`、`AI音乐MV T.R.Y《不是因为寂寞才想你》粤语版`）——版本词（摇滚DJ/土嗨DJ/粤语/越南鼓/citypop）由用户给，别自己编。简介**去掉开场介绍句**，直接写 `🎬 AI 改编制作 | FAFO 工作室` + `原曲：歌手《歌名》（版本）`（或 `喜欢请点赞投币收藏，三连支持～` + 一句贴合歌词的话）；标签 6-10 个，前 3 最重要，类型+特色结合（歌名,歌手,音乐,MV,AI改编,版本词,风格词,经典歌曲…）。发布前把标题/简介/标签发给用户确认，用户会逐轮改稿（去第一行/加版本词/加歌手名），以当轮指令为准。
- **B 站封面规则（用户确认）**：默认选择首页封面，封面比例 4:3，展示原图（880x1184 竖版）**最上面 4:3 部分**：`ffmpeg -ss 1 -i <video> -frames:v 1 /tmp/f.png && ffmpeg -i /tmp/f.png -vf "crop=880:660:0:0" cover_43.jpg`（crop 高 = 宽*3/4，从 y=0 起裁）。
- **B 站登录强制要求交互终端，无头服务器要用 pty 伪装**：`sau bilibili login` 内部检查 `sys.stdin.isatty() and sys.stdout.isatty()`，非交互环境直接拒绝（"Bilibili login requires a local interactive terminal"）。绕过：用 `pty.openpty()` 把子进程 stdin/stdout/stderr 接 pty，后台跑 + reader 线程读输出（见下）。
- **biliup 二进制缺失时自动下载常超时，需手动镜像下载**：sau 的 biliup 运行时在 `~/.social-auto-upload/tools/biliup/linux-x86_64/biliup`；缺失时 `ensure_biliup_binary` 从 `github.com/biliup/biliup/releases` 下载会 connect timeout（api.github.com 通但 downloads 不通）。手动下载用镜像：`curl -sL https://gh-proxy.com/https://github.com/biliup/biliup/releases/download/v1.3.4/biliupR-v1.3.4-x86_64-linux.tar.xz`，解压后把 `biliupR-v1.3.4-x86_64-linux/biliup` 移到 `linux-x86_64/biliup` 并 chmod 755。
- **biliup 交互菜单选「扫码登录」**：pty 起来后出现多选菜单（账号密码/短信登录/扫码登录/浏览器登录/网页Cookie），光标默认在「短信登录」，**只按一次** `\x1b[B`（↓）+ `\r` 选「扫码登录」；按两次会选到「浏览器登录」（变成浏览器链接而非二维码，选错要重跑）。二维码生成在项目根 `qrcode.png`，发给用户扫。
- **B 站频控 code 21566「投稿过于频繁」**：`upload-video` 返回 `ResponseData { code: 21566, message: "投稿过于频繁，建议将APP升级至最新版本后再试" }`，RC 1。**频控是账号级滚动窗口，不是严格按自然日**：过 0 点后窗口重置能再发，但当日累计约 4-8 条（视账号权重）又触发——实测 10-26 发 8 条后拦，10-27 发 4 条后第 5 条又被拦。**保存草稿也不绕过**：`--extra-fields '{"draft":1}'` 视频能上传成功但提交接口同样 21566。**手动网页发布同样受限**（频控在提交接口层，与自动化无关，用户问"手动发是不是就不限"答案是否）。发现 21566 立即停手，把待发清单备好（标题/简介/标签/封面全就绪），用**一次性 cron 定时任务**自动重试：**用户要求「继续现在发，试试看」时可以试一次确认频控是否已解除——预期仍被拦（实测间隔 ~1 小时照样 21566），一次失败后立即停，不要连试 4 条；**`cronjob_manage action=create schedule="in 2h"`（或 `"in 14h"` 排到次日），prompt 写成完全自包含的发布指令（视频路径/标题/简介/标签/封面 + sau 调用步骤 + 频控再遇即停），deliver=origin 回本会话；**批量排期发布时每条间隔 30-40 分钟**（等滚动窗口冷却，2 分钟间隔对当日批量太密），任一条再报 21566 就暂停 2h 重试该条、连续 2 次失败停止后续。用户改手动时先 `cronjob_manage remove` 掉该任务防重复。**cron 定时任务到点会自动真实发稿，且可能已在后台把清单里的条目发掉**——若用户随后又手动要求发同一条（尤其批量指令覆盖了待发清单），先 `biliup -u cookie list` 查该标题是否已有 BV：cron 已发成（状态=开放浏览/审核中）就跳过或提示用户删重复，别闷头再发一遍（实测：cron 夜里发掉棉花糖+漫步人生路，次日手动又发棉花糖 → 同标题两条 BV）。改任务清单用 `cronjob_manage update` 改同一 job 的 prompt，别 create 新的又忘 remove 旧的。
- **多平台同时被问「还在禁用吗」时，逐平台实测而非只 check**：cookie valid ≠ 能发布（小红书禁发是接口层、B站频控是提交层，check 都只验 cookie 有效期）。快速总览：B站 `biliup -u cookie list` 能列出稿件 = 登录有效，实际发一条看是否 21566 才知道频控解没解；小红书必须走一次完整上传→点发布→看网络响应才判禁发；抖音先看 cookie 有没有 `sessionid`。逐平台分别给出「登录态」与「可发布性」两个结论，别用一个 check 结果概括全部。
- **用户逐条改标题的批量确认模式**：批量发布多条时，用户常一次性发「第1条标题、第2条标题…」覆盖整组，其中可能夹杂「重新编曲」「某风格版」等描述词——把每条拟定标题完整回显成一列（含简介/标签缩略），等用户统一确认后再逐条执行；用户只改标题时，简介/标签沿用模板，别因标题变了就重问全部字段。
- **抖音 login 需要 patchright 专属 chromium build**：抖音 uploader 代码 `launch(channel="chromium")`（不像小红书那样能用 `executable_path` 指向 playwright chromium-1234），缺 patchright build 时 login 报 `Looks like Playwright was just installed... please run playwright install`。抖音登录前先 `.venv/bin/python -m patchright install chromium`（别设 PLAYWRIGHT_DOWNLOAD_HOST 到 npmmirror），装好再起 login 扫码。
- **抖音登录窗口期短（约 2 分钟，比小红书 5 分钟短），且扫码后必须在 APP 弹窗点「确认登录」才算完成**：只扫码不点确认 → 进程一直打「请扫码，小人正在耐心等待登录完成」直到 `等待抖音扫码登录超时` 退出且 cookie 未落盘。给用户发二维码时同步提醒「扫码 + 点确认登录」；用户说已扫/已确认但日志没变 → 大概率窗口已过期或确认未完成，直接重出二维码，别反复 check 旧码。登录成功的标志是 cookie 文件 `cookies/douyin_<名>.json` 出现 + 日志 `扫码成功`，check 输出 valid 才是终态。
- **抖音 headless 扫码确认可能根本不被捕获（疑被检测自动化拦登录跳转）**：实测连续 6 次「扫码+确认登录」进程日志都停在等待、cookie 不落盘、最后超时——headless 无头环境被抖音风控识别后，扫码确认后页面不跳转登录态。备选：① 手动 cookie 方案——**`document.cookie` 抓不到 HttpOnly cookie（缺 `sessionid`）**，必须 F12 → Network → 点任意请求 → Headers → 复制 Request Headers 里完整的 `Cookie:` 串（含 HttpOnly）；② 或放弃该平台。诊断登录态别用 `"creator-micro" in url` 判断（未登录的 upload 页 URL 也含该词，会误判成功）——看 cookie 里有没有 `sessionid` 才准。
- 多平台发布任务已交「小发」项目经理 Bot（profile `p_561911`，SOUL 见 `~/.hermes/profiles/p_561911/SOUL.md`，进度 `~/项目目录/projects/p_561911/进度.md`）：它通过 execute_code subprocess 调 `.venv/bin/sau` 执行登录/上传（项目 Bot 禁 terminal 但 execute_code 可用）；已登录账号 cookie 在 `cookies/<platform>_<名>.json` 复用

## Pitfalls（本会话全部实锤）
- **launch 报 `unknown flag ... exit code 64` = build 与 patchright 参数不兼容**：换一个 compatible chromium build（当前发布链路用 `~/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome` 实测正常），别用系统 google-chrome。下载 build **别设 PLAYWRIGHT_DOWNLOAD_HOST 到 npmmirror**（没有 patchright build → Download failure），用官方 cdn.playwright.dev（unset 环境变量）。
- **conf.py 的 LOCAL_CHROME_PATH 要指向可用的 chromium 可执行文件**：sau 有分支直接 `executable_path=LOCAL_CHROME_PATH`，填系统 chrome 或不存在的路径都会崩。写独立 patchright 探针时要同样显式传 `executable_path=<conf.py 里的值>`：默认 launch 走 headless_shell，未安装就报 `Executable doesn't exist ... chrome-headless-shell`。
- **代码里 launch 别带 `channel="chromium"`**：channel 模式参数集不兼容。把所有 `launch(headless=X, channel="chromium")` 改成 `launch(headless=X)`（sed 批量改）。
- **未绑定手机号的小红书账号无法发布**（页面横幅"你还未绑定手机号…绑定手机号后才可发布笔记"）：发布流程会**无限循环**打"🏃 小人正在冲刺发布图文"（main.py ~line 806 `while True` 点"发布"等成功 URL），永不退出。诊断：用 `scripts/xhs_diag.py` 打开创作平台读 body 文本找"绑定手机号"横幅。修复 = 用户 APP 端「设置→账户与安全→手机号」绑定后重发。
- 发布按钮无限循环时直接 kill 后台进程，别等它超时（无退出）。
- **自定义封面（--thumbnail）在新版发布页不稳定**：点「上传」tab 或 file input 常 30s 超时失败，日志『封面设置失败，跳过该步骤继续发布（用视频首帧）』——实测 6 条全失败，实际封面=视频首帧。用户 2026-10-24 决定：**发布不再传 --thumbnail**，直接用平台首帧，省掉 30s 失败等待。
- **AI 生成内容必须声明「笔记含AI合成内容」**（不是"来源转载"）：sau 旧代码误用 check_original_declaration 导致 2026-10-23 发 5 条全被判『包含利用AI创作但未声明的内容』违规。已修：declare_ai_content 提升到基类，视频/图文路径都调用（main.py 854/990 行）。发布日志看到 `已声明：笔记含AI合成内容` 才算合规。
- **标题框提前出现 ≠ 上传完成**：新版发布页上传过程中标题输入框就提前渲染，网速慢时视频还在传（预览区显示 `上传中 19%`）。旧代码看到标题框就放行填表→点发布，表单未就绪导致 3 次点击全落空。修复：填表前等「上传中」文本消失（`get_by_text("上传中", exact=False)` 不可见才算传完）——main.py 已加该等待，发布日志出现 `标题框已出现但仍在「上传中」，继续等上传完成` 属正常等待，别当卡死。
- **发布按钮 3 次点击未确认 ≠ 已发出**：日志 `第 N 次发布未确认` + 结尾无 `视频发布成功`，一律先开笔记管理页确认笔记数没多，再决定重跑，别盲目重发（避免重复发布同一条）。
- **发布按钮定位：`xhs-publish-btn` 可能是透明空壳，点它的 rect 中心不一定有效**：新版发布页 `xhs-publish-btn` 是 sticky 空壳元素（children=0、innerHTML 空、背景透明、cursor:auto、无 onclick）——点它中心可能**零网络请求**（点击事件没触发）。真实发布按钮是页面底部红色像素块。定位法：截图扫红色像素（RGB 阈值 R>200,G<90,B<110），按 y 分段找**密集聚类的红块中心**（不是全页红色平均中心——页面顶部 logo/活动卡片也是红色，会拉偏到 (300,288) 之类的假位置；真实按钮约在 x640-760/y655-695）。日志 `已按JS坐标点击发布按钮 x,y` 只是点了某元素，不代表点中按钮——**点击后必须看网络请求**：`pg.on("request")` 过滤 `note|publish|sns` URL，零请求 = 没点中；有 POST `/web_api/sns/v2/note` = 点中了。
- **发布页内容在内部滚动容器 `.publish-page`（scrollH≈1853 > clientH≈656），body 的 scrollHeight 不等于真实页面高**：定位/截图发布按钮前先 `document.querySelector('.publish-page').scrollTop = scrollHeight` 滚动到底，否则按钮区域被内容卡片（关联活动等）盖住或截图看不到。
- **点击发布前先关引导浮层**：新版页面常有「PK封面」popover（`.pk-cover-guide-popover`，z-index 100）和「视频分辨率较低」横幅，会拦截或干扰点击——先点「我知道了」关掉（`get_by_role("button", name="我知道了")`），或 JS `el.remove()` 移除 popover。
- **发布进程被中断（网关重启/kill）时**：publish 日志停在中间步骤 = 大概率没发出；重启后先跑笔记管理探针确认列表无新增，再重跑发布，别直接重发造成重复。
- **账号级禁发：发布点击 3 次未确认时，先监控网络请求区分「没点中」vs「被平台拒绝」**：点真实按钮后若发出 POST `https://edith.xiaohongshu.com/web_api/sns/v2/note` 且响应 `{"success":false,"msg":"因违反社区规范禁止发笔记","result":-9136}` = **账号被平台禁发**（账号级处罚，不是技术故障），再试点击/重发都没用。触发路径：同一账号多条笔记被判违规（如 AI 未声明）→ 平台禁发。处理：小红书 APP 端查违规通知/申诉（`我 → 设置 → 联系客服` 或违规通知里的「我要申诉」），处罚可能是短期的或需申诉解除；**账号解禁前停发**。诊断写法：`pg.on("request")` + `pg.on("response")` 过滤 `note|publish|sns` URL 并读响应 body，点击后**等 4-5 秒再抓**（请求不是瞬间发出），同时 diff 页面 body 文本——「因违反社区规范禁止发笔记」会作为新增文本出现，两者任一命中即确认。
- **小红书禁发 ≠ cookie 失效：check valid、首页数据正常（曝光/观看照常增长）都不能证明能发布**——禁发是发布接口层拦截，cookie 仍有效、创作中心首页照常显示。判断账号能不能发，唯一可靠方式 = 走一次完整上传→点发布→看网络响应（或直接看历史：最近一条「视频发布成功」的日志时间 vs 违规处罚时间）。别因 check valid 就认为解禁了。
- **删除违规笔记不会自动解禁**：用户把被判违规的笔记删掉后，发布接口仍返回 -9136（处罚挂在账号上，不随删笔记解除）。删笔记只是止损，解禁要等处罚期过或申诉；删完仍禁发属预期，别反复试加重记录。
- **execute_code 里调 sau 必须先清 PYTHONPATH**：Hermes execute_code 内核自带 PYTHONPATH（hermes 的 site-packages、scratch 目录等），会让 sau 的 `utils` 包解析冲突，报 `ModuleNotFoundError: No module named 'utils.log'; 'utils' is not a package`（terminal 直跑正常、execute_code 直跑必炸）。subprocess 调用时传 `env={k: v for k, v in os.environ.items() if k != "PYTHONPATH"}`，且 `cwd=~/tools/social-auto-upload`（项目根）。
- **cookie 会过期，发布前先 check**：小红书 cookie 不是永久的（实测约 3 周失效，`sau xiaohongshu check` 输出 `invalid`）。每次登录/发布前先 `check`，invalid 就重跑 `login` 让用户重扫，别拿旧 cookie 直接 upload 白等。cookies 目录里可能混有他人/主号 cookie（如 `xiaohongshu_主号.json`）——只动自己账号的文件，主号不碰。

## Support files
- `scripts/xhs_diag.py` — 小红书创作平台诊断探针：用 cookie 打开 publish 页，dump body 文本 + file input 数 + 按钮（判定账号可发布性/页面状态，判定是否有"未绑定手机号"横幅）。
- `scripts/publish_video.py` — 小红书发视频一键封装：清 PYTHONPATH + 后台起 sau upload-video + 轮询日志判成功（`--timeout` 默认 300s）。
- `references/account-status-diagnosis.md` — 用户报「笔记违规/限流」时的取证路径：创作中心笔记管理三个状态标签、新版路由、主站 IP 风控拦截与「要不要找用户截图」的判定表。
