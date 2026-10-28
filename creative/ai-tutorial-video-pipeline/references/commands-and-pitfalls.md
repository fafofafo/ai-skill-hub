# 命令与错误实录（AI 教程视频流水线）

## 一次性环境搭建（腾讯云已验证）
```bash
# 1) 中文字体（关键：否则 drawtext / PIL 中文全变方块）
sudo apt-get install -y fonts-wqy-zenhei
# 验证：fc-list | grep -i wqy
# 路径：/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc

# 2) Python 环境（PEP 668 禁止系统 pip，用 uv venv）
~/.hermes/bin/uv venv ~/video-venv
~/.hermes/bin/uv pip install --python ~/video-venv/bin/python \
  -i http://mirrors.tencentyun.com/pypi/simple pillow edge-tts
# 腾讯镜像加速；镜像缺少上传日期，勿用 exclude-newer
```

## edge-tts 关键点与限流实录

**错误**：`edge_tts.exceptions.NoAudioReceived: No audio was received`
- 现象：CLI 单条生成成功（`edge-tts --voice zh-CN-YunxiNeural --text "测试" --write-media /tmp/x.mp3`），但 Python 库**批量**连续调用时随机报 NoAudioReceived。
- 根因：edge-tts 免费服务对高频连续请求限流。
- 修复（已验证）：每段重试最多 4 次、退避 3s×attempt；段与段之间 `sleep 2`。
  ```python
  async def tts(text, out, voice, retries=4):
      import edge_tts
      for attempt in range(1, retries + 1):
          try:
              await edge_tts.Communicate(text, voice).save(str(out))
              if out.stat().st_size > 2000: return
              raise RuntimeError("音频过小")
          except Exception as e:
              await asyncio.sleep(3 * attempt)
      raise RuntimeError("TTS 多次失败")
  ```
- 可靠 voice：`zh-CN-YunxiNeural`（男声，默认）、`zh-CN-XiaoxiaoNeural`（女声）。

## PIL 生成中文信息卡
- 加载 ttc：`ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", size, index=0)`（Pillow 支持 ttc，index=0=WenQuanYi Zen Hei）
- 卡片结构（1920×1080）：顶部大标题（居中，超长自动缩字号，`while f.getlength(card) > W-320 and size>56: size-=4`）→ 副标题 → 分隔线 → 要点列表（发光圆点 `d.ellipse` + 文字，逐字 wrap 换行）→ 底部圆角信息条（关键命令/副语）
- 背景：垂直渐变（逐行 `d.line`）+ 半透明光斑（RGBA overlay + GaussianBlur 140）+ alpha_composite

## ffmpeg 合成
- drawtext 用 ttc 渲染中文：`drawtext=fontfile=/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc:text='中文':fontcolor=white`（已验证 OK）
- 单段合成（图片+音频，时长=音频）：
  ```
  ffmpeg -y -i img.png -i seg.mp3 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x12121e,fade=t=in:st=0:d=0.4,fade=t=out:st=D-0.4:d=0.4" -map 0:v -map 1:a -t D -c:v libx264 -preset fast -c:a aac -b:a 160k -pix_fmt yuv420p clip.mp4
  ```
- 拼接：`-f concat -safe 0 -i list.txt -c copy out.mp4`（list.txt 每行 `file 'clip.mp4'`）
- **关键坑**：信息卡/图片本身已含标题时，**不要**再叠 drawtext 标题（会重叠）→ 用 `--notitle` 模式只留 fade。
- 图片比例：素材 16:9（1672×941）等比放大 1920×1080 无失真；非标比例用 scale+pad 填深色底。

## 交付与验收
- `ffprobe -v error -show_entries format=duration,size -of csv=p=0 out.mp4`
- 抽帧：`ffmpeg -y -ss 8 -i out.mp4 -frames:v 1 prev.png` → `MEDIA:` 发用户验收
- 当前模型无视觉：图片内容/顺序无法自检 → 用文件名约定（01.png=段1）+ 明确请用户核对顺序与排版
