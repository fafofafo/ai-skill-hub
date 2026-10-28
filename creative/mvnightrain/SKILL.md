---
name: mvnightrain
description: Use when 用户发MP3+歌词标题生成歌词同步MV（深夜细雨海边公路美女配图）。频谱柱+歌词字幕+AI配图。
version: 1.0.0
metadata:
  license: MIT
---

# MVNightrain：MP3 + 歌词 → 歌词同步 MV（深夜细雨海边公路美女配图）

基于 mvbpnew 创建（2026-10-27 用户指定）：**唯一改动 = 配图从 picbpnew（现代波普）换成 picnightrain（深夜细雨海边公路昭和美女，主题派生式）**，其余流程/规则/铁律完全不变。mvbpnew/mvbpold 保留不动。

## 触发
- 用户发 MP3（背景乐）+ 歌词标题/歌名（可互联网搜索）→ 说"做MV/歌词同步MV"
- 输入：MP3 + 歌名（歌手名可附）
- 风格词：深夜细雨/雨夜公路/海边公路/昭和雨夜美女配图 MV

## 与 mvbpnew 的唯一区别
| | mvbpnew | mvnightrain |
|---|---|---|
| 配图技能 | **picbpnew**（现代波普：干净轮廓/高饱和渐变/当代插画）| **picnightrain**（深夜细雨海边公路昭和美女：主题派生式，每段 theme 派生昭和80年代时尚装美女+深夜细雨海边城市公路、左上角超大标题=theme、温柔浅笑表情）|
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
# 4. 每段主题 → picnightrain 逐段出图(深夜细雨海边公路美女, 用 segments.json 的 theme 字段, 每段一张 880x1184)
#    (调用见 picnightrain 技能; 图片按段序命名 img1.png..imgN.png)
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

## 继承铁律（逐条来自 mvbpnew/mv2，一字不改）
- **图片数量公式**：1（首图）+ N（中间，N=ceil 歌唱时长/25）+ 1（末图）；首图=纯歌名标题为主题（标题占视觉核心），末图=最后一张中间图保持到结束；不重复、中间各图主题互不相同
- **图片时间轴**：lyrics_segment.py 官方歌词按空行分段 → 每段时长按句数比例映射到 whisper 时间轴；切换点前后各 0.8s 交叉淡化
- **FPS 一致性**：模板 FPS 必须与渲染 --fps 一致（viz_render 自动注入 `const FPS=<fps>`）；headless 注入内联进 HTML；帧用 canvas.toDataURL；长视频 --format jpeg
- **图片顺序铁律**：按 segments.json 段序排列（img1=第1段, imgN=最后段），禁止按 mtime/尺寸排序；素材统一转 880×1184 cover 填充
- **成品规格**：竖版 3:4、时长=歌全长；频谱柱白字黑边 BAR_MAXH=150 44柱×14px Attack 0.6/Decay 0.35 泛光 blur5；字幕 Fontsize 60 纯白黑描边简体，长句 `\N` 换行每行 ≤12 汉字
- **交付**：默认发 QQ 邮箱（mv1 流程）+ IMAP 读回验证；只发邮箱不压缩不发预览版
- **外语歌**：transcribe 硬编码 language=zh，外语歌内联调 WhisperModel 指定语言；字幕中日/英中对照（主行中文 Fontsize 52 MarginV 250、副行原文 Fontsize 30 MarginV 180）
- **纯音乐/无歌词**：whisper 转写全为乐器名即纯音乐版，直接问用户（图片轮播版 or 换带歌词文件）；图片轮播版=不生成 ASS、手工均分 segments.json、照常 viz-analyze + viz-render、ffmpeg 不叠字幕；渲染中断恢复=全量重跑 viz-render（无断点续传）
- **whisper 环境**：pyav 19.x 报 `metadata_errors` TypeError 时 patch faster_whisper/audio.py 去掉该参数（或装新版 av）

### picnightrain 出图要点（本技能特有）
- 每段 theme 作为 picnightrain 主题：自动派生「1 个日本1980年代昭和年轻美女 + 深夜细雨海边城市公路」，左上角超大主标题=theme（bold 立体挤压现代波普艺术字，第一视觉焦点，不能写错字）
- 画风固定保留：数字插画 3D 渲染 + 昭和80年代时尚装扮（风衣/连衣裙/牛仔等）+ 复古配饰 + 温柔浅笑表情 + 海边公路/海岸城市夜景/湿润路面倒影/细雨/路灯/霓虹招牌 + 冷暖霓虹各半 + 高调明亮布光（明度验收 40-55%，写「高调明亮布光+无大面积死黑+路面反光明亮」三件套）
- 末尾固定带「右上角粗体字标注：FAFO工作室」
- 默认出图：image2.5 sunburst (2098218128315609089)，880x1184 竖版（默认约 3:4）

## 验证清单（交付前）
- 抽 3-5 个歌词段起止时刻的帧：确认对应段图片已切换（不是均分）
- 歌词段边界无闪黑（交叉淡化生效）
- 字幕简体/样式正确、与频谱柱不重叠
- 邮件 IMAP 读回确认送达（如走邮箱）

## 相关
- 底层脚本：~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts/（make_music_video.py + lyrics_segment.py + 模板）
- 配图：**picnightrain 技能**（深夜细雨海边城市公路昭和美女数字插画，主题派生式，昭和80年代时尚装+温柔浅笑+雨夜霓虹）
- mvbpnew 技能（同流程，配图用 picbpnew 现代波普）
- mvbpold 技能（同流程，配图用 picbp 复古波普）
- mv1 技能（原始版本，图片均分；mvnightrain 与它独立，互不影响）
