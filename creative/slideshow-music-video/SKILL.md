---
name: slideshow-music-video
description: Use when 图片序列+背景乐→轮播视频，Ken Burns 动态化+歌词字幕对齐。含 ffmpeg 配方与踩坑。
---

# 图文配乐视频合成（ffmpeg 本地出片）

## When to Use
- 用户给 N 张图片 + 背景乐 → 按序轮播成 MP4（幻灯片/MV 风格）
- 需要 Ken Burns 运镜让静态图动态化、歌词/字幕与音乐对齐

## 流程（按序）

### 1. 定序与替换
- 图片按上传时间排序：`ls -la --time-style=full-iso`（精确到纳秒）
- 用户说"第 N 张替换成 X" → 按时间序替换对应位置（替换图通常时间戳晚于原图）
- 尺寸统一检查（PIL identify）；保持原图尺寸输出（不放大防糊）

### 2. 规格确认（clarify 一次，避免返工）
- 时长：默认=背景乐全长；或短视频。问清"整首/60s/30s"
- 每张图时长 = 音乐全长 ÷ 张数（不卡点则均分）

### 3. Ken Burns 运镜（zoompan 配方）
```
zoompan=z='1.08+0.08*sin(on/100)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=<帧数>:s=<WxH>:fps=25
```
- ⚠️ **z 表达式永不能让 zoom<1**：sin 摆动必须加基线（1.08+0.08*sin），否则 zoom<1 时 zoompan 输出黑边+画面静止（后端一半时间不动）
- ⚠️ 不能用 `min(zoom+0.0004,1.15)` 线性放大：到封顶后后半段静止
- 每张图错相位（+1.57/+3.14/+4.71…）制造变化
- 单图输入 + `d=帧数`（帧数=秒×25fps）展开

### 4. 歌词字幕（ASS）
- **时间轴必须实测对齐**：全局平均时间轴（总长÷行数）用户会说"对不上"。用 ASR 实测：
  - 音频切割成 13s 段：`-ss` **放 -i 之后**（输出端精确 seek）——放 -i 前 mp3 快速 seek 不精确导致段序错乱
  - ASR 用硅基流动 `Qwen/Qwen3-ASR-1.7B`（**SenseVoiceSmall 漏词严重不可用**，Qwen3 连续完整）
  - 每段转录 → 歌词行映射到段边界 → 每句起止 ±1-2s；空段（间奏）不排字幕
- **字幕位置顶部**：图片底部常自带文字（postcard 署名/标语），字幕放底部必叠字——`Alignment: 8`（顶部居中）+ `MarginV: 90`
- **视效**：`{\fscx115\fscy115\t(0,250,\fscx100\fscy100)\fad(250,400)}` 弹出落定+淡入淡出；`BorderStyle: 3` 半透明黑底（BackColour &H8C000000）
- 样式：Microsoft YaHei 56、粗体 -1、白字

### 5. 渲染与体积
```
ffmpeg -y -v error -i img1.png ... -i img6.png -i music.mp3 \
 -filter_complex "[0:v]zoompan=...[v0];...[v0]...[v5]concat=n=6:v=1:a=0[vcat];[vcat]ass=sub.ass[vout]" \
 -map "[vout]" -map <音频索引>:a -c:v libx264 -preset medium -crf 28 -pix_fmt yuv420p -c:a aac -b:a 128k -shortest out.mp4
```
- ⚠️ **动态化让体积暴涨是正常**：静态图相邻帧相同（H.264 帧间压缩白赚），Ken Burns 每帧都变 → 同样 CRF 体积大 5-7 倍（22MB→144MB）。**CRF 20→28 降 ~72%**，视觉差异小。QQ 邮箱附件限 50MB，超了 CRF 28 压
- 复用已渲染视频流时（只改字幕）：`-i final.mp4 -i music -filter_complex "[0:v]ass=sub.ass[vout]"` 不重跑 zoompan
- 大渲染后台跑（notify_on_complete）

### 6. 验证（抽帧 + vision）
- 抽帧：`-i file -vf "select='eq(n,帧号)'" -vsync 0 -frames:v 1`（精确帧索引）或 `-i file -ss N -frames:v 1`（精确 seek）
- ⚠️ **全图 vision 会把图片自带文字误当字幕**——看字幕用 region 裁剪：`region=[0,50,880,420]` 聚焦字幕区
- 动态效果验证：相邻帧中心区像素差（PIL 采样，>3 为动态）；zoom<1 黑边检查角落非纯黑

### 7. 交付
- 企微：`MEDIA:/abs/path`；邮箱：smtplib QQ（见 scripts/send_qq_mail.py 模板）
- 用户默认"直接发邮箱"——发了就报"已发并 IMAP 验证"，不要问要不要发

## Pitfalls（通用规则）
- ASR 校准字幕必须实测时间轴，别用均分——用户能听出对不上
- 字幕避开图片自带文字（底部文字→字幕放顶部）
- zoompan 永不下 1.0（黑边+静止）
- 大附件 SMTP 超时→timeout 300
- mp3 -ss 精确 seek 放 -i 后
