# LoRA 与单模型页（RunningHub）

## 模型页 URL 形态
`https://www.runninghub.cn/model/public/<modelId>`

页面（未登录也可读）给出的关键元数据：

| 项 | 示例 |
|---|---|
| 模型名 | `<风格名> Mood \| <基础模型>` |
| 模型类型 | **LoRA**（也可能 Checkpoint/VAE/ControlNet）|
| 基础模型 | `moss-image` / `flux-dev` / `z-image-turbo` 等 |
| 文件名称 | `models/loras/<file>.safetensors` |
| MD5 | 校验用 |
| 状态 | 可能标「已冻结」 |
| 来源 | 原创作者 + 搬运者 + 搬运地址 |
| **风格描述** | 页面底部一段英文逗号串（如摄影/光影/色调/氛围），**这是近似测试的提示词蓝本** |

拿到模型页后先分清：**LoRA 是挂件，不是可独立出图的模型**——必须配它的基础模型，并且要有一个带 `Load LoRA` 节点的工作流。

## 为什么「搜不到」不是「不存在」
- `POST /api/search/workflow` 搜的是**工作流模板标题/描述**，LoRA 文件名一般不会出现在标题里 → 搜 LoRA 名 0 命中是常态。
- `POST /api/sku/list` 只覆盖标准接口市场，LoRA 不进 SKU。
- 所以判断顺序改为：**先读模型页确认元数据，再判断有无可用模板**。

## 模板是否能换 LoRA：看 apiCallDemo 字段
```python
import json, re, urllib.request
def demo(webapp_id, key):
    req = urllib.request.Request(
        f"https://www.runninghub.cn/api/webapp/apiCallDemo?webappId={webapp_id}&apiKey={key}",
        headers={"Authorization": f"Bearer {key}"})          # GET，POST 会 301 PARAMS_INVALID
    return json.load(urllib.request.urlopen(req, timeout=60))

raw = demo(webapp_id, key)["data"]["curl"]
raw = raw.replace('\\\\n', '\n').replace('\\\\"', '"')      # curl 是双重转义，必须反转义
fields = re.findall(r'"nodeId":\s*"(\d+)",\s*"fieldName":\s*"([^"]+)"', raw)
has_lora = any('lora' in f.lower() for _, f in fields)
```

典型文生图模板暴露的字段（实测 MOSS 系）：
`batch_size, value(提示词), text, unet_name, weight_dtype, clip_name, vae_name, aspect_ratio, megapixels, cfg, denoise, sampler_name, scheduler, seed, steps`

**没有 `lora_name` / `lora_strength` 就是不能换 LoRA**——这类模板把 LoRA 固化在工作流文件里，webapp 只开放提示词与采样参数。

## 需要登录才能做的事（API key 做不到）
| 接口 | 结果 |
|---|---|
| `/api/model/detail?modelId=` | `412 TOKEN_INVALID` |
| `/api/model/public/detail` | `404 NOT_FOUND` |
| `/api/portal/model/detail` | `301 PARAMS_INVALID`（参数形状不对）|
| 价格表类接口 | 同样要登录 token |

未登录模型页只有「返回 / 申诉 / 点赞 / 收藏」，没有试跑或下载按钮。

## 近似测试（方案 C，实测已跑通）

### 步骤
1. 从模型页抄下整段英文风格描述（作者写的风格定义，就是提示词蓝本）。
2. 搜基础模型名拿**有 webappId** 的文生图模板：`/api/search/workflow` → 逐个 `/api/portal/workflow/detail` 取 `data.webappId`（很多模板为 null，不可调用）。
3. 拉该模板 apiCallDemo，找提示词字段（多为 `text` 或 `value`）与尺寸字段。
4. 提交 `POST /task/openapi/ai-app/run` `{webappId, apiKey, nodeInfoList}`，轮询 `POST /openapi/v2/query` 到 SUCCESS，**立即下载** results 里的 COS 链接。
5. 交付时说「未挂真 LoRA，只验风格方向」——只说风格对得上，不说模型已验证。

### 实测可用的基础模型文生图模板
| 基础模型 | webappId | 提示词字段 | 尺寸字段 | 实测输出 | 成本 |
|---|---|---|---|---|---|
| **Z-image-base** | `2055930575931887617` | `21.text` | `7.width` / `7.height` / `7.batch_size` | 1086×1448 → 实际 2160×2896 PNG（6-8MB）| 8-9 币，40-45s |
| **moss-image** | `2113455891075915777` | `45.text`（英文 caption）/ `34.value`（中文需求，会被 node 35 的 prompt-engineer 系统词扩写）| `19.megapixels`、`44.batch_size` | 1024×1024 | 3-9 币，14-42s |

**Z-image 模板是当前最好的 3:4 高清出图路径**：原生接受任意宽高（3:4 出 2160×2896），比 image2.5 sunburst 的 880×1184 清晰得多；中文长提示词直接填 `21.text` 即可。

### 已验证的命中案例
- **lilia**（Z-image-base；romantic vintage editorial photography / painterly cinematic / soft natural light / dark moody shadows / floral still life / muted warm grading）→ Z-image 模板 + 中文直译提示词，一次命中：饱和度 23.6%、R-B +16.5、柔度 0.031、干花静物与侧窗柔光全在。
- **feverdream**（moss-image；dreamcore / fever-dream 氛围）→ MOSS 模板 + 中文直译，梦核氛围到位：悬浮失重、扭曲空间、光尘、冷暖对撞、暗调。

### 近似测试的边界（必须向用户说清）
- **文字渲染弱**：MOSS 系模板即使提示词写了品牌字（如 FAFO）也会画成抽象符号，别指望准确中文标题；需要标题文字就后期贴字或换 image2.5。
- 近似测试只证明「风格方向可复现」，不能证明该 LoRA 的真实笔触与细节偏好。

## 不要做的事
- 不要因为搜索 0 命中就说「模型不存在」——先看用户给的模型页。
- 不要用 SKU/workflow 搜索代替模型页读取；两者覆盖的形态不同。
- 不要在没确认模板含 lora 字段前，就向用户承诺「换这个 LoRA 跑一张」。
- 不要把近似测试说成「该 LoRA 已验证」；也不要在 MOSS 系模板上承诺准确中文标题。
