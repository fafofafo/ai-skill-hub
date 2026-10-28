---
name: agnes-free-video-gen
description: "Use when 要免费 AI 生成视频（文生/图生）。Agnes Video 免费 API 已验证。"
version: 1.0.0
metadata:
  hermes:
    tags: [video, 视频生成, agnes, 免费, api]
---

# Agnes 免费 AI 视频生成（Video 2.5 Flash）

## When to Use
- 用户要 AI 生成视频（文生视频 / 图生视频），要免费、不耗 RH 币
- 与 RunningHub 视频（耗 RH 币，runninghub-marketplace-search）相比：**Agnes 当前 $0/秒（限时促销）**，首选

## 前提
- `AGNES_API_KEY` 在 terminal 环境变量（config `model.aliases.agnes-video.api_key` = `${AGNES_API_KEY}`）
- **坑：execute_code 的 python 子进程读不到 AGNES_API_KEY**（env 隔离），返回 401 Invalid token。必须用 terminal 工具跑，或在脚本里 os.environ 读（terminal 起的进程才有）
- base: `https://apihub.agnes-ai.com/v1`

## 2026-10-16 复核（视频推"Agnes桌面智能体"）
- 免费政策延续：agnes-video-2.5-flash 仍 $0/秒（限时免费）；agnes-video-v2.0 也免费；官方 FAQ 称核心模型无限期免费
- 免费限制=RPM（每分钟请求数限速），非每日硬配额——"卡顿/限量"=触发 RPM 就等一会
- 视频说"每天登录"是桌面端场景：Agnes Code Desktop（Mac/Windows）登录 Agnes 账号同步订阅；**我们无头 Linux 用 API 通道即可，不需要桌面端**
- Agnes2.5 Pro（付费 token plan / 2.5 Pro-Beta 文本模型）真实存在，但"为支持公司而付费"是话术，按需
- 社区封装 CLI（1038lab/Agnes-AI agnes.py）不需要装，我们脚本已覆盖

## 接口（OpenAI Videos 兼容）
- **创建任务**：`POST /v1/videos`
  ```json
  {"model":"agnes-video-2.5-flash","prompt":"...","seconds":"5","mode":"text|reference|keyframe","size":"720P","aspect_ratio":"9:16","images":["公开图片URL"]}
  ```
  - mode=text：纯文生视频（无 media 字段）
  - mode=reference：图生视频，`images` 传 1-5 个公开 URL；prompt 里用 `<Picture 1>` 引用
  - mode=keyframe：`first_frame`/`last_frame` 公开 URL
  - seconds 是**字符串** "4"-"12"；size 固定 "720P"（其他 400）；aspect_ratio 支持 9:16/16:9/1:1 等
- **轮询**：`GET /agnesapi?video_id=<id>&model_name=agnes-video-2.5-flash` → status 到 completed/failed；非 text 模式必须带 model_name
- 出片 ~2 分钟；下载 url 字段（platform-outputs.agnes-ai.space）

## 图片公开 URL（图生视频必需）
- 图片必须公网可访问、任务期间有效。本机图片：**用 RunningHub 上传接口拿 COS 临时公开 URL**（`POST /openapi/v2/media/upload/binary`，Authorization: Bearer，返回 data.download_url，~24h 有效）再传给 Agnes
- 腾讯云本机直出 URL 到外网不通（ufw 只放行 22/80/443/3000 且 80 被 BunkerWeb 挡）→ 别在七牛云起 http.server 当图床

## 流程
1. terminal 跑脚本（能读到 AGNES_API_KEY）
2. 图生视频：先传图拿公开 URL → POST /v1/videos（reference 模式）→ 轮询到 completed → 下载 mp4
3. 文生视频更快验证通道通不通（无图也能测）
4. 验证产物：ffprobe 时长/分辨率 + 抽帧视觉核验画面与提示词匹配

## 坑
- 字段名必须精确：`image_url`/`duration` 不是合法字段（400 invalid_request）；用 `images` 数组 + `seconds` 字符串
- 轮询太快会 429 Too Many Requests → 间隔 3s + 失败重试
- flash 模型 images 上限 5；videos 字段不支持
- 结果 URL 是 COS 临时链接，completed 后尽快下载
