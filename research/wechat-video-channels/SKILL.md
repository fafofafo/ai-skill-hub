---
name: wechat-video-channels
description: Use when 用户要学习/获取某微信视频号博主的全部视频内容。含可行通道矩阵与付费 API 选择。
version: 1.0.0
---

# 微信视频号内容获取（WeChat Channels）

用户（内容创作者，跟踪 AI 生态）要"学习某个视频号博主的所有内容"时用。产物通常是**文字稿/要点**（发给 learn 学习），不一定是视频文件本身。

## 核心事实（先对齐，别浪费 token 试错）
- 视频号**无官方开放 API**，不能像 B 站/YouTube 一条命令拉全量。公网/搜狗搜不到账号内容（搜狗微信搜 type=1 只有公众号，视频号账号名搜不到）。
- 因此"学博主全部内容"只有两条实质通道：公众号同步版（免费）或第三方付费 API（全量数据）。

## 流程（顺序执行）
1. **先查有无公众号**：`curl -sL "https://weixin.sogou.com/weixin?type=1&query=<账号名>&ie=utf8"` 搜公众号。有同名公众号 → 走 wechat-articles 技能免费全量抓图文（多数博主视频与公众号同源，文字稿覆盖 80%+），零成本立即跑，不用碰 API。
2. 无公众号 → 走第三方付费 API（见下）。
3. 拉取链路：搜账号 → 拿 finder username（`v2_...@finder`）→ 拉全部作品列表（标题/简介/互动/时间）→ 下载视频 → ASR 转文字稿 → 整理成"博主内容包"。
4. **对接 learn**（五入口学习库）：资料写入 `~/知识库目录/drafts/` 或注入 learn 的 Bot Chat；learn SOUL=摄入→草稿→验证→judge 四档（PROMOTE 写 main/）。无需改造，learn 会自动走审定流程。

## 付费 API 服务商（2026-09 调研确认，接口存在、服务可达；完整拉取流程待 key 实测）
| 服务商 | 特点 | 接口 |
|---|---|---|
| **JustOneAPI** (justoneapi.com) | 接口最全，一条龙 | 账号搜索 V1-V3 / 账号视频 V1 / 视频基本信息·标题·下载链接 / 指标 / 评论 |
| **TikHub** (tikhub.io) | 国内团队、支付宝/微信充值、国内访问稳定、0.01$/次 | 账号搜索 / fetch_user_videos（用户作品列表，翻页 last_buffer）/ 视频详情·评论 |
- 国内用户注册：**优先 TikHub**（实测官网/docs/api 全通且快）。JustOneAPI 服务器侧可达但用户本地报"网络连接异常"——境外站国内访问不稳，非服务故障。
- 成本：拉一个博主全量（100-500 条）约几元到几十元；ASR 走免费额度。
- 大整数 ID（id/object_nonce_id 等 64 位）必须**按字符串**接收/传参，别过 JS Number（精度丢失）。

## 坑
- **下载 URL = media.url + media.url_token**（url_token 以 `&token=` 开头；full_url 已是拼接结果）。漏 token 的表现是 **HTTP 400 Bad Request（不是 403）**——先检查 URL 是否拼全，别在 UA/Referer/https 上浪费时间。
- **链接+decode_key 会过期**：隔天/几天后失效（400/无效），重新 fetch_video_detail 拿新值；url_token+decode_key 必须来自同一次响应（微信每次请求换新 key）。
- **视频加密**：下载的 MP4 无法播放 = 加密文件，需同次 API 响应返回的 `decode_key` 解密；微信每次请求都换新 key，**decode_key 必须与下载文件来自同一次响应**，否则解密失败。
- **响应慢**：微信服务器原因，接口超时要设 30s+，timeout 过小会已扣费但收不到响应。
- 需要 API key 才能实测；拿到 key 先小规模验证（搜账号→拉 5 条）再全量，别上来就烧钱拉全量。
