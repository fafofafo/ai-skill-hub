---
name: mvy2kgirlhome
description: Use when 用户发MP3+歌词标题生成歌词同步MV（Y2K室内Frutiger Aero美女半身照配图，蓝白绿玻璃拟态）。频谱柱+歌词字幕+AI配图。
version: 1.0.0
metadata:
  license: MIT
---

# mvy2kgirlhome：MP3 + 歌词 → 歌词同步 MV（Y2K 室内 Frutiger Aero 美女半身照配图，蓝白绿）

原 mvgirly2k，2026-10-28 用户重命名为 **mvy2kgirlhome**（对齐 pic 系列 picy2kgirlhome 重命名，Y2K 女孩城市街头 MV）。

基于 mvbpnew 创建（2026-10-20 用户指定）：**唯一改动 = 配图从 picbpnew（现代波普）换成 picy2kgirlhome（Frutiger Aero 美女·蓝白绿玻璃拟态）**，其余流程/规则/铁律完全不变。mvbpnew 保留不动。

## 触发
- 用户发 MP3（背景乐）+ 歌词标题/歌名（可互联网搜索）→ 说"做MV/歌词同步MV"
- 输入：MP3 + 歌名（歌手名可附）

## 与 mvbpnew 的唯一区别
| | mvbpnew | mvy2kgirlhome |
|---|---|---|
| 配图技能 | **picbpnew**（现代波普）| **picy2kgirlhome**（Frutiger Aero 美女·主题派生式：玻璃拟态/气泡水滴/绿叶草坪/蓝天白云/蓝白绿三色/高精度3D渲染/仰视面部特写/数字光晕/治愈氛围）|
| 其余 | 图片公式/首末图/字幕/交付/外语歌 全部一致 | 同左 |

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
# 4. 每段主题 → picy2kgirlhome 逐段出图(Frutiger Aero 美女·蓝白绿, 用 segments.json 的 theme 字段, 每段一张 880x1184)
#    (调用见 picy2kgirlhome 技能; 图片按段序命名 img1.png..imgN.png)
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
- 中间各图主题：按歌唱时长均分窗口，每窗口取主唱歌词为 theme 交给 picy2kgirlhome 出图（**Frutiger Aero 美女·蓝白绿**，非现代波普）
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

## 相关
- 底层脚本：~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts/（make_music_video.py + lyrics_segment.py + 模板）
- 配图：**picy2kgirlhome 技能**（Frutiger Aero 美女·蓝白绿玻璃拟态，按主题出图）
- mvbpnew 技能（同流程，配图用 picbpnew 现代波普；本技能保留 mvbpnew 不动）
- mv1 技能（原始版本，图片均分；mvy2kgirlhome 与它独立，互不影响）
