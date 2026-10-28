---
name: image-slideshow-video
description: Use when 图片+背景乐做 MV/幻灯片视频（Ken Burns 动态+歌词字幕）。ffmpeg 全流程。
---

# 图片幻灯片 MV 视频（ffmpeg）

## When to Use
- 用户给 N 张图片（按顺序）+ 一段音乐，要做成视频（浪漫 MV / 产品轮播 / 纪念卡点 / 图文转视频）
- 用户要求"图片动态化"（Ken Burns 运镜）+ "配字幕"（歌词或文案）

## 流程（按顺序）
1. **确认素材顺序**：图片上传顺序 = 缓存目录的 mtime（`ls --time-style=full-iso` 纳秒级排序，最早=第 1 张）。文件名不可靠，mtime 是唯一可信顺序。后补的"替换图" mtime 更晚，替换到对应位。
2. **确认规格**（先问清，避免整条重渲）：
   - 视频时长：默认 = 背景乐全长；每张时长 = 总长/N（用户不卡点就平均分配）
   - 分辨率/比例：查原图尺寸（PIL/identify），常见竖版卡片 880x1184 (3:4)；zoompan 输出 s=同尺寸
   - 字幕内容：歌词（用户给全文 / ASR 转录）还是指定文案；浮现效果
3. **生成 ASS 字幕**（歌词逐行浮现）→ `references/lyrics-subtitle-ass.md`；直接跑 `scripts/gen_lyrics_ass.py 歌词.txt --total 298 --start 8 --out /tmp/lyrics.ass`（免手算时间戳）
4. **ffmpeg 渲染**：每张图一个 zoompan 段（Ken Burns）→ concat → ass 烧录 → 音乐 `-shortest`
5. **验证**：ffprobe duration/尺寸/nb_frames；指定时间抽帧 + vision 确认首帧顺序正确 + 字幕出现；md5 对比各帧确认每张图不重复/不错位

## 关键命令骨架（6 图 + 1 mp3）
```bash
ffmpeg -y -i img1 -i img2 ... -i img6 -i bgm.mp3 \
 -filter_complex "[0:v]zoompan=z='1.08+0.08*sin(on/100)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1243:s=880x1184:fps=25[v0];...\
 [v0][v1]...[v5]concat=n=6:v=1:a=0[vcat];[vcat]ass=/tmp/lyrics.ass[vout]" \
 -map "[vout]" -map 6:a -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest out.mp4
```
- 每张帧数 `d` = 每张秒数 × fps（49.7s×25 ≈ 1243）；图片用单帧输入（`-i img.png` 无 loop），zoompan d 展开成帧
- 字幕文件必须在渲染前生成好（ass 过滤器读路径）
- **z 表达式必须永远 ≥1.0**（见 Pitfall 1）

## Pitfalls（血泪）
1. **zoompan z 封顶 = 后半段静止**：`z='min(zoom+0.0004,1.15)'` 到 1.15 后不再变化——几十秒的长段后半程完全静止，观感像卡住，必须整条重渲。
2. **sin 摆动必须保证 z≥1.0（修正版已验证）**：`z='1+0.12*sin(on/100)'` 会下穿 1.0——zoom<1 时 zoompan 输出黑边+画面静止（实测第 1 段内帧 0 vs 100 差 49 正常，但帧 500 vs 625 差 0.0）。**唯一可靠公式：`z='1.08+0.08*sin(on/100)'`**（zoom 1.0~1.16，全程动态无黑边）；每张错相位（`+0 / +1.57 / +3.14 / +4.71 / +0.785 / +2.36`）制造变化。
3. **顺序恢复靠 mtime 不靠文件名**：缓存文件名随机，只有 mtime 纳秒级可信；替换图单独确认。
4. **字幕时长**：默认平均分配（不卡点）；但用户要求"和语音同步"时，必须 ASR 实测逐句对齐（Qwen3-ASR 按 ~13s 分段转录，每句定位到 ±1-2s），勿平均——平均分配与真实演唱位置可差 25s+，用户会听出不对。前奏/间奏（无歌词段）不留字幕。
5. **单帧验证不出 Ken Burns**：抽一帧看是静态构图，看不出"在动"；动态靠 zoompan 数学确认（每帧 zoom 在变）或连续两帧对比中心内容位移。
6. **验证动态用帧索引，别用快速 seek**：`-ss N -i file`（-i 前）是快速 seek 落到 keyframe（GOP 内不精确）→ 抽到同一帧误判"没动态"（实测 20s/25s 帧差 0.0 其实是同 keyframe）。用 `-i file -vf "select='eq(n,N)'" -vsync 0 -frames:v 1` 精确帧索引，或 `-i file -ss N`（-i 后精确 seek）。
7. **验证动态 = 相邻帧像素差**：PIL 抽两帧中心区算 RGB 平均差（>3 动态正常，0=静止）。**单图 zoompan 测试有效 ≠ 完整 filter 链有效**（单图 48.3 差但完整链 0.0）——完整渲染后必须抽帧验证。
8. **-shortest 对齐**：视频流略短于音乐时用 -shortest 收尾；验证 duration≈音乐时长。
9. **大渲染后台跑**：298s/7452 帧中等 preset 在 2C4G 机器要几分钟——用 background=true + notify_on_complete，别前台死等。
10. **交付注意**：**默认只发邮箱，未主动要求不发企微**（2026-09 用户定）；用户要企微预览才用 `MEDIA:/abs/path.mp4`；QQ 邮箱单封附件 ≤50MB（100MB+ 视频先压 1080p 或分段）；smtplib 发 smtp.qq.com:465 大附件 timeout 必须 ≥300s（60s write timeout 断连）；发完用 IMAP 读回验证（imap.qq.com:993 同授权码）；授权码不写进任何文件/备份。
11. **字幕必须从原始素材一步渲染**：从"已烧字幕的视频"再叠 ass = 旧字幕已烧进画面无法清除（用户会看到两层字幕叠加）。任何版本迭代都回到原图 + 原音乐整条重拼，绝不拿已带字幕的 mp4 当源。
12. **图片自带文字会撞字幕**：postcard/海报类图底部常有署名/文案（如"特别的爱你给特别的你"），底部字幕直接叠上去。渲染前先 vision 看图片内容；撞了就把字幕移顶部/上移，或与用户确认能否接受。
13. **ASS BorderStyle=3（半透明黑底框）渲染不稳定**（libass 兼容问题，效果时有时无）；要可读性用 BorderStyle=1 黑描边+阴影（Outline=3, Shadow=1）更稳。

## 参考
- `references/lyrics-subtitle-ass.md` — ASS 歌词字幕模板（\fad 浮现 / 时间轴 / 前奏延迟）+ 用硅基流动 ASR 从背景乐转录歌词
