# 免费配图 + ffmpeg 图片循环（本会话新增，2026-08-24）

## ffmpeg 单张 PNG 不循环 → 黑屏（重大坑，务必先修）
**症状**：用户反馈"视频中没有图片显示"。合成出的 MP4 画面全黑、只有配音。
**根因**：`ffmpeg -i img.png -i audio -t D ...` 中，单张 PNG 作为视频输入时 ffmpeg 只取 **1 帧**（不循环），视频流在首帧后结束 → 黑屏。所有用 PNG 当画面的版本都中招。
**修复**：图片输入前加 `-loop 1 -framerate 30`：
```bash
ffmpeg -y -loop 1 -framerate 30 -i img.png -i seg.mp3 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x12121e,fade=t=in:st=0:d=0.4,fade=t=out:st=D-0.4:d=0.4" \
  -map 0:v -map 1:a -t D -c:v libx264 -preset fast -c:a aac -pix_fmt yuv420p clip.mp4
```
**自检**（模型无视觉时用像素统计判黑屏）：
```python
from PIL import Image; import statistics
px = list(Image.open('frame.png').convert('L').getdata())
# 标准差 >10 即有画面；全黑时均值=0 且标准差=0
print(statistics.mean(px), statistics.pstdev(px))
```
另：输出文件**异常偏小**（如 1.2MB 恒等）或**前后版本 MD5 相同** = 复用/黑屏的强烈信号。

## 免费 AI 配图：pollinations.ai（零 key、免费、无限量）— 主选
- 端点：`https://image.pollinations.ai/prompt/{URL编码英文提示词}?width=1024&height=576&nologo=true&seed=N`
- **必须带浏览器 UA**，否则 403（urllib 默认 `Python-urllib` 被拒）：
  ```python
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
  ```
- 固定输出 **1024×576（16:9）**，请求大尺寸/`model=flux` 参数不生效（manufacturer=sana）。
- 提示词用**英文**；中文也偶可但英文更稳。`nologo=true` 去水印；`seed` 控制一致性。
- 免费档偶发 403/限流 → 重试（3 次，退避 6s×attempt）。
- 参考实现：`~/ai-video-content/gen_poll_images.py` + `videos/prompts_en.json`（7 张分镜英文提示词模板）。

## 免费 AI 配图：硅基流动 Kolors（备选，有坑）
- 已有 key 在 `~/.hermes/agent-memory-data/.env`（SILICONFLOW_API_KEY）。
- 模型 `Kwai-Kolors/Kolors`（中文提示词好）；`black-forest-labs/FLUX.1-schnell` 对该账号报 `code 30003 Model disabled`（不可用）。
- **坑 1**：返回 URL 偶发 `temporary/None/...`（无效，下载得 90B JSON 报 20115）——必须校验 URL 不含 `None` 且下载产物是 JPEG/PNG 头，否则重试。
- **坑 2**：免费档 429 限流严重（连续几张就 429）。
- 结论：仅当 pollinations 不可用时才退回此路。

## 最终画面 = 配图 + 内容叠加（图文并茂）
- `overlay_points.py`：AI 配图(1024×576) 放大 1920×1080 → 顶部半透明遮罩+主标题+副标题 → 底部半透明遮罩+要点（发光圆点）→ 输出 frames/frameNN.png。
- 用户偏好（两次纠正）：**画面必须有内容**——纯插画不行、纯文字卡也不行；配图打底 + 要点文字 = 通过。

## 小云雀真实 AI 视频生成（可选升级）
- 技能 `xyq-skill`（~/.hermes/skills/creative/xyq-skill）：`submit_run.py --message "用户原始描述"` → 后端 Agent 自动拆分镜/选模型/生成。
- key：`~/.hermes/xyq.env`（600）。用户侧只**原样传话**，不做创作加工。生成消耗 credits，须用户确认。
- 短剧走 `xyq-short-drama-skill`。
