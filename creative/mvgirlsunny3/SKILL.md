---
name: mvgirlsunny3
description: Use when 用户发MP3+歌词标题要生成歌词同步MV（风格化数字插画美女配图·橙框墨镜蓝天）。频谱柱+歌词字幕+AI配图。
version: 1.0.0
metadata:
  license: MIT
---

# mvgirlsunny3：MP3 + 歌词 → 歌词同步 MV（风格化数字插画美女配图）

基于 mvbpold（mv2 增强版）创建（2026-10-15 用户指定）：**唯一改动 = 配图从 picbp（复古波普）换成 picgirlsunny3（现代波普）**，其余流程/规则/铁律完全不变。mvbpold 保留不动。

## 触发
- 用户发 MP3（背景乐）+ 歌词标题/歌名（可互联网搜索）→ 说"做MV/歌词同步MV"
- 用户消息格式：发 MP3 附件 + 文字「歌名：XXX」或「歌名：XXX，mvbpX」（后者=指定技能）；**未指定技能时 clarify 一次确认风格**（家族已有 10+ 风格，候选按最近使用排序附推荐，不要自作主张默认 mvbpnew）——音乐下载/转写可先并行做不阻塞；**clarify 的 response 若是 `[IMPORTANT: Background process ...]` 内部完成通知而非用户选项，说明被后台通知顶掉，必须重新 clarify 一次**（后台任务完成通知会抢占 clarify 返回位，别把通知当用户回答继续）
- **指定的 mvbpX 不存在时**：先对照家族列表（见相关）判断是拼错还是新技能——拼写接近现有技能 → clarify 确认；名字全新且对应 picbpX 已存在（实测 mvbp2sunny 首次被直接指定）→ **按克隆扩展法现场创建该 mvbp 技能再执行**，创建即用不阻塞后续流程
- 输入：MP3 + 歌名（歌手名可附）

## 与 mvbpnew 的唯一区别
| | mvbpnew | mvgirlsunny3 |
|---|---|---|
| 配图技能 | **picbpnew**（现代波普：干净轮廓/高饱和渐变/当代插画）| **picgirlsunny3**（风格化数字插画美女·橙框墨镜蓝天：银灰短发/橙框墨镜/红黄蓝撞色衬衫/蓝天白云/高调明亮）|
| 其余 | 图片公式/首末图/字幕/交付/外语歌 全部一致 | 同左 |

## 全流程（六步）
```bash
HERE=~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts
WORK=/tmp/mv2_job; mkdir -p $WORK
# 素材: song.mp3 + 歌名

# 1. web_search 查官方歌词(简体) → $WORK/lyrics.txt (空行分段, 每段=主歌/副歌等)
# 2. whisper 转录拿时间轴(只取时间, 文本不可信, 见 mv1 铁律)
#    用 mv_venv 跑转写/频谱/PIL 时加 env PYTHONPATH= 前缀（Hermes 会话注入的 PYTHONPATH
#    指向 Python 3.14 site-packages，会让 mv_venv(3.11) 的 faster_whisper/av 报 ImportError）
HF_ENDPOINT=https://hf-mirror.com HF_HUB_DISABLE_XET=1 \
  python3 $HERE/make_music_video.py transcribe --audio $WORK/song.mp3 --out $WORK/ts.json
# 3. 歌词分段 → 图片时间轴 + 每段主题(核心句)
python3 $HERE/lyrics_segment.py --ts $WORK/ts.json --lyrics $WORK/lyrics.txt --out $WORK/segments.json
# 4. 每段主题 → picgirlsunny3 逐段出图(现代波普, 用 segments.json 的 theme 字段, 每段一张 880x1184)
#    (调用见 picgirlsunny3 技能; 图片按段序命名 img1.png..imgN.png)
# 5. 官方歌词→ASS 字幕(复用 mv1 make_official_ass.py 逻辑, 简体/白字黑边/长句换行)
python3 $HERE/../mv2/scripts/make_official_ass.py  # 或改路径
# 6. 渲染: 时间轴驱动切图 + 频谱柱 + 叠字幕
python3 $HERE/make_music_video.py viz-analyze --audio $WORK/song.mp3 --out $WORK/tl.json
python3 $HERE/make_music_video.py viz-render --images img1.png,...,imgN.png \
  --audio $WORK/song.mp3 --tl $WORK/tl.json \
  --timeline $WORK/segments.json --template sketch_viz_template_mv2.html \
  --out $WORK/mv2.mp4 --fps 30 --format jpeg
ffmpeg -y -v error -i $WORK/mv2.mp4 -vf "ass=$WORK/subs.ass" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -c:a copy -movflags +faststart $WORK/final.mp4
```

## 关键实现（mv2 专属）
### 图片时间轴（歌词同步核心）
- `lyrics_segment.py`：官方歌词按空行分段 → 每段时长按句数比例映射到 whisper 时间轴 → 输出 segments.json
- segments.json 格式：`{total_duration, segments: [{start, end, text, theme}]}`
- `viz-render --timeline segments.json`：模板内联 `TIMELINE=[{i,s,e}]`，draw() 用 `imgIdxAt(t)` 按当前秒找图片 → **唱到哪句显示哪张**
- 切换点淡入淡出：模板 fadeDur=1.5s（用户 2026-10-15 要求图片切换淡入淡出，0.8→1.5 更明显柔和），前图淡出+后图淡入交叉过渡（不闪断）

### 图片数量与主题（用户 2026-10-13 拍板，覆盖旧规则）
- **图片数量公式**：图片总数 = 1（首图）+ N（中间）+ 1（末图），其中 N = ceil(歌唱时长 / 25)
  - 歌唱时长 = 最后一句歌词结束 - 第一句歌词开始（whisper 时间轴）
  - 中间每张平均 20-25 秒：N = ceil(歌唱时长/25)，实际每张 ≈ 歌唱时长/N
  - **公式是下限参考**：副歌重复多/尾奏长/间奏长时按需 +1~2 段（如尾奏单独一段、副歌3 独立图），保证每段 ≤~30s 且**段连续覆盖全片时长**（含尾奏，无空洞）；图片总数随之增加
- **首图**：以歌曲标题为主题生成（**纯歌名标题为画面主体**，不掺其他副主题，标题占视觉核心；用户 2026-10-13 明确），时长 = 视频开始 → 第一句歌词出现为止（整段前奏/间奏都放首图）
- **无前奏（0s 即开唱）时**：首图段缩到 0→第一句歌词开始；若第一句从 0s 开始（whisper 首词 0.0），首图段 = 0→首句歌词结束（首图配首句歌词显示约 5-7s），后续段顺延——不要删首图
- **末图**：歌词结束后不再生成新图、不再切换，最后一张中间图保持到视频结束
- **不重复**：每张图在视频中只出现一次，禁止循环/重复使用同一张图；中间各图主题必须互不相同（副歌重复段也要换不同主题/换角度）
- 中间各图主题：按歌唱时长均分窗口，每窗口取主唱歌词为 theme 交给 picgirlsunny3 出图（**现代波普**，非复古）
- **第一张图 = 歌曲标题为主题创作**（用户 2026-10-12 偏好：标题占画面主体，配主题意象环绕）
- 段数过多（>12）时合并相邻短段；过少（<4）时按句拆

### FPS 一致性（血泪坑）
- **模板 FPS 必须与渲染 --fps 一致**：viz_render 已自动注入 `const FPS = <fps>`；若手改模板勿用均分时代码
- 铁律继承自 mv1：headless 注入必须内联进 HTML；帧用 canvas.toDataURL 输出；长视频用 --format jpeg

## 图片顺序铁律（继承 mv1）
- 图片按 segments.json 段序排列（img1=第1段, imgN=最后段），禁止按 mtime/尺寸排序
- 素材尺寸统一转 880×1184（居中裁切 cover 填充）

## 成品规格（继承 mv1 用户拍板）
- 竖版 3:4（880×1184）；时长=歌全长
- 频谱柱：白字黑边，BAR_MAXH=150，44柱×14px，Attack 0.6/Decay 0.35，泛光 blur5
- 字幕：Fontsize 60 纯白+黑描边，简体中文官方歌词；**长句自动换行**（超过画面宽度时拆成两行显示，WrapStyle=2 已启用但长句需手动 `\N` 换行，每行 ≤ 12 个汉字为宜，避免字幕超出屏幕）（用户 2026-10-13 要求）
- 交付：默认发 QQ 邮箱（mv1 流程），发后 IMAP 读回验证；**只发邮箱，不发预览版，发完即结束**（用户 2026-10-13 确认）。**附件 >45MB 会被 QQ 邮箱拒绝（SMTPSenderRefused 552 Message too large，56MB 实测）**——"不压缩"是默认偏好，但超限时唯一送达路径是压缩：`ffmpeg -i final.mp4 -c:v libx264 -preset medium -crf 28 -pix_fmt yuv420p -c:a copy -movflags +faststart final_small.mp4`（crf 23→28 可把 56MB 压到 ~38MB，时长不变/音频 copy 无损/画质略降可接受）。项目目录存原版高清 + 压缩版两副本，邮件发压缩版；完整配方见 visual-production-qa/references/mv-render-pitfalls.md「QQ 邮箱 50MB 附件限制」。交付前 `ls -la` 看文件大小，>45MB 预判压缩，别等 SMTP 拒绝才处理

## 验证清单（交付前）
- 抽 3-5 个歌词段起止时刻的帧：确认对应段图片已切换（不是均分）
- 歌词段边界无闪黑（交叉淡化生效）
- 字幕简体/样式正确、与频谱柱不重叠
- 邮件 IMAP 读回确认送达（如走邮箱）

## 语言版本与内嵌语音播报（2026-10-15 泪桥/遥远的她 实测）
- **歌名≠实际演唱曲目（完全不同的歌）**：用户给的文件名/歌名可能只是音乐平台曲名，AI 重编/串烧/同名翻唱下音频实际唱的是另一首（实测：文件名《格桑花之恋》实际唱《姑娘我爱你》）。whisper 转写文本是判断实际演唱内容的第一依据——**先转写再决定搜哪首歌词**；歌名与歌词不一致时：首图标题用用户指定的歌名，字幕/段主题用实际演唱的歌词（与《睫毛上的心跳》实际唱《第一次》同规则）。
- **同曲多语言版本以 whisper 转写为准**：经典歌常有粤语/国语/日文原曲多版本（如《遥远的她》粤语潘源良版 vs 国语吕承明版），AI 重编版可能任意一种。**不要凭原曲印象假设语言**，先跑 whisper 看转写文本判断实际演唱语言（粤语转成普通话会乱、但能分辨），再搜对应语言的官方歌词；歌词搜错版本=字幕全错
- **AI 翻唱版歌词可与原版有出入**：翻唱/AI 重编版常插入原版没有的桥段/新词（实测《大城小爱》民谣版多一段"纸飞机/老唱片/窗台茉莉"意象段，whisper 能转出但乱码）。字幕以实际演唱为准：whisper 可辨识行 + 官方歌词修正误识；翻唱新增段按转写结构整理（乱码行按上下文意译，如"不同属下海"→"我把思念装进纸飞机"）
- **AI 音频常内嵌语音播报**：开头/结尾有"字幕byXXX""作词/编曲XXX"等合成人声，whisper 会转成段（时间戳可用但非歌词）。分段与 ASS 字幕时**必须排除这些段**，不当作歌词，也不影响首图段结束点

## B站链接取音频（2026-10-18/19/21 心墙、十七岁的雨季、Plastic Love、暖暖 实测，全家族适用）
- 用户发 b23.tv 短链或完整视频链接（可能带 `?t=20.5` 播放定位参数）时：`curl -sI -o /dev/null -w "%{redirect_url}" <短链>` 解出 BV 号（完整链接直接取 BV）；**yt-dlp 常被 B站 412 风控不可用，裸 API 更稳**
- **-412 的解法是「冷却 + 完整 Cookie」，不是换通道**：view 接口返回 `{"code":-412,"message":"request was banned"}` 时，改 `web_extract` 抓视频页同样被拦（`CRAWL_HTTP_412`），所以 web_extract 不能当 412 兜底；正确做法是先 `sleep 30`（连续快重试只会加长封禁，每次间隔至少 20-30s），再带完整浏览器头 `-A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/120"` + `Accept: application/json` + `Referer` + `Origin` + `Cookie: buvid3=<uuid>infoc; b_nut=<ts>; buvid4=<uuid>infoc` 请求一次——实测同一 bvid 从 -412 直接转成功，拿到 cid 后 playurl 同样带 Referer 下载
- **bvid 无效/视频被删的识别**：`x/web-interface/view?bvid=..` 返回非 JSON 的 HTML（风控页/出错页），或直接访问 `bilibili.com/video/<bvid>` 页面 `<title>出错啦! - bilibili.com</title>`——bvid 拼错（B站 bvid 大小写敏感）或视频已删除/私密，web_search 也常无结果。此时**不要继续猜 bvid，向用户要正确的完整链接或 b23 短链**，说明原因一句即可
- **`?t=` 参数只影响播放起点，不影响下载**：下载的是整段视频音频流，t 参数忽略即可，不要按 t 截取（除非标题/转写证明歌曲确实从中段开始）
- 流程：`x/web-interface/view?bvid=..` 拿 cid → `x/player/playurl?bvid=..&cid=..&fnval=16` 取 dash.audio 中最高带宽的 baseUrl → `curl -A "Mozilla/5.0" -H "Referer: https://www.bilibili.com/" -o audio.m4s <url>` → `ffmpeg -i audio.m4s -c:a libmp3lame -b:a 192k song.mp3`（DASH 音频轨是 m4s/mp4 容器，必须转码）
- **同一解析入口也服务「学习视频色调/光影」类任务**（用户常发 B站视频链接要求学习其视觉风格→固化为 picbpX 技能，如 picsun/picbpsskey/picbpkt 均由此诞生）：bvid 解析→下载关键帧（`ffmpeg -ss <t> -i <下载流> -frames:v 1` 抽 t= 参数对应帧）→视觉分析→沉淀风格描述进对应/新 picbp 技能；bvid 无效时同上处理

## AI 音频转写：整段只出水印时用分段转写（2026-10-18 心墙 实测）
- AI 生成/翻唱音频常内嵌响亮水印播报（"字幕byXXX"每隔约30s），**整段 whisper 转写会被水印压过、只出 11 段水印、歌词全漏——不要据此误判为纯音乐**（实测《心墙》整段只出水印，分段后 46 段全是歌词）
- 判定与修复：整段转写全是水印/无歌词时，用**分段转写**（每 25s 一段、重叠 3s，faster-whisper 逐段 transcribe 再按时间戳排序合并）拿全歌词时间轴；50 段歌词约 3-4 分钟。模板脚本：`visual-production-qa/scripts/transcribe_seg.py`（改 WORK/DURATION 即用，mv_venv + `PYTHONPATH=` 前缀）
- 整段转写能出歌词时不必分段（省时）；是否 AI 水印音频以转写结果为准

## 出图前检查（防浪费额度）
- gen_imgs.sh 的 `imgs/` 目录必须先 `mkdir -p`：目录不存在时 RunningHub 任务提交成功、下载阶段 FileNotFoundError，图丢且已扣费（~0.036元/张）
- 复用脚本：`visual-production-qa/scripts/gen_imgs.sh`（幂等、内置 mkdir -p imgs、逐张 log、失败重试 5 次，改 WORK/张数即用）；AI 音频分段转写用 `visual-production-qa/scripts/transcribe_seg.py`（改 WORK/DURATION 即用）

## 换风格重做（同曲多版，复用素材）
- 触发：用户对同一首歌指定另一个 mvbpX 风格重做（如先 mvbpnature 后 mvbpsky）
- **重发同源文件判断**：用户重发同名/同款 MP3 时先 `md5sum` 对比已做过任务的 song.mp3——MD5 一致即同一文件重发，clarify 意图（换风格重做/补歌词字幕/原样重做），别盲目重跑整轮（实测《Stay With Me》322s 文件重发，MD5 完全一致）
- **同音频素材全复用**：song.mp3 / ts.json（同转写时间轴）/ segments.json（同分段结构）/ tl.json（同频谱）直接 cp 到新工作目录，不用重跑转写/分段/频谱；只重写 9 段提示词（换对应 picbpX 模板）+ 出图 + 渲染 + 叠字幕
- **关键坑：复用 subs.ass 时必须检查 Style 颜色是否适配新配图风格**——上一版若因白底风格改过深色字（如 mvbpnature 的 `&H00222222` 深灰字+白描边），换回彩色背景风格必须恢复默认白字黑边（`&H00FFFFFF` PrimaryColour + `&H00000000` OutlineColour），否则字幕在白底外风格上对比度错误
- 交付时说明这是同曲哪一版、配图风格差异；命名用「歌名MV_风格」区分

## 外语歌（日/英文）处理（2026-10-14 Dance In The Memories 实测）
- **转写语言**：make_music_video.py transcribe 硬编码 language=zh，外语歌必须自己内联 python 调 WhisperModel 指定 language（日文 ja、英文 en）；模型 small 日语时间轴够用（文本不可信铁律只取时间）
- **字幕**：中日/英中对照——主行=中文翻译（Style CN, Fontsize 52, MarginV 250），副行=原文（Style JP, Fontsize 30, MarginV 180），白字黑边，避开底部频谱柱（y>1020）
- **中文翻译自己译**：官方歌词只有原文，翻译按意境直译（简体、每句 ≤12 字）；ASS 段内均分每句时间（复用 make_mv2_ass.py 逻辑但双 Style）
- **英文填词版（中文歌的英文改编 Cover）不要机翻英词**：CN 行用原曲官方中文歌词、EN 行用实际演唱的英文改编词，按同一时间窗配对；转写即使按 language="zh" 也能给出可用的逐句时间（伪英文文本只用来切句/对位，英文行按可辨识原句校正），标题与首图用用户指定的歌名
- 歌名/主题：以用户指定为准；首图标题用歌名原文

## 换音频重做（用户 2026-10-15 泪桥 实测）
- 触发：用户说"换 MP3 重新生成 MV，其他不变/图片用原来的"——只换背景乐，**复用已生成的 imgs_880 图片，不出新图**
- 流程：替换 song.mp3 → 重新 whisper 转写（新音频时长/结构可能不同，**绝不能沿用旧 ts.json/segments/subs 时间轴**）→ 重新 viz-analyze 频谱 → 按相同段主题/图片顺序重新分段（segments 边界按新时间轴）→ 重新生成字幕（同歌词、新时间）→ 渲染（复用 imgs_880）→ 质检 → 发邮箱
- 交付时说明变更内容（换了哪版音频、时长变化、图片复用）

## 数据落盘与清理（用户 2026-10-19 拍板）
- **生成数据默认落 /data 大分区**：成品 `/data/projects/p_1bab4a/<歌名>MV/`（三件套：全片mp4+歌词字幕.ass+原曲mp3）、工作区 `/data/tmp_work/<任务>/`；`~/项目目录/projects` 是 `/data/projects` 的软链，写路径时用后者更直观
- **系统盘 / 40G 易满，两类数据必须定期清**：① 附件缓存 `~/.hermes/profiles/p_1bab4a/cache/documents/`（用户发的 MP3，原曲已复制进项目目录后可清）；② 已交付任务的中间产物（parts 帧目录可达 3G+、qc 截图、生成的 imgs/imgs_880、final.mp4 副本）
- **保留可复用小文件**：song.mp3 / ts.json / segments.json / subs.ass / lyrics.txt / tl.json / prompts（换风格重做、换音频重做直接复用，省整轮转写+频谱）
- 已建每日 4:00 cron（job ef847199664f，静默 local）跑 `~/.hermes/profiles/p_1bab4a/scripts/cleanup_mv_data.py`：清 7 天前附件 + 各 mv2_* 任务的 parts/qc/imgs/final.mp4，脚本可手动跑
- **⚠️ 自动清理必须保护进行中任务**（2026-10-21 实测误删教训）：cleanup 脚本曾无条件删除所有 mv2_* 的 imgs/parts/final.mp4，把**还没交付**的 Plastic Love/暖暖 配图全删（渲染到一半帧目录消失→ENOSPC 崩溃、13+12 张图重出重新扣费）。修复规则：**只清理 7 天前创建的任务目录**（`os.stat(d).st_ctime < 7*86400` 跳过）——进行中任务当天创建，永不误删；手动清中间产物时同样先确认该任务已交付（项目目录有对应成片）再删 imgs/parts

## 纯音乐/无歌词 MV（2026-10-19 午夜之门～STAY WITH ME 实测）
- 触发：AI remix/合成器浪潮/氛围乐常是**新编词中英混唱或纯音乐**，无官方歌词可查、whisper 转写质量差（大量哼唱/乱码）。整段与分段转写都确认无可靠歌词时，**不要自作主张硬做歌词字幕**——先 clarify 三选项：用转写整理歌词（个别字可能有误）/ 用户提供歌词文本 / 不做歌词字幕（纯音乐 MV）
- **纯音乐模式流程**：图片时间轴按歌长均分（如 322s→12 张，每张≈27s）或按音乐结构分段；配图主题按歌名/意境发挥（午夜/霓虹/月光等氛围意象）；**跳过 ASS 叠字幕步骤**——final.mp4 = 三段渲染拼接后的 concat 片（render_all.py 最后 shutil.copy(mv2_concat.mp4 → final.mp4)）
- 交付说明：纯音乐无字幕版（用户选择）；后续想要歌词字幕可补歌词再叠

## 相关
- 底层脚本：~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts/（make_music_video.py + lyrics_segment.py + 模板）
- 配图：**picgirlsunny3 技能**（现代波普海报，按主题出图）
- mv1 技能（原始版本，图片均分；mvbpnew 与它独立，互不影响）
- **MV 配图风格家族（克隆扩展法）**：mvbpold(picbp 复古波普) / mvbpnew(picbpnew 现代波普) / mvgirlsunny3(picgirlsunny3 风格化数字插画美女·橙框墨镜蓝天) /  mvbpsky(picbpsky 日系二次元·新海诚) / mvbpdarkblue(picbpdarkblue 国潮深蓝夜色·鎏金) / mvbpnature(picbpnature 学术机制图·纯白底) / mvbpnsm(picbpnsm 鸟山明漫画·80-90年代) / mvbpsskey(picbpsskey 日系治愈动画·Sunny Bread) / mvbpsunny(picbpsunny 3D写实次世代·红蓝撞色·左上强侧光) / mvbpfirework(picbpfirework 夏日祭典华丽日系) / mvbp2sunny(picbp2sunny 3D写实次世代·纯主题驱动) / mvpicsun(picsun 日系写实美女·URI Dream Lab·主题派生式) / mvbpfgnew(picbpfgnew 新复古主义·New Retro Style：圆润胶囊几何/奶油米黄焦糖撞番茄红青蓝/棋盘格条纹/棚拍光长阴影) / mvbpzh(picbpzh 昭和复古未来·Showa Retro Future：高密度都市/霓虹/单轨列车/胶囊建筑/老电视/特摄，亮蓝白主调) / mvgirlfgnew(picgirlfgnew 新复古主义美女·主题派生式：每段 theme 派生美女+背景，左上角标题) / mvgirlzh(picgirlzh 昭和复古未来美女·亮蓝白) / mvlove(piclovesunny 3D写实多人物群像社论·全中文青年群像) / mvbpkt(picbpkt 复古犯罪片场景向·Pulp Crime Neo-noir·褪色绯红芥末黄烟草棕/35mm 胶片颗粒/高调布光明亮，老旧美式街巷/酒吧/霓虹/电话亭) / mvgirlkt(picgirlkt 复古犯罪片美女·主题派生式，v1.1.0 高亮版同 mvbpkt 画风)。用户要新风格时「生成技能 mvbpX = 克隆 mvbpnew 全文，仅把配图技能名/描述/配图小节换成 picbpX，其余流程/规则/铁律一字不动」——picbpX 技能族已有 30+ 风格模板，克隆即用，保留 mvbpnew 本身不动；克隆出的新 mvbp 若带专属配图要点（如 picbpsunny/picgirl 系安全提示：写实人物避开「紧身/身材线条/汗珠」措辞防 image2.5 安全审查拦截；picbp2sunny 是主题驱动长模板且**默认不加 FAFO 画面标注**；picsun/picgirlfgnew/picgirlzh 为写实人物主题派生、左上角超大标题=theme）一并带上
- **用户常拼错技能名**（实测 mvbpssky→mvbpsskey、mvbp Skyfall/mybpssky→mvbpsskey）：收到不存在的技能名时先对照家族列表找最近拼写，两个候选都可能时用 clarify 问一次再开工（音乐下载/转写可先并行做，不阻塞）
