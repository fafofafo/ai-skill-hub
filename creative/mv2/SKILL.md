---
name: mv2
description: Use when 用户发MP3+歌词标题要生成歌词同步MV（图片随歌词进度轮播）。频谱柱+歌词字幕+AI配图。
version: 1.0.0
metadata:
  license: MIT
---

# MV2：MP3 + 歌词 → 歌词同步 MV（图片轮播与歌词进度匹配）

基于 mv1 升级（2026-10-11 用户需求）。核心差异：**图片不是均分展示，而是按歌词段进度切换**——唱到哪句，就显示对应那句意境生成的图。

## 触发
- 用户发 MP3（背景乐）+ 歌词标题/歌名（可互联网搜索）→ 说"做MV/歌词同步MV"
- 输入：MP3 + 歌名（歌手名可附）

## B站链接取音频（常见输入，2026-10-22 实测 5/5）
用户发 bilibili.com/b23.tv 链接（带 ?t= 时间戳无妨）时，先按 bvid 取音频再走全流程。**用户只发「音乐：歌名 + 技能」（无链接无附件）时**：先 web_search「B站 <歌手> <歌名> 音频 完整版」确认一个完整版 bvid（首选标题含「无损/完整版」的音频向视频，勿选混剪/合集页），再走同一流程；b23.tv 短链用 `curl -sL -A "Mozilla/5.0" -o /dev/null -w "%{url_effective}"` 解出 BV 号。
- **裸 curl view API 间歇被风控**（code -412 request was banned）——不是链接错，是 B站风控；web_extract 同样可能被 412（CRAWL_HTTP_412），不必依赖它；直接冷却重试
- **稳定解法**：`sleep 30` 后带完整浏览器头重试 view：UA（Chrome 120 完整串）+ `Accept: application/json` + `Referer: https://www.bilibili.com/video/<bvid>` + `Origin: https://www.bilibili.com` + `Cookie: buvid3=...; buvid4=...`（buvid 可用固定占位值，不必真实）→ 拿 `title/duration/cid`
- 下载：`x/player/playurl?bvid=..&cid=..&fnval=16&fourk=1` 只需 UA + `Referer: https://www.bilibili.com/`（比 view 少被风控）；选 `bandwidth` 最大 audio 的 baseUrl → `audio.m4s` → `ffmpeg -y -v error -i audio.m4s -c:a libmp3lame -b:a 192k song.mp3`
- 视频标题常是「[风格] 歌名 | 番剧」等封面翻唱（如 [苏联风] 月光传说 / 英文填词 Cover / 胜利纪念版）——**标题里的语言标签提示实际演唱语言**，决定转写 language 与字幕方案（见外语歌处理）
- 工作目录统一 `/data/tmp_work/mv2_<歌名拼音>`；bvid/cid/标题记录在工作目录 view.json 留痕

## 与 mv1 的区别
| | mv1 | mv2 |
|---|---|---|
| 图片来源 | 用户发图 | **AI 生成**（picbp 按歌词意境出图）|
| 图片切换 | 按歌长均分 | **按歌词段时间轴**（唱到哪句显示哪张）|
| 歌词来源 | 用户提供 | web_search 搜官方歌词 |
| 图片数量 | 用户给几张用几张 | **我按歌词段数决定**（自然段，约 5-10 张）|

## 全流程（六步）
```bash
HERE=~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts
WORK=/tmp/mv2_job; mkdir -p $WORK
# 素材: song.mp3 + 歌名

# 1. web_search 查官方歌词(简体) → $WORK/lyrics.txt (空行分段, 每段=主歌/副歌等)
# 2. whisper 转录拿时间轴(只取时间, 文本不可信, 见 mv1 铁律)
HF_ENDPOINT=https://hf-mirror.com HF_HUB_DISABLE_XET=1 \
  python3 $HERE/make_music_video.py transcribe --audio $WORK/song.mp3 --out $WORK/ts.json
# 3. 歌词分段 → 图片时间轴 + 每段主题(核心句)
python3 $HERE/lyrics_segment.py --ts $WORK/ts.json --lyrics $WORK/lyrics.txt --out $WORK/segments.json
# 4. 每段主题 → picbp 逐段出图(用 segments.json 的 theme 字段, 每段一张 880x1184)
#    (调用见 picbp 技能; 图片按段序命名 img1.png..imgN.png)
# 5. 官方歌词→ASS 字幕(用 make_mv2_ass.py 或手写段映射, 简体/白字黑边; 勿用 make_music_video.py ass 子命令——段数>歌词行数时会重复显示)
python3 $HERE/make_mv2_ass.py --segments $WORK/segments.json --out $WORK/subs.ass
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
- **转写后先看 ts_full.json 时间轴（字段是 s/e 不是 start/end）**：B站取的音频可能含视频开场独白/片头，whisper 会把独白也转写出来，lyrics_segment.py 按句数比例映射会把歌词压缩到开头、末段异常长（典型症状：第一句歌词 start≈0、最后一段 end=全长）。若首段是旁白（0~16s 全是独白）→ 不用自动分段：抽 2-4 个时间点 ffmpeg 切片内联转写确认歌曲真正起点（第一句歌词时间），按 whisper 真实段边界手工构建 segments.json（首图 0→第一句歌词，中间段按主歌/副歌实际边界，末图=最后一张中间图保持到结尾），再走出图/渲染。
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
- 中间各图主题：按歌唱时长均分窗口，每窗口取主唱歌词为 theme 交给 picbp 出图
- 段数过多（>12）时合并相邻短段；过少（<4）时按句拆
- **单段上限**：公式算出后逐段检查时长，单段 >35s（长间奏/长副歌/长尾奏）必须再拆并加图，目标每段 20-33s——拆点选间奏边界或句子自然停顿，避免整段 40s+ 长时间一张呆图（长尾奏 80s+ 也要拆成两段以上）

### FPS 一致性（血泪坑）
- **模板 FPS 必须与渲染 --fps 一致**：viz_render 已自动注入 `const FPS = <fps>`；若手改模板勿用均分时代码
- 铁律继承自 mv1：headless 注入必须内联进 HTML；帧用 canvas.toDataURL 输出；长视频用 --format jpeg

### 同源音频重做（换风格/换技能）复用
- 用户重发同名 MP3（换配图风格/换 mvbp 变体重做）时先 `md5sum` 对比旧工作目录 `/data/tmp_work/mv2_*`（或项目目录 `~/项目目录/projects/<歌名>MV/`）的 song.mp3；**同源则复用 ts.json（whisper 时间轴）、segments.json（时间轴结构不变，仅把首图 theme 改为用户本次指定歌名）、subs.ass（外语歌中日对照），只重写配图提示词**后台出图——省一次 ~46s 转写和歌词搜索。
- 复用旧 subs.ass 必须重跑「>12 字拆行」检查：旧字幕可能早于换行规则（无 `\N`）；880px/margin40 下 CJK 13 字=780px 仍放得下，>13 字才必须 `\N` 拆行；JP/EN 行 Fontsize 小一般不受限。
- 复用旧 render_all.py：只改 WORK/PY 路径即可，PLANS/timeline/frames 因 segments 复用而保持不变。

### whisper 内联调用（抽段验证/外语歌指定语言）
- 模型路径必须传**完整 HF 缓存快照路径** `~/models/whisper/models--Systran--faster-whisper-small/snapshots/<hash>/`（传 `~/models/whisper/small` 报 HFValidationError「repo id 格式错误」）；配 `HF_HUB_OFFLINE=1` + `local_files_only=True` 防联网卡死。make_music_video.py transcribe 已封装，只有内联 `WhisperModel(...)` 才需要。

### 外语歌/粤语歌处理（2026-10-25 实测）
- 转写先判语言，标题语言标签直接提示（[英文版]/[粤语版]/日语原曲）；日语/英语/粤语歌 whisper zh 文本都不可信（**粤语尤其会转成近似普通话乱码**），只取时间轴
- 字幕方案：
  - 英/日语歌：主行中文翻译 + 副行原文对照（CN Fontsize52 MarginV250 上 / JP·EN Fontsize30 MarginV180 下，同帧两条）
  - 粤语歌：中文可懂，用官方粤语歌词（简体化）单行字幕
- 字幕颜色按配图底色定：浅亮底（sunny3 蓝天高调）用深灰字 &H00202020 + 白描边；彩色/青绿底（glass）用白字黑边

## 图片顺序铁律（继承 mv1）
- 图片按 segments.json 段序排列（img1=第1段, imgN=最后段），禁止按 mtime/尺寸排序
- 素材尺寸统一转 880×1184（居中裁切 cover 填充）

## 分段渲染脚本核对（血泪坑）
- 手写 render_all.py 的 PLANS：**imgs 列表与 timeline 的 i 索引必须逐一对应 segments.json 段序**，写完对照 segments.json 核对一遍——常见错误是 part 边界处漏图/错图、末图误用倒数第二张（part 内图片跨段边界时尤其容易）；本次 part4 曾写成 img7-img10、实为 img8-img11。
- timeline 的 s/e 是**相对该 part 起点的秒数**（绝对秒 − part 起点），不是绝对时间；frames = part 时长 × FPS。

## 成品规格（继承 mv1 用户拍板）
- 竖版 3:4（880×1184）；时长=歌全长
- 频谱柱：白字黑边，BAR_MAXH=150，44柱×14px，Attack 0.6/Decay 0.35，泛光 blur5
- 字幕：Fontsize 60 纯白+黑描边，简体中文官方歌词
- 交付：默认发 QQ 邮箱（mv1 流程），发后 IMAP 读回验证；**只发邮箱，不压缩、不发预览版，发完即结束**（用户 2026-10-13 确认）

## 验证清单（交付前）
- 抽 3-5 个歌词段起止时刻的帧：确认对应段图片已切换（不是均分）
- 歌词段边界无闪黑（交叉淡化生效）
- 字幕简体/样式正确、可读（底部频谱柱与字幕重叠是模板默认布局：柱 BAR_Y=H−14、顶 y≈1020，字幕 MarginV=110、底 y≈1074，白字黑边压在暖白柱上仍可读；勿改 MarginV、勿误判为缺陷，判定用 visual-production-qa 的收窄字幕带 OCR）
- 邮件 IMAP 读回确认送达（如走邮箱）

## 相关
- 底层脚本：~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts/（make_music_video.py + lyrics_segment.py + 模板）
- 配图：picbp 技能（复古波普海报，按主题出图）
- mv1 技能（原始版本，图片均分；mv2 与它独立，互不影响）
- **变体**：mvbpold（主频道维护的增强版，配图 picbp）、mvbpnew（= mvbpold 规则 + 配图 picbpnew 现代波普）；选型与完整规则见 pic-poster-family 的「mv2 变体」节——用户当场指定用哪套，配图风格决定用 picbp 还是 picbpnew。
- **配图切换**：若要求现代波普（无复古），把第 4 步的 picbp 换成 picbpnew，其余流程不变。
