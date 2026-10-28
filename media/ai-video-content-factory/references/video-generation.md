# 视频生成层：脚本口播 → 配音 → 画面 → MP4

> 完整链路：口播稿分段 → edge-tts 配音 → 画面（AI 配图/信息卡 + 要点叠加）→ ffmpeg 合成/拼接。
> 全自动、零人工、零 API 成本。所有脚本在 `~/ai-video-content/`。

## 0. 环境准备（一次）

```bash
sudo apt-get install -y fonts-wqy-zenhei        # 中文字体（ffmpeg drawtext 渲染中文必需）
~/.hermes/bin/uv venv ~/video-venv
~/.hermes/bin/uv pip install --python ~/video-venv/bin/python -i http://mirrors.tencentyun.com/pypi/simple edge-tts pillow
```
- 字体路径：`/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`（PIL 与 ffmpeg drawtext 均支持 .ttc）
- Pillow 装到 `~/video-venv`（系统 PEP 668 禁 pip）；腾讯镜像可能慢 → 用 background=true 装

## 1. TTS 配音（edge-tts）

```python
import asyncio, edge_tts
asyncio.run(edge_tts.Communicate(text, "zh-CN-YunxiNeural").save(str(out_mp3)))
```
- voice：`zh-CN-YunxiNeural`（云希男声）/ `zh-CN-XiaoxiaoNeural`（晓晓女声）
- **坑：连续请求被限流** → 报 `NoAudioReceived`。必须：每段重试 3~4 次（指数退避间隔）+ 段间 sleep 2s。单段失败不代表工具坏了。
- 中文引号""可直接传入；避免文本里有异常字符。

## 2. 免费 AI 配图（pollinations.ai —— 首选，零 key）

```
https://image.pollinations.ai/prompt/<urlencoded英文prompt>?width=1024&height=576&nologo=true&seed=N
```
- **零 key、免费、无严格限流**；返回固定 **1024x576（16:9）** JPEG。
- **坑：urllib 必须带浏览器 UA**，否则 `HTTP 403`（`Python-urllib` UA 被拒）。curl 默认 UA 可过，python 需显式：
  ```python
  urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 ... Chrome/120"})
  ```
- 提示词用英文；插图风格统一描述（深蓝紫渐变+霓虹光效+扁平半写实）保证整套画面一致。
- 分辨率低（放大到 1080p 略糊）：对插画/视频运动画面可接受；配合叠加文字要点观感 OK。
- 备选：硅基流动 `Kwai-Kolors/Kolors`（免费档**不稳定**：返回 `temporary/None/` 无效 URL + 429 限流）——不推荐主用，除非 pollinations 不可达。

## 3. 画面合成（两档）

### A. 信息内容卡（PIL，无配图时兜底）
- `make_cards.py`：content.json（card/sub/bullets/footer）→ 深色渐变背景 + 主标题 + 圆点要点 + 底部信息条 → 1920x1080 PNG。
- PIL 加载 wqy-zenhei.ttc：`ImageFont.truetype(FONT, size, index=0)`。

### B. 配图 + 要点叠加（推荐，图文并茂）
- `overlay_points.py`：AI 配图 1024x576 LANCZOS 放大到 1920x1080 → 顶部半透明遮罩+主标题 → 底部半透明遮罩+要点（蓝色圆点）。
- 遮罩：`Image.new("RGBA",(W,h),(8,10,22,alpha))` 后 `paste`；文字需自动换行 `wrap()`（按 `font.getlength` 截断）。

## 4. 合成 MP4（ffmpeg）

```bash
# 每段：画面帧 + 该段配音 → 片段（-shortest 对齐时长）
ffmpeg -y -i frame01.png -i seg01.mp3 -vf "scale=1920:1080,drawtext=... ,fade=t=in:st=0:d=0.4,fade=t=out:st=<D-0.4>:d=0.4" -map 0:v -map 1:a -t <D> -c:v libx264 -preset fast -c:a aac -pix_fmt yuv420p clip01.mp4
# 拼接
ffmpeg -y -f concat -safe 0 -i list.txt -c copy out.mp4
```
- `img_video.py` 封装上述流程：`--imgdir` 画面目录 / `--notitle`（画面自带标题时不叠加 drawtext，避免标题重叠）/ `--out`。
- drawtext 中文：`fontfile=/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`；特殊字符转义 `:` → `\:`。
- 输出 1080p 视频验证：`ffprobe -show_entries format=duration,size`。

## 5. 用户验收要点（重要）
- 视频必须**图文并茂且有内容展示**：每段画面要有「要点/命令/步骤」文字，不能只放插画或纯标题卡（用户明确纠正过"视频全程没有内容展示"）。
- 交付时附 1 帧预览图（抽帧）让用户直接看画面效果——当前模型无视觉能力时，让用户亲眼确认优于空谈。
- 分段顺序按用户发图的顺序假设，交付时列出"段↔图"对照表供核对；错了重排重渲染成本低。
