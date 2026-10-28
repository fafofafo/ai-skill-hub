---
name: mvbpnew
description: Use when 用户发MP3+歌词标题生成歌词同步MV（现代波普配图）。频谱柱+歌词字幕+AI配图。
version: 1.0.0
metadata:
  license: MIT
---

# MVBPnew：MP3 + 歌词 → 歌词同步 MV（现代波普配图）

基于 mvbpold（mv2 增强版）创建（2026-10-15 用户指定）：**唯一改动 = 配图从 picbp（复古波普）换成 picbpnew（现代波普）**，其余流程/规则/铁律完全不变。mvbpold 保留不动。

## 触发
- 用户发 MP3（背景乐）+ 歌词标题/歌名（可互联网搜索）→ 说"做MV/歌词同步MV"
- 输入：MP3 + 歌名（歌手名可附）

## 与 mvbpold 的唯一区别
| | mvbpold | mvbpnew |
|---|---|---|
| 配图技能 | **picbp**（复古波普：半调网点/套印错位/复古招贴）| **picbpnew**（现代波普：干净轮廓/高饱和渐变/当代插画）|
| 其余 | 图片公式/首末图/字幕/交付/外语歌 全部一致 | 同左 |

## 音频来源（用户只给歌名、没发 MP3 附件时）
- 从 B站提取完整版音频：`bili search` CLI 对歌名常返回空（游客搜索受限）→ `web_search「歌名 bilibili」`拿 bvid（选 duration 接近原版完整时长）→ view/playurl API（完整 Chrome 头 + buvid3 cookie 绕 412）→ dash 音频选最高码率 m4s → curl 下载（带 Referer）→ ffmpeg 转 mp3。完整配方见 references/bilibili-audio-extraction.md
- ⚠️ **B站搬运源常含开场独白/口播**（2026-10-27 张宇《给你们》实测）：whisper 转写后若首段文本不是歌词、且自动分段把歌词挤到开头（末段异常长，如 59-280s），即错位——此时按 whisper 真实 s/e 时间手工构建 segments.json + ASS 字幕（配方见 references/bilibili-audio-extraction.md）

## 全流程（六步）
```bash
HERE=~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts
WORK=/tmp/mv2_job; mkdir -p $WORK
# 素材: song.mp3 + 歌名

# 1. web_search 查官方歌词(简体) → $WORK/lyrics.txt (空行分段, 每段=主歌/副歌等)
# 2. whisper 转录拿时间轴(只取时间, 文本不可信, 见 mv1 铁律)
#    ⚠️ 必须在装有 faster-whisper 的 venv 里跑，不能裸 python3：
#    - mv_venv 缺失/损坏时重建：python3 -m venv /tmp/mv_venv && /tmp/mv_venv/bin/pip install faster-whisper
#    - 加 PYTHONPATH= 前缀清掉 Hermes 注入的 3.14 site-packages（否则 venv 的 faster_whisper/av 报 ImportError）
#    - 验证环境用 `import faster_whisper` 而不是 pip show（ctranslate2 二进制不兼容时 pip show 有、import 仍报 ModuleNotFoundError）
#    - 首次转写含模型下载，322s 歌 CPU 转写约 5-10 分钟 → 必须后台跑 + notify，勿前台等
HF_ENDPOINT=https://hf-mirror.com HF_HUB_DISABLE_XET=1 PYTHONPATH= \
  /tmp/mv_venv/bin/python $HERE/make_music_video.py transcribe --audio $WORK/song.mp3 --out $WORK/ts.json
# 3. 歌词分段 → 图片时间轴 + 每段主题(核心句)
python3 $HERE/lyrics_segment.py --ts $WORK/ts.json --lyrics $WORK/lyrics.txt --out $WORK/segments.json
# 4. 每段主题 → picbpnew 逐段出图(现代波普, 用 segments.json 的 theme 字段, 每段一张 880x1184)
#    (调用见 picbpnew 技能; 图片按段序命名 img1.png..imgN.png)
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
- 切换点前后各 0.8s 交叉淡化（不闪断）

### 图片数量与主题（用户 2026-10-13 拍板，覆盖旧规则）
- **图片数量公式**：图片总数 = 1（首图）+ N（中间）+ 1（末图），其中 N = ceil(歌唱时长 / 25)
  - 歌唱时长 = 最后一句歌词结束 - 第一句歌词开始（whisper 时间轴）
  - 中间每张平均 20-25 秒：N = ceil(歌唱时长/25)，实际每张 ≈ 歌唱时长/N
- **首图**：以歌曲标题为主题生成（**纯歌名标题为画面主体**，不掺其他副主题，标题占视觉核心；用户 2026-10-13 明确），时长 = 视频开始 → 第一句歌词出现为止（整段前奏/间奏都放首图）
- **末图**：歌词结束后不再生成新图、不再切换，最后一张中间图保持到视频结束
- **不重复**：每张图在视频中只出现一次，禁止循环/重复使用同一张图；中间各图主题必须互不相同（副歌重复段也要换不同主题/换角度）
- 中间各图主题：按歌唱时长均分窗口，每窗口取主唱歌词为 theme 交给 picbpnew 出图（**现代波普**，非复古）
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
- 交付：默认发 QQ 邮箱（mv1 流程），发后 IMAP 读回验证；**只发邮箱，不发预览版，发完即结束**（用户 2026-10-13 确认）。**大小门槛**：本地 >33.75MB 时 base64×4/3 超 QQ 45MB 限制，必须 `ffmpeg -crf 28` 压一版发邮箱（原版+压缩版都归档项目目录，主题标明版本）——2026-10-26 光之奇旅 39MB/笑纳 35.5MB/小镇姑娘 36.3MB 均压 crf28 后交付

## 验证清单（交付前）
- 抽 3-5 个歌词段起止时刻的帧：确认对应段图片已切换（不是均分）
- 歌词段边界无闪黑（交叉淡化生效）
- 字幕简体/样式正确、与频谱柱不重叠
- 邮件 IMAP 读回确认送达（如走邮箱）

## 外语歌（日/英文）处理（2026-10-14 Dance In The Memories 实测）
- **转写语言**：make_music_video.py transcribe 硬编码 language=zh，外语歌必须自己内联 python 调 WhisperModel 指定 language（日文 ja、英文 en）；模型 small 日语时间轴够用（文本不可信铁律只取时间）
- **字幕**：中日/英中对照——主行=中文翻译（Style CN, Fontsize 52, MarginV 250），副行=原文（Style JP, Fontsize 30, MarginV 180），白字黑边，避开底部频谱柱（y>1020）
- **中文翻译自己译**：官方歌词只有原文，翻译按意境直译（简体、每句 ≤12 字）；ASS 段内均分每句时间（复用 make_mv2_ass.py 逻辑但双 Style）
- 歌名/主题：以用户指定为准；首图标题用歌名原文

## 纯音乐/无歌词（器乐版）处理（2026-10-25 实测）
- **检测**：whisper 转写结果全为乐器名（Zither Harp/Piano 等）即纯音乐版——**时间轴是否有值无关**（2026-10-26《Stay With Me》实测 37 条全 Zither Harp 但时间轴 4.76-317.66s 有值，仍是纯音乐，勿因时间轴有值误判为有歌词），判断标准=文本全是乐器名、无任何可同步歌词。直接问用户：图片轮播版 or 换带歌词文件（用户拍板后再继续）
- **图片轮播版流程**：不生成 ASS 字幕；手工生成均分 segments.json（`total_duration=歌长`，段数同公式 1首图+ceil(时长/25)+1末图，每段 theme 围绕歌名/氛围自定义，text 留空）→ 照常 viz-analyze + viz-render（切图+频谱柱）→ ffmpeg 不叠 ass 字幕
- **渲染中断恢复=全量重跑 viz-render**（2026-10-26《Stay With Me》实测）：会话中断后 _viz_frames/部分帧只是临时产物，无断点续传；恢复=重新执行完整 viz-render（--images 全部段图 + --tl + --timeline + --template），mv2.mp4 从头生成。渲染是 30fps×歌长帧数的 CPU 密集任务，恢复时后台跑 + notify，勿前台等

## 同曲换风格重做（用户「XX重新制作，mvYY」；2026-10-25/26 十余首实测）
- 复用 song.mp3 / ts_full.json / segments.json / subs.ass / tl.json，只重出图 + 重渲染
- **清目录三件套：`rm -rf imgs parts final.mp4 final_small.mp4 imgs_880`**——不只 parts/final，**旧 `imgs/` 必须一起清**（血泪坑：gen_imgs.sh 的「已存在跳过」会把上次任务遗留的旧图当新图用，新风格视频混进旧风格图，直到 QA 才发现）。判断 imgs 是否可复用看时间戳是否本次会话内；重做一律清掉最稳
- **字幕颜色按新配图底色调整**：暗底（军装/夜店/夜景图底部像素均值<100 时）用白字黑边（Style 主色 &H00FFFFFF + 黑边 &H00000000），浅底用深灰字白边；旧 subs.ass 是浅底深灰字时暗底上看不见。**改字幕颜色只需重跑 `ffmpeg -y -i parts/mv2_concat.mp4 -vf ass=subs.ass ... final.mp4`，不要重渲染帧**
- 重做渲染启动前确认 render_all.py 切分（CUTS/frames）与 segments 匹配；若中途改过 segments（如拆分长段）需同步改脚本

## 渲染中断/中途改图恢复
- **中断恢复=重跑 render_all.py**：脚本幂等，part*.mp3 与 tl_part*.json 已存在自动跳过，p1/p2/p3 帧目录 rmtree 后重渲；无断点续传，直接全量重跑（后台+notify）
- **中途改单张图（如末图标题错）**：process_manage kill 渲染进程 → 改该图提示词 → 单独重出该图（runhub_img.py t2i 前台重试至成功）→ 重转 imgs_880（含该图）→ 重跑 render_all.py
- 出图失败单张重试：gen_imgs.sh 内 5 次重试偶尔仍失败（img8 失败 5 次），脚本结束后前台单独补出（最多 8 次重试可成）；补出后转 imgs_880 再渲染

## QA 字幕可见性验证（叠字幕后的像素差分）
- **字幕带用 60%-95% 高度区间**，不是 60%-92%——MarginV 180/250 的对照字幕（中文上+原文下）落在更低位置，92% 截断会漏检
- **采样时刻必须选实际有歌词字幕的时间点**：歌词间隙/短字幕 fad 结束后无字幕是正常的（勿判失败）；先 grep subs.ass 的 Dialogue 起止时间，取其中有歌词的时刻采样
- 暗底图用深灰字时差分几乎为 0（字与底同色）——先看字幕区像素均值判断底色亮暗，再决定字幕颜色；白字黑边后差分应 >5000px

## 克隆 mvbpX 配图技能时的差异表保护（血泪坑，两次实测）
- 克隆=读 mvbpnew → 全局 `replace('picbpnew', 配图)`。但全局替换会把「与 mvbpnew 的唯一区别」表**左列**（mvbpnew 的 picbpnew）和家族列表里 `mvbpnew(picbpnew 现代波普)` 一起误换成配图技能名
- **正确顺序**：①先整体替换差异表为「与 mvbpnew 的唯一区别」新表；②用占位符 `@@KEEP_PICBPNEW@@` 保护新表左列的 picbpnew；③全局 `replace('picbpnew', 配图)`；④恢复占位符为 picbpnew；⑤单独把家族列表 `mvbpnew(picbpnew 现代波普)` 恢复并在其后追加新条目
- **验证看磁盘文件**（grep/wc/diff），不要信同一 cell 内存变量的布尔结果——实测 execute_code 变量显示 False/长度不符，磁盘内容实际正确
- **优先用「精简引用式」创建新 mvX 技能（2026-10-26 实测 mvsunny3/mvboysunny3，零坑）**：不要全量复制 mvbpnew 正文——正文长、全局 `replace('picbpnew', X)` 的差异表替换坑只在全量复制时出现。新技能 SKILL.md 精简结构：①frontmatter（description 一律「Use when 用户发MP3+歌词标题生成歌词同步MV（<风格>配图）。频谱柱+歌词字幕+AI配图。」）②一段声明「克隆 mvbpnew 全文，唯一改动=配图技能换成 picX，其余流程/规则/铁律一字不动」③触发④「与 mvbpnew 的唯一区别」两行表（只换配图技能一列）⑤六步全流程精简版（命令骨架）⑥继承的铁律列表逐条一行（图片公式/首末图/不重复/FPS 一致/图片顺序/字幕/交付/外语歌/换风格重做清 parts）⑦相关（配图技能+底层脚本+家族条目）。短而完整，未来维护只改配图技能名一处。用户命令「新技能，mvX」即按此创建，创建即用不阻塞后续 MV 流程
- **MV 风格技能家族命名规律**：`mvbpX`=场景（无人物）、`mvgirlX`=美女、`mvboyX`=帅哥、`mvX`（无 b/girl/boy）=人物肖像通用（如 mvsunny3）；对应配图技能 `picbpX/picgirlX/picboyX/picX`。技能会整族改名/拆细（如 mvbpglass→mvglassin/mvglassout 室内/室外两版），用户指定旧名时对照当前技能列表用新名执行

## whisper 转写环境（pyav 兼容 fix）
- faster-whisper 的 `audio.py` 调 `av.open(..., metadata_errors="ignore")`，pyav 19.x 不支持该参数 → `TypeError: open() got an unexpected keyword argument 'metadata_errors'`，进程会卡死（CPU 0%）或直接报错。修复：patch `faster_whisper/audio.py` 去掉 `metadata_errors="ignore"`（或装新版 av）
- 转写卡住时先看 CPU：CPU 0% 且 huggingface 缓存不再增长 = 卡在 decode，不是模型下载，杀进程查 pyav 版本
- **手工内联 WhisperModel 必须用完整快照路径**：`~/models/whisper/models--Systran--faster-whisper-small/snapshots/<hash>`（`~/models/whisper/small` 简写报 HFValidationError「Repo id must be in the form」；用 `find ~/models/whisper/models--Systran--faster-whisper-small -name model.bin` 定位）。参数：WhisperModel(路径, device="cpu", compute_type="int8", local_files_only=True)，环境 HF_HUB_OFFLINE=1 HF_HUB_DISABLE_XET=1 PYTHONPATH=

## 相关
- 底层脚本：~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts/（make_music_video.py + lyrics_segment.py + 模板）
- 配图：**picbpnew 技能**（现代波普海报，按主题出图）
- mv1 技能（原始版本，图片均分；mvbpnew 与它独立，互不影响）
- mvbpold 技能（同流程，配图用 picbp 复古波普；本技能保留 mvbpold 不动）
