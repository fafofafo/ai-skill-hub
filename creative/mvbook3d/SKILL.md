---
name: mvbook3d
description: Use when 用户发MP3+歌词标题生成歌词同步MV（3D纸雕立体书配图）。频谱柱+歌词字幕+AI配图。
version: 1.0.0
metadata:
  license: MIT
---

# MVBOOK3D：MP3 + 歌词 → 歌词同步 MV（3D纸雕立体书配图）

克隆 mvbpnew 全文，唯一改动=配图技能换成 picbook3d，其余流程/规则/铁律一字不动。

## 触发
- 用户发 MP3（背景乐）+ 歌词标题/歌名（可互联网搜索）→ 说"做MV/歌词同步MV"
- 输入：MP3 + 歌名（歌手名可附）

## 与 mvbpnew 的唯一区别
| | mvbpnew | mvbook3d |
|---|---|---|
| 配图技能 | **picbpnew**（现代波普艺术拼贴） | **picbook3d**（3D纸雕立体书旅行插画） |
| 其余 | 图片公式/首末图/字幕/交付/外语歌 全部一致 | 同左 |

## 全流程（六步）
```bash
HERE=~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts
WORK=/tmp/mv2_job; mkdir -p $WORK
# 素材: song.mp3 + 歌名

# 1. web_search 查官方歌词(简体) → $WORK/lyrics.txt (空行分段, 每段=主歌/副歌等)
# 2. whisper 转录拿时间轴(只取时间, 文本不可信, 见 mv1 铁律)
HF_ENDPOINT=https://hf-mirror.com HF_HUB_DISABLE_XET=1 PYTHONPATH= \
  /tmp/mv_venv/bin/python $HERE/make_music_video.py transcribe --audio $WORK/song.mp3 --out $WORK/ts.json
# 3. 歌词分段 → 图片时间轴 + 每段主题(核心句)
python3 $HERE/lyrics_segment.py --ts $WORK/ts.json --lyrics $WORK/lyrics.txt --out $WORK/segments.json
# 4. 每段主题 → picbook3d 逐段出图(3D纸雕立体书, 用 segments.json 的 theme 字段)
#    (调用见 picbook3d 技能; 图片按段序命名 img1.png..imgN.png)
# 5. 官方歌词→ASS 字幕(复用 mv1 make_official_ass.py 逻辑)
python3 $HERE/../mv2/scripts/make_official_ass.py
# 6. 渲染: 时间轴驱动切图 + 频谱柱 + 叠字幕
python3 $HERE/make_music_video.py viz-analyze --audio $WORK/song.mp3 --out $WORK/tl.json
python3 $HERE/make_music_video.py viz-render --images img1.png,...,imgN.png \
  --audio $WORK/song.mp3 --tl $WORK/tl.json \
  --timeline $WORK/segments.json --template sketch_viz_template_mv2.html \
  --out $WORK/mv2.mp4 --fps 30 --format jpeg
ffmpeg -y -v error -i $WORK/mv2.mp4 -vf "ass=$WORK/subs.ass" \
  -c:v libx64 -preset medium -crf 23 -pix_fmt yuv420p -c:a copy -movflags +faststart $WORK/final.mp4
```

## 继承的铁律（从 mvbpnew 原样继承）
- 图片数量公式：1首图 + ceil(歌唱时长/25)中间 + 1末图
- 首图 = 歌曲标题为主题；末图 = 最后一张中间图保持到结束
- 不重复：每张图只出现一次
- FPS 一致性：模板 FPS 必须与渲染 --fps 一致
- 图片顺序：按 segments.json 段序排列
- 字幕：简体中文官方歌词，白字黑边，长句自动换行
- 交付：默认发 QQ 邮箱，发后 IMAP 读回验证

## 相关
- 底层脚本：~/.hermes/profiles/learn/skills/creative/musicvideo2/scripts/
- 配图：**picbook3d 技能**（3D纸雕立体书旅行插画）
- mvbpnew 技能（现代波普配图，本技能保留不动）
- mvbpold 技能（复古波普配图，同流程独立）
