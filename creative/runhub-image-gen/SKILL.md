---
name: runhub-image-gen
description: Use when 用 RunningHub 生成/编辑图片。文生图、图生图 API 已打通，含调用脚本与参数速查。
version: 1.0.0
metadata:
  hermes:
    tags: [runninghub, 图片生成, 文生图, 图生图, api]
---

# RunningHub 图片生成（API 已打通）

## 默认风格提示词（用户指定 2026-09-07）
文生图/图生图默认风格前缀：
```
Modern pencil illustration, 1950s–60s retro travel poster, silkscreen/serigraph texture, loose hand-drawn strokes + clean outlines, bold saturated high-contrast palette, flat color blocks, misregistration grain, cinematic balance, decorative framing, mid-century optimistic graphic simplification.
```
用法：`t2i "<默认风格> <画面内容>"`；画面内容由用户提供或按场景合理拟。

## When to Use
- 用户要求生成图片/封面/配图，或编辑已有图片（AI 文生图/图生图）。
- 优先用 RunningHub（画质好、用户付费账号），替代免费 Pollinations。

## 工具
`~/tools/runhub/runhub_img.py`（API key 在 backup.env RUNNINGHUB_API_KEY）

```bash
# 文生图（全能图片2.0-文生图-低价渠道版）
python3 ~/tools/runhub/runhub_img.py t2i "提示词" --ratio 9:16 --res 2k --out 输出.png
# 图生图（image2 图生图 V1.0，自动上传输入图）
python3 ~/tools/runhub/runhub_img.py i2i "编辑指令" 输入图.png --out 输出.png
```

## 参数速查
- ratio 可选: empty/3:2/1:1/2:3/5:4/4:5/16:9/9:16/21:9/3:4/4:3/9:21/1:2/2:1/1:3/3:1
- res 可选: 1k/2k/4k（默认 1k；2k 更清晰，耗币略高）

## 3:4 高清出图：Z-image 基础模板（海报首选）
image2.5 sunburst（`--app 2098218128315609089`）输出恒定约 880×1184；要**精确 3:4 + 高清**改用 Z-image 文生图模板：

| 项 | 值 |
|---|---|
| webappId | `2055930575931887617` |
| 提示词节点 | `21.text`（中文长提示词直接填）|
| 尺寸节点 | `7.width` / `7.height` / `7.batch_size` |
| 3:4 参数 | width=1086, height=1448 → 实出 **2160×2896** PNG（6-8MB）|
| 成本/耗时 | 8-9 币，40-45s |

```python
nodes = [
 {"nodeId":"7","fieldName":"width","fieldValue":"1086"},
 {"nodeId":"7","fieldName":"height","fieldValue":"1448"},
 {"nodeId":"7","fieldName":"batch_size","fieldValue":"1"},
 {"nodeId":"21","fieldName":"text","fieldValue": prompt},
]
post("/task/openapi/ai-app/run", {"webappId":"2055930575931887617","apiKey":key,"nodeInfoList":nodes})
```

- 提示词正文仍要写「3:4 竖版构图，尺寸 1086×1448」——只给节点宽高、正文不提比例，构图会走形。
- 该模板**不暴露 LoRA 节点**（只有 unet/clip/vae/text/尺寸/采样），换 checkpoint 无效：LoRA 固化在工作流内部，要挂自定义 LoRA 只能登录网页端。
- 中文提示词唯一稳定路径：先 `write_file` 落 /tmp，再 `open().read()` 传 `21.text`；拼进 shell 命令会被引号和括号打断。

## 关键接口（备忘）
- 提交: `POST /task/openapi/ai-app/run` body {webappId, apiKey, nodeInfoList[{nodeId, fieldName, fieldValue}]}
- 轮询: `POST /openapi/v2/query` body {taskId} → status=SUCCESS 后 results[0].url
- 上传: `POST /openapi/v2/media/upload/binary`（multipart file）→ 返回 fileName 供 image 节点用
- 获取应用参数: `GET /api/webapp/apiCallDemo?webappId=&apiKey=`（返回 curl 示例+nodeInfoList）
- 应用ID: 文生图 2064020837354790914（node 3=prompt, 7=aspectRatio/resolution）；图生图 2047883048150110209（node 1=text, 3=image）

## 注意
- 消耗 RH 币（文生图 1k 约 1 币 + 第三方 0.1 元；费用按实际用量结算）
- 标准模型 API（seedream 等 /openapi/v2/*）需企业级-共享 Key，消费级 Key 只能调 AI 应用/工作流 API
- 任务平均 45-140 秒，轮询间隔 5s

## 内容安全审查拦截（errorCode 1501）
- **泳装/暴露女性造型触发 image2.5 的内容安全审查**（`Content security audit did not pass` / `内容安全审查未通过`，errorCode 1501），提示词多措辞重试（含改为「端庄克制、非暴露」表述）均被拦截——**这是平台审核红线，不是提示词问题，不要反复重试或尝试绕过**。
- 应对：改为非泳装表述（如「夏日度假时装」「露肩连体裙装+薄纱罩衫」）能通过审核但结果可能不像泳装；或如实告知用户被平台拦截、建议换造型。透明告知比绕过审核更符合交付原则。

## 限流与偶发失败（2026-10-15 实测）
- **`TASK_QUEUE_MAXED`（提交返回 code 421）**：RunningHub 服务端任务队列满，非脚本故障，与提示词/节点参数无关。间隔 <60s 的重试基本无效（实测 6 次 × 25s 全灭），队列可持续堵塞数分钟——用 `terminal(background=True, notify=True)` 跑 **60s × 12 次** 退避，成功即下载；不要在前台同步循环里阻塞对话，也不要因为报错就改提示词。
- **提交偶发失败**（`'NoneType' object is not subscriptable`）：提交/轮询的临时解析失败，立即重试通常成功。
- **任务超时**（`TimeoutError 300s`）：长 prompt 或高峰时生成超过 300s 超时窗，重跑同一条命令即可。
- **余额不足（errorCode 605「您的账户余额不足，请充值」）**：**先 curl 探测一次确认，605 可能是瞬时/充值延迟同步**（2026-10-26 实测：第一次 curl 返回 605、第二次即 success，用户网页端显示有余额）——探测恢复则继续出图；连续 2-3 次仍 605 才停止重试循环，告知用户去 RunningHub 控制台充值（https://www.runninghub.cn），充值后再继续；充完可能已有部分图成功，只补缺失图即可。
- 三类失败重试模式统一：脚本里 `if 输出文件存在且 >100KB: 成功`，否则 sleep 后重试，避免被单次限流卡死整批。
