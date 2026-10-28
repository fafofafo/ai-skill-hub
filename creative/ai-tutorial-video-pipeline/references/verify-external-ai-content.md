# 外部 AI 工具/技术内容：验证真伪 + 讨论（本会话新增，2026-08-25）

> 背景：用户反复粘贴第三方"AI 工具安利文/技术宣传文"（Gemini 3 Pro、ThetaWave、MoneyPrinterTurbo、FreeToken、BibiGPT），并要求**验证真伪 + 讨论**，不做视频。这条验证流程在本会话跑了 5 次，稳定有效。

## 铁律（用户明确，2026-08-25）
- 用户贴外部内容 → 先**验证真伪 + 讨论**，**绝不主动做视频**（原话："先不做视频，后续也不要马上就做视频"）。
- 只有用户明确说"做视频 / 切换成X做视频"才产出。
- 验证结论必须**逐条对照**：哪些属实 / 哪些是营销加料，不能笼统"是真的"。

## 验证工具箱（按需组合）
1. **GitHub API 查仓库真实性/星标/描述**（快，无需 key）：
   ```
   curl -sL https://api.github.com/repos/<owner>/<repo>
   # 看 stargazers_count / description / license / updated_at
   ```
   星标数对比宣传稿——MoneyPrinterTurbo 宣传"18.6k"实际 **116k**（差 6 倍）→ 一眼穿帮。
2. **Tavily 搜索**（key 在 `~/.hermes/agent-memory-data/backup.env`）：查工具名/官网/知乎实测/开源仓库。
3. **arXiv 查论文**（技术宣传文常对应真实论文）：`web_extract https://arxiv.org/abs/<id>` 读摘要 → 逐条对照数字。
4. **直接抓官网/域名**：`curl -sI` 看响应；可疑域名（如 `gemini3-pro.com` 冒充官方）静态页 + "免费领取"引流钩子 = 山寨。官方域名必是 `.google.com / github.com / 厂商官网`。

## 数字合理性检查（最重要的辨别力）
物理/常识上限，超过即假：
- **LLM 生成速度**：现实约 20~100 token/s。40 万字 ≈ 60 万 token → 现实 1.5~8 小时。"50 秒 40 万字"= 假。
- **TTS 语速**：现实约 300~500 字/分钟。百万字配音要 30 小时以上。"1 分 12 秒百万字配音"= 假。
- **"提速万倍"、"成为新标准"、"印钞机"** = 营销口号，非数据。
- 具体可验证的硬指标（如"753B 单机推理""35B 笔记本"）若论文摘要吻合 → 可信；宣传稿独有的数字（"超 Ollama 四倍""RTX4060 39.3 t/s"）标注"官方口径，待复现"。

## 已验证案例（供复用对照）
| 内容 | 结论 | 关键证据 |
|---|---|---|
| "Gemini 3 Pro 提示词工具" | ❌ 山寨引流 | 真 Gemini 3 Pro 是模型；`gemini3-pro.com` 静态冒充页 |
| ThetaWave | ✅ 真实 | 官网 thetawave.ai + Google Play；"命中率极高"是话术 |
| MoneyPrinterTurbo | ✅ 真实，数字夸大 | GitHub 116k 星（宣传写 18.6k）；"50s/40万字"等物理不可能 |
| FreeToken | ✅ 真实论文 | arXiv:2608.16157 伯克利/MIT；753B/35B 吻合，Ollama 对比未证实 |
| BibiGPT | ✅ 真实成熟 | bibigpt.co + 开源 GitHub JimmyLv/BibiGPT-v1 |

## 坑
- 营销文常**不点名具体项目**（如 FreeToken 那段通篇没写名字）→ 用术语（"边缘原生"/"统一内存池"）去搜论文/项目定位真身。
- "OLLaMma" 这类拼写错误 = 大概率是 Ollama 的笔误，别被带偏。
- 验证完给出"哪些属实/哪些加料"的对照表，再等用户决定下一步（讨论/做视频/存档），不要自作主张推进。
