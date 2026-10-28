---
name: mvrainnight
description: Use when 用户发MP3+歌词标题生成歌词同步MV（居家雨夜女配图）。频谱柱+歌词字幕+AI配图。
version: 1.0.0
metadata:
  license: MIT
---

# MVRainnight：MP3 + 歌词 → 歌词同步 MV（居家雨夜女配图）

基于 mvbpnew 创建（2026-10-26 用户指定）：**唯一改动 = 配图从 picbpnew（现代波普）换成 picrainnight（居家雨夜女数字插画，主题派生式）**，其余流程/规则/铁律完全不变。mvbpnew/mvbpold 保留不动。

## 触发
- 用户发 MP3（背景乐）+ 歌词标题/歌名（可互联网搜索）→ 说"做MV/歌词同步MV"
- 输入：MP3 + 歌名（歌手名可附）
- 风格词：居家/雨夜/室内窗景配图 MV

## 与 mvbpnew 的唯一区别
| | mvbpnew | mvrainnight |
|---|---|---|
| 配图技能 | **picbpnew**（现代波普：干净轮廓/高饱和渐变/当代插画）| **picrainnight**（居家雨夜女数字插画：主题派生式，每段 theme 派生居家美女+室内雨夜窗景、左上角超大标题=theme、居家休闲装+窗外雨夜城市灯火）|
| 其余 | 图片公式/首末图/字幕/交付/外语歌 全部一致 | 同左 |

## 全流程（六步）
```bash
HERE=~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts
WORK=/tmp/mv2_job; mkdir -p $WORK
# 素材: song.mp3 + 歌名

# 1. web_search 查官方歌词(简体) → $WORK/lyrics.txt (空行分段, 每段=主歌/副歌等)
# 2. whisper 转录拿时间轴(只取时间, 文本不可信, 见 mv1 铁律)
HF_ENDPOINT=https://hf-mirror.com HF_HUB_DISABLE_XET=1 PYTHONPATH= \
  python3 $HERE/make_music_video.py transcribe --audio $WORK/song.mp3 --out $WORK/ts.json
# 3. 歌词分段 → 图片时间轴 + 每段主题(核心句)
python3 $HERE/lyrics_segment.py --ts $WORK/ts.json --lyrics $WORK/lyrics.txt --out $WORK/segments.json
# 4. 每段主题 → picrainnight 逐段出图(居家雨夜女, 用 segments.json 的 theme 字段, 每段一张 880x1184)
#    (调用见 picrainnight 技能; 图片按段序命名 img1.png..imgN.png)
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

## 关键实现（mv2 专属，与 mvbpnew 一致）
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
- 中间各图主题：按歌唱时长均分窗口，每窗口取主唱歌词为 theme 交给 picrainnight 出图（**居家雨夜女**，主题派生式）
- **第一张图 = 歌曲标题为主题创作**（用户 2026-10-12 偏好：标题占画面主体，配主题意象环绕）
- 段数过多（>12）时合并相邻短段；过少（<4）时按句拆

### picrainnight 出图要点（本技能特有）
- 每段 theme 作为 picrainnight 主题：自动派生「1 个居家美女主体 + 室内雨夜窗景」，左上角超大主标题=theme（bold 立体挤压现代波普艺术字，第一视觉焦点，不能写错字）
- 画风固定保留：数字插画 3D 渲染 + 居家休闲装（奶黄/暖粉/淡蓝毛衣卫衣）+ 室内暖光+窗外雨夜冷蓝 + 高调明亮 + 冷暖平衡（R-B 平衡口诀：冷暖各半最快收敛）
- 末尾固定带「右上角粗体字标注：FAFO工作室」
- 默认出图：image2.5 sunburst (2098218128315609089)，880x1184 竖版（默认约 3:4）

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
- 交付：默认发 QQ 邮箱（mv1 流程），发后 IMAP 读回验证；**只发邮箱，不压缩、不发预览版，发完即结束**（用户 2026-10-13 确认）

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
- **检测**：whisper 转写结果全为乐器名（Zither Harp/Piano 等）且时间轴全 0 → 纯音乐版，无歌词可同步。直接问用户：图片轮播版 or 换带歌词文件（用户拍板后再继续）
- **图片轮播版流程**：不生成 ASS 字幕；手工生成均分 segments.json（`total_duration=歌长`，段数同公式 1首图+ceil(时长/25)+1末图，每段 theme 围绕歌名/氛围自定义，text 留空）→ 照常 viz-analyze + viz-render（切图+频谱柱）→ ffmpeg 不叠 ass 字幕

## 克隆 mvbpX 配图技能时的差异表保护（血泪坑，两次实测）
- 克隆=读 mvbpnew → 全局 `replace('picbpnew', 配图)`。但全局替换会把「与 mvbpnew 的唯一区别」表**左列**（mvbpnew 的 picbpnew）和家族列表里 `mvbpnew(picbpnew 现代波普)` 一起误换成配图技能名
- **正确顺序**：①先整体替换差异表为「与 mvbpnew 的唯一区别」新表；②用占位符 `@@KEEP_PICBPNEW@@` 保护新表左列的 picbpnew；③全局 `replace('picbpnew', 配图)`；④恢复占位符为 picbpnew；⑤单独把家族列表 `mvbpnew(picbpnew 现代波普)` 恢复并在其后追加新条目
- **验证看磁盘文件**（grep/wc/diff），不要信同一 cell 内存变量的布尔结果——实测 execute_code 变量显示 False/长度不符，磁盘内容实际正确

## whisper 转写环境（pyav 兼容 fix）
- faster-whisper 的 `audio.py` 调 `av.open(..., metadata_errors="ignore")`，pyav 19.x 不支持该参数 → `TypeError: open() got an unexpected keyword argument 'metadata_errors'`，进程会卡死（CPU 0%）或直接报错。修复：patch `faster_whisper/audio.py` 去掉 `metadata_errors="ignore"`（或装新版 av）
- 转写卡住时先看 CPU：CPU 0% 且 huggingface 缓存不再增长 = 卡在 decode，不是模型下载，杀进程查 pyav 版本

## 相关
- 底层脚本：~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts/（make_music_video.py + lyrics_segment.py + 模板）
- 配图：**picrainnight 技能**（居家雨夜女数字插画，主题派生式，居家休闲装+室内雨夜窗景）
- mvbpnew 技能（同流程，配图用 picbpnew 现代波普）
- mvbpold 技能（同流程，配图用 picbp 复古波普）
- mv1 技能（原始版本，图片均分；mvrainnight 与它独立，互不影响）
