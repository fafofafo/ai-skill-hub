---
name: runninghub-marketplace-search
description: Use when 在 RunningHub 找某模型/接口并比价。含市场搜索、模板→webapp、实测成本、视频模板。
version: 1.0.0
metadata:
  hermes:
    tags: [runninghub, 市场搜索, 比价, api]
---

# RunningHub 市场搜索与比价

## When to Use
- 用户问「RunningHub 上找 X 模型最便宜的接口/应用」
- 需要确认某模型在 RunningHub 是否可用、以什么形态提供、实际每张/每次成本
- 生成图片本身用 runhub-image-gen 技能（用户自建）；本技能管「找接口/比价」

## 模型形态判断（按序探测）
1. **标准接口市场（SKU）**：`POST /api/sku/list` body `{"search":"关键词","pageNo":1,"pageSize":20}`（最小 body 即可）。搜 gpt/openai/image2.5 均 0 → 该模型还没进标准接口市场。
2. **工作流模板**：`POST /api/search/workflow` body `{"search":"关键词","pageNo":1,"pageSize":10}`。**字段必须是 `search`，`keyword` 静默无效**（返回最新列表，total=全量）。
3. **模板→可调用 webapp**：`POST /api/portal/workflow/detail` body `{"workflowId": 模板id}` → 响应 `data.webappId`（null=未发布为 webapp，需自带第三方 key 或 clone 运行）。
4. **webapp 调用格式**：`GET /api/webapp/apiCallDemo?webappId=&apiKey=` → `data.curl` 含 nodeInfoList 字段结构。**必须用 GET**——POST 同参数返回 `301 PARAMS_INVALID`。curl 是双重转义字符串，解析节点字段前先 `.replace('\\\\n','\n').replace('\\\\"','"')` 再用正则 `"nodeId":\s*"(\d+)",\s*"fieldName":\s*"([^"]+)"`。
5. **LoRA / 单模型页**：用户可能直接给 `https://www.runninghub.cn/model/public/<modelId>` 的模型页——既不是工作流也不是 SKU。此时按模型名搜 workflow/SKU 全 0 属正常（LoRA 不会作为模板标题出现），**不要据此回答「不存在」**；先用浏览器读模型页拿「模型类型 / 基础模型 / 文件路径」，再走下面的 LoRA 排查。

## LoRA 模型页（/model/public/<id>）：查找与测试
模型页浏览器可直接读：模型名、类型（LoRA）、基础模型（如 moss-image）、文件路径（`models/loras/xxx.safetensors`）、MD5、作者/搬运来源、标签。

**核心结论：用现成 webapp 测指定 LoRA，基本做不到。**
- 模型详情 API 需登录态：`/api/model/detail?modelId=` → `412 TOKEN_INVALID`（API key ≠ 登录 token）；`/api/model/public/detail` → `404`。
- 未登录模型页只有「返回/申诉/点赞/收藏」，无试跑/下载入口。
- 文生图模板的 apiCallDemo 只暴露 `unet_name / clip_name / vae_name / text / aspect_ratio / steps / seed / cfg` 等字段，**没有 `lora_name`——LoRA 写死在模板内部，用户不可替换**。判断方法：解析 demo 全部 `nodeId.fieldName`，grep `lora`，全无即不可换。

**排查顺序（四步给出确定答复）**：①模型页读类型与基础模型 → ②搜模型名/风格词，0 命中说明无现成模板 → ③搜基础模型名拿 webappId，逐个查 demo 是否含 lora 字段 → ④都不行则明确告知需登录网页端挂载，并给三条替代路径（用户扫码登录让你接管 / 用户网页试跑发图给你做量化分析 / 基础模型+同风格提示词近似测试并声明不是真 LoRA）。
详细字段清单与探测脚本、近似测试的模板 ID 与节点字段表见 references/lora-and-model-pages.md。

**近似测试已跑通（方案 C，默认走这条）**：模型页正文那段英文风格描述就是提示词蓝本——逐句翻成中文并入提示词，套该基础模型自己的文生图 webapp，通常一次命中风格方向（实测 Z-image-base + lilia 描述、moss-image + feverdream 描述均一次对上：低饱和暖调/柔和侧窗光/干花静物/复古编辑摄影质感/梦核悬浮光尘全到位）。**交付口径必须是「未挂真 LoRA，只验风格方向」，不能说成「该模型已验证」**。已知：Z-image 系模板支持任意 3:4 高清出图（2160×2896，比 image2.5 的 880×1184 好得多）；MOSS 系文字渲染弱，提示词写品牌字也会画成抽象符号。

## 实测成本（决定性方法）
- 价格表接口（/api/area/price/table、/api/workflow/webapp-price-estimate、skuPriceTable）需登录 token（Rh-Accesstoken），API key 不够 → 别浪费时间。
- 正确姿势：跑 1 张测试（1k/1:1 最省），提交 `POST /task/openapi/ai-app/run` body {webappId, apiKey, nodeInfoList}（节点从 apiCallDemo 的 curl 提取，只保留 text/prompt/aspectRatio/resolution），轮询 `POST /openapi/v2/query` 到 SUCCESS。
- **轮询响应是平铺结构**：`usage` 在顶层（`q["usage"]["consumeCoins"]`、`thirdPartyConsumeMoney`、`taskCostTime`），不是 `q["data"]["usage"]`。
- 总成本 ≈ consumeCoins×币价（**¥0.002-0.005/币**，按会员套餐折算；每日登录赠 100 币）+ thirdPartyConsumeMoney。模板自称「单张成本低至X分」多为第三方口径，以实测为准。
- **坑：很多「低价」image2.5 模板走 LLAI 第三方中转（ComfyUI_LLAI_API 节点），需自带第三方 key**；直接用我们 API key 提交会报 `API key not found. Please set apikey on this complete image node.`（实测 2098729446000906242/2098663449214672897 均如此）。先看 demo curl 里的节点类型，含 LLGPTImage25Generator 的慎测。
- **i2i 节点坑：text/image 的 nodeId 因 webapp 而异，提交前必须从 apiCallDemo 核对**。猜错顺序报 `NODE_INFO_MISMATCH(nodeId=.., fieldName=.., reason=field_not_found_in_node_inputs)`（实测：image2.5 i2i 2097970230151704577 = image@4/text@3；image2 系列 2047883048150110209/2048027355322523650 = image@3/text@1；image2 低价渠道 2080590320298979330 = 多参考图@24-27/text@22）。失败先重新拿 apiCallDemo 看节点，别猜。
- **提交失败诊断：报 `'NoneType' object is not subscriptable`（r["data"]["taskId"]）时先打印完整响应**——data=None 且 code!=0 是真失败（多为 NODE_INFO_MISMATCH 节点错或并发限流），不是网络抖动，别盲目重试；成功响应 data 里带 netWssUrl 等字段但 taskId 也在 data.taskId。
- **image2 实测结论（2026-09-16）**：文生图最便宜 2048025785323229185（2币+0.1元≈0.108元/张）；图生图最便宜 2047883048150110209（2币+0.1元，59s）。跨代：文生图 image2.5 Sunburst 更便宜（0.036），图生图 image2 更便宜（0.108 vs 0.22）。
- 单次测试 ≈0.1-0.5 元，比价测 2-3 个候选可接受。
- **批量实测多个候选（2026-09-16）**：并发提交多任务会被限流（响应 data 为 None）；结果 URL 是 COS 临时链接有时效——**串行提交+间隔 3-4s+失败重试，SUCCESS 后立即下载**（轮询完再统一下载会拿 137B 失效页）。
- **results 可能多节点（2026-09-17）**：query 响应 `results` 有时含 [txt(内容=图片URL), png(真图)]，`results[0]` 是文本节点——下载验证图时按 `outputType=image` 或 url 以 .png/.jpg 结尾选，别取 [0]。

## 实测价格表（横向比价决策用，每张文生图）

| 方案 | 应用/webapp | 实测消耗 | 耗时 | 输出尺寸 | 备注 |
|---|---|---|---|---|---|
| **image2.5 sunburst（默认首选）** | 2098218128315609089 | **2 币 ≈¥0.036** | ~30s | 880×1184 | 日常默认，最便宜 |
| image2 i2i 低价渠道 | 2047883048150110209 | 2 币 + ¥0.1 ≈¥0.108 | 59s | — | 图生图用 |
| Qwen-Image InstantX CN Union（aPS龙神） | 2096885511829938178 | **17 币 ≈¥0.034–0.085** | 83s | — | 线稿/深度/姿态控制 |
| Qwen-Image InstantX CN Union（龙神呀） | 2097175742214926337 | 19 币 | 91s | — | 同上，多 2 币 |
| krea2 无LORA | 2093344604832751618 | **10 币** | 49s | 1152×1536 | krea2 里最便宜 |
| Pornmaster krea2 t2i | 2099151417163468801 | 12 币 | 58s | 832×1216 | 写实人像，尺寸最小 |
| Krea2 文生图 | 2096506122457927681 | 14 币 | 68s | 1360×2048 | krea2 里画质最高（锐度 6.25） |
| Krea2 简洁好用 | 2096850838621876226 | 21 币 | 102s | 1360×2048 | 最贵，无优势 |

**报价口径**：全部是 `usage.consumeCoins` 实测值，`thirdPartyConsumeMoney` 均为 null（无第三方费用）；币价按 ¥0.002–0.005/币折算。

### 用户价格红线（standing）
报方案前先算「币数 ÷ image2.5 的 2 币」：**超过 ~5 倍（>10 币）即视为贵，不主动推荐**。用户对 krea2 系列（10–21 币）的结论是「都太贵了，全部放弃」——这类模型只在用户点名要时才给，并先报币价让用户决定。便宜替代路径：image2.5 出图 + 提示词加 `Raw photo / 35mm film grain / realistic skin texture / cinematic grading` + cinema-color-grade 调色（成本仍 0.036 元/张）。

## 查某个 .safetensors 文件在平台上的名字
两条路，按需选：
1. **模型公共页**：`https://www.runninghub.cn/model/public/<modelId>` 用浏览器打开，`document.body.innerText` 直接含「模型类型 / 基础模型 / 文件名称：models/unet/xxx.safetensors / MD5」——最快，模型详情 API 要登录态（`/api/model/detail` 报 TOKEN_INVALID/TOKEN_MISSION）。
2. **工作流依赖**：`POST /api/portal/workflow/detail` 拿 `data.usedModels` 数组，或对整个响应体正则 `[\w\-\.]+\.safetensors` 抓全部依赖（含主模型/VAE/文本编码器/加速 LoRA/预处理模型）。

**用户给的模型名 ≠ 平台文件名**：常见差异是前缀顺序与分隔符（用户写 `Qwen-image-InstantX-Controlnet-Union.safetensors`，平台实际是 `InstantX_Qwen-Image-ControlNet-Union.safetensors`）。答用户时必须给平台实际名，并附用在哪些工作流/ID。

**同名系列的版本差异**：用户指定的模型可能在平台「已冻结」且无可调用工作流（如 PornMaster flux2-klein-9b），此时同一作者的 **krea2 版**往往才是唯一可调用的 webapp——按「同作者/同系列的其他基础模型版本」找替代，并明确告知版本与尺寸差异，不要含糊说「就是这个模型出的」。

## Midjourney 标准模型 API（2026-10-20 实测）
- **存在**：youchuan 系列 text-to-image（v6/v6.1/v7/v8.1/v8.2-preview/fast/turbo/niji6/niji7）+ image-to-video。端点 `/openapi/v2/youchuan/text-to-image-v81` 等。参数对齐 MJ 语义（prompt/chaos/stylize/quality/raw/iw/tile/seed/weird/hd）。
- **费用**：v8.1 稳定版 ≈ $0.09/张；v8.2-turbo ≈ 2x fast；社区工作流模板 0.25 元/次（每日免费 5 次）。对比 image2.5 只要 0.036 元/张。
- **当前账户调不了（实测 40310）**：CN 节点因合规下线 midjourney（`"this model is no longer available on the CN endpoint"`）；即使提交到 runninghub.ai 全球站端点仍 40310——key 绑定 CN 账户主体，需全球站注册的企业级-共享 key（标准模型 API 仅支持企业级共享 key）。
- **参数/端点排错**：缺 `hd` 报 `1007 field 'hd' is required`（端点活着）；v8.2-preview/turbo 直接 POST 报 `1001 Invalid URL`——端点名别猜，按官方 api-XXXX 文档页核对。
- **实用建议**：复刻 MJ 提示词不必上 MJ 接口，提示词通用、直接搬进 image2.5 即可（省 10-20 倍）。

## 坑
- 模板搜索分页 bug：pageNo 不生效，永远返回同样 10 条；换关键词而不是翻页。
- `/api/sku/list` 的 `categoryType:"ALL"` 会返回 0；不带或带具体类目（如 WEBAPP）才行。
- 页面级搜索（/ai-apps 等）是 CMS 落地页不是可搜索市场；Nuxt SPA 用 web_extract 只有壳。
- 从 SPA 逆向接口：抓 `/_nuxt/*.js` chunk，grep `"/api/..."` 路径找真实端点（详见 references/runninghub-api-discovery.md）。
- **视频生成无 SKU**：标准接口市场（/api/sku/list）搜视频/图生视频/可灵/即梦全 0——视频只能走工作流模板→webapp 形态。
- **接口域名固定 `https://www.runninghub.cn`**：`api.runninghub.ai` / `api.runninghub.cn` 直连返回 HTTP 000（连不上，不是风控）；搜工作流、`/api/portal/workflow/detail`、`/api/webapp/apiCallDemo`、`/task/openapi/ai-app/run`、`/openapi/v2/query` 全部走这个域，别按文档惯性换域名试
- **上传文件用 `Authorization: Bearer` 头**（不是 Rh-Accesstoken）；用错头报 `apiKey is required`。
- **TASK_QUEUE_MAXED（code 421）**：任务队列满（前一个超时任务还占着队列，全站共享），不是网络错也不是提示词/节点问题——间隔 <60s 的重试往往全灭（实测 6 次 × 25s 全部 421，队列可持续堵塞数分钟）。做法：`terminal(background=True, notify=True)` 跑 **60s × 12 次**退避循环，成功即下载；不要在前台同步循环里堵对话，也不要因 421 去改提示词。
- **视频实测结论（2026-09-19）**：MiniMax H3 图生视频 2099756447792979969（node4=image+node7=prompt，49币/245s，5s 720p 可用）性价比最好；SkyReels 1892245892601176066 44币但产物异常（4KB/1.9s）避坑；混元 I2V 1897647069900034049 缺 guidance_type 参数报 failed。

## 参考
- references/runninghub-api-discovery.md — 从 SPA JS chunk 逆向 RunningHub 接口的完整方法
