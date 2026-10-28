---
name: free-video-generation
description: "Use when 要文生/图生视频。Agnes 免费 API 首选，含 RunningHub 付费比价。"
version: 1.0.0
metadata:
  hermes:
    tags: [video, 视频生成, agnes, 免费, 图生视频, api]
---

# 免费 AI 视频生成（文生/图生）

## 选型（按顺序，用户重成本）
1. **Agnes Video 2.5 Flash — 完全免费（$0/秒，限时促销）** ⭐ 首选，已验证
2. RunningHub 开源模板（MiniMax H3）≈0.05-0.13 元/条（耗 RH 币，每日登录送 100 币≈免费 2 条）
3. RunningHub 商业（可灵/Vidu/Kling）贵一个量级，不做首选

## Agnes Video 2.5 Flash（免费，实测 2026-09-19）

### 关键参数
- Base URL: `https://apihub.agnes-ai.com/v1`，key 用环境变量 `AGNES_API_KEY`（已在 config.yaml `model.aliases.agnes-video`）
- ⚠️ **key 在 Hermes terminal/bash 环境里，execute_code 子进程读不到**（`os.environ.get` 返回空）——用 terminal 跑或脚本里先 `echo -n "$AGNES_API_KEY"` 导出
- 模型 `agnes-video-2.5-flash`（还有 agnes-video-2.5 / agnes-video-v2.0）
- **OpenAI 兼容，异步任务**：`POST /v1/videos` 创建 → 轮询 `GET /agnesapi?video_id=<ID>&model_name=agnes-video-2.5-flash`

### 创建任务 body
```json
{"model":"agnes-video-2.5-flash","prompt":"...","seconds":"5","mode":"text","size":"720P","aspect_ratio":"9:16"}
```
- `seconds`: 字符串 "4"-"12"，默认 "5"
- `size`: 只支持 `"720P"`（其他值 400）
- `aspect_ratio`: 21:9/16:9/4:3/1:1/3:4/9:16（输出像素见官方文档）
- `mode`: `text`（文生）/ `keyframe`（首尾帧）/ `reference`（图生）
- **图生视频**：`mode:"reference"` + `images:[公开URL]`（≤5 张，prompt 里用 `<Picture 1>` 引用）；图片必须公开可访问
- keyframe：`first_frame`/`last_frame` 至少一个
- 响应拿 `video_id`，轮询 1-2s，`status` 到 `completed` 后取 `url` 下载
- 出片约 2 分钟；720P，自带音频

### 图片公开 URL 方案（图生视频必需）
- 本机图片不能直接传：先上传到公开图床。实测 0x0.st 已关（AI 垃圾流量），litterbox/catbox 不稳；七牛云公网被 BunkerWeb WAF 挡
- ✅ 已验证：**RunningHub 上传接口拿 COS 临时 URL**——`POST https://www.runninghub.cn/openapi/v2/media/upload/binary`（multipart file，`Authorization: Bearer <RH_API_KEY>`）→ `data.download_url` 直接可用作 Agnes images

## RunningHub 付费替代（开源模型）
见 runninghub-marketplace-search 技能（已含视频 webapp 实测结论：MiniMax H3 首选，SkyReels 避坑，TASK_QUEUE_MAXED 重试）。

## 成品处理
- 下载后 ffprobe 验证时长/分辨率再交付
- 用户做广告视频时：Agnes 出动态画面 → ffmpeg 叠字幕/配音（配乐见 ai-voice-cloning 技能）
- 清理 /tmp 中间文件，成品发 MEDIA: 路径
