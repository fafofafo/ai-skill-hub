---
name: free-media-gen
description: Use when 需要生成图片/封面/缩略图等素材。用 Pollinations 免费生成，无需 key。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [media, image, cover, 封面, 素材, pollinations, 免费]
    related_skills: [content-intelligence, ai-video-content-factory]
---

## When to Use
- 用户要视频封面、缩略图、配图、示意图等图片素材。
- 低成本生成，不调付费图片 API。

## Pollinations.AI（已验证可用，无需 key）
- API：GET `https://image.pollinations.ai/prompt/{URL编码的prompt}?width=1280&height=720&nologo=true`
- 参数：`width`/`height` 尺寸，`nologo=true` 去水印，`seed` 固定结果。
- 生成的是 JPEG；模型为 sana；本机（腾讯云）可达性已验证。
- 封面建议 1280x720（B站/视频号 16:9）。

## Agnes 免费图片 API（2026-10-28 实测，优先用这个）
- **agnes-image-2.5-flash**：文生图/图生图/多图合成全免费（官方 2026-06-01 起无限期），分辨率 1K/2K/3K/4K 全免费；2.1-flash/2.0-flash 兼容备用
- 接口：`POST https://apihub.agnes-ai.com/v1/images/generations`（OpenAI 兼容），`Authorization: Bearer $AGNES_API_KEY`
- 参数：`model=agnes-image-2.5-flash`、`prompt`、`size="1K"`（注意是 1K/2K 不是 1024x1024）、`ratio="1:1"`（支持 16:9/9:16 等）、`n`、可传 `images` 数组做图生图/多图合成
- 限速：1K≈20-30 RPM、2K≈10-20、3K/4K≈1-2 RPM，高峰排队等一会
- 实测：1K 约 2-4 分钟出图（比 RunningHub 慢），复古海报风格还原度高、无瑕疵，可作海报/封面素材
- **必须用 terminal 跑**（execute_code 子进程读不到 AGNES_API_KEY，会 401）；返回 URL 是 COS 临时链接要尽快下载
- GitHub 现成封装/文档：`lj1270998580-crypto/Agnes-help-skill`（312★，全模态 API 帮助中心）

## 用法（Pollinations）
1. 写英文 prompt：风格 + 主体 + 构图 + 留文字空间（如 "clean minimal tech video cover, person using AI agent interface, blue purple gradient, flat design, text space on left"）。
2. 用 terminal `curl -sL "URL" -o 输出.png` 下载。
3. 存到 `~/ai-video-content/assets/`，命名 `cover_<主题>.png`。

## Duck.ai 图像生成（2026-10-28 实测：服务器不可用）
- duck.ai 的 New Image 功能免费、无需账号、支持文生图+图生图（模型 gpt-6-luna），但数据中心 IP 被限流：页面能开、生成请求返回 ERR_BN_LIMIT，curl 直连 418 ERR_CHALLENGE（反机器人）。仅住宅 IP 浏览器可用，别在服务器上浪费时间试它。

## 其他免费素材（备用，未深度验证）
- Transcript LOL（transcript.lol）：音频/视频转文字，每天 2 次免费。
- Audio Enhancer：网页音频降噪工具。
- 找更多免费服务查本地 `~/dev/free-for-dev/速查-创作与部署.md`。
