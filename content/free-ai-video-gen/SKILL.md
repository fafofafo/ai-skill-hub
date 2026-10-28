---
name: free-ai-video-gen
description: "Use when 免费生成AI视频（文生视频/图生视频）。Agnes Video 2.5 Flash 当前 $0/秒。"
version: 1.0.0
metadata:
  hermes:
    tags: [video, 视频生成, 免费, agnes, text-to-video, image-to-video]
    related_skills: [ai-voice-cloning, free-media-gen, runninghub-marketplace-search]
---

# 免费 AI 视频生成（Agnes Video 2.5 Flash）

## When to Use
- 用户要免费/低成本的 AI 视频（文生视频、图生视频、关键帧）
- 比 RunningHub 视频模板（耗 RH 币，~0.05-0.13 元/条）更省钱时优先 Agnes
- 广告视频、素材视频、变体视频的生成

## 状态（2026-09-19 实测）
- **Agnes Video 2.5 Flash：当前完全免费（$0/秒，限时促销）**，720P，4-12 秒，带音频
- 对比：RunningHub MiniMax H3 图生视频 ~0.05-0.13 元/条（耗 RH 币）；Agnes 免费 → 优先
- API key：`AGNES_API_KEY` 环境变量（已配置，见下方坑），base_url `https://apihub.agnes-ai.com/v1`

## 流程
1. **创建任务**：POST `/v1/videos`，JSON：
```json
{
  "model": "agnes-video-2.5-flash",
  "prompt": "<视频描述>",
  "seconds": "5",        // 字符串 "4"-"12"，默认 "5"
  "mode": "text",        // text / keyframe / reference
  "size": "720P",         // Flash 固定 720P
  "aspect_ratio": "9:16"  // 16:9 / 9:16 / 1:1 / 3:4 / 4:3 / 21:9
}
```
2. **轮询**：GET `https://apihub.agnes-ai.com/agnesapi?video_id=<id>&model_name=agnes-video-2.5-flash`，每 2-3s，直到 `status=completed`（~2 分钟出片；偶发 429 重试即可）
3. **下载**：completed 响应的 `url` 字段，curl 保存 mp4

## 三种模式
- **text 文生视频**：只需 prompt
- **reference 图生视频**：`mode:"reference"` + `images:["<公开图片URL>"]`（≤5 张）+ prompt 里用 `<Picture 1>` 引用；图片必须公网可访问且任务期间有效
- **keyframe 关键帧**：`mode:"keyframe"` + `first_frame`/`last_frame`（URL）
- 图像参考用参考图的图片描述写法（如"Use the product and art style in <Picture 1> as reference"）

## ⚠️ 坑
- **execute_code 子进程读不到 AGNES_API_KEY**（Hermes 网关注入的 env 只对 terminal 可见）→ 用 terminal 跑脚本，或从 config.yaml 读（`model.aliases.agnes-video.api_key` 存的是 `${AGNES_API_KEY}` 引用，实际值在 env）
- **图片要公开 URL**：本地图先上传到 RunningHub 上传接口（`/openapi/v2/media/upload/binary`，返回 COS download_url，公网可拉）——七牛云公网 80 被 BunkerWeb WAF 挡，别用
- **video_id 轮询**：keyframe/reference 模式必须带 `model_name` 参数；text 模式可省略
- 免费是限时促销，文档页面会更新价格（`$0/秒` → 恢复 $0.025/秒）——用前先查当前价

## 相关
- RunningHub 视频模板比价：见 runninghub-marketplace-search 技能
- 配音/音色克隆：见 ai-voice-cloning 技能
