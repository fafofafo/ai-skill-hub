---
name: system-one-decision-models
description: Use when 部署/调用本地决策模型（Laya/NanoJev/Jev 族，只输出概率不生成文字）。
version: 1.0.0
metadata:
  hermes:
    tags: [system-one, decision-model, laya, jev, nanojev, 决策模型, 本地推理]
---

# System One 决策模型（本地部署与调用）

## When to Use
- 需要低成本/低延迟结构化决策：合规判断 / 工单路由 / 内容分类 / 审核 / 意图分类
- 部署或调用 Laya-multilingual / NanoJev / 官方 Jev（TypeSafe）族模型
- 想把高频小决策从大模型（花钱/慢）下沉到本地决策引擎

## 选型结论（2026-09 实测）
- **Laya-multilingual = 主引擎**（Convai Innovations，Apache-2.0 开源，mmBERT-base 322M）：中文最强、单次 0.3-2.2s、概率校准好、本地免费
- **官方 Jev**（TypeSafe AI）：闭源云 API，注册送 $5（≈1.2 亿 token），质量未独立实测；**"开放注册"≠"开源权重"**（权重/架构/论文均未发布，仅 SDK 开源）
- **NanoJev**（个人复刻，Qwen3-0.6B 底座）：中文弱于 Laya 且重（torch 栈、~32s/次）；唯一价值=官方端到端训练管线可单卡微调定制——已清理，留作微调储备路径
- Laya 英文版 ONNX（receptron/laya-onnx）：最轻（onnxruntime 无 torch、加载 5-7s）但中文不可用；纯英文场景可备
- 决策模型共性：输入 state+结构化问题，输出概率分布，**零 token 生成**、不写文字、不做对话

## 服务化（主模型高频调用，理想分工）
- 常驻 HTTP 服务：`~/models/laya-multilingual/scripts/laya_server.py`（POST /decide + GET /health，127.0.0.1:8123）——模型加载一次、秒回判断
- 守护：`~/bin/laya_server_guard.sh`（健康失败自动拉起，等加载最多 240s）
- 调用：`curl -s -X POST http://127.0.0.1:8123/decide -H 'Content-Type: application/json' -d '{"state":"...肯定式描述...","questions":{"q":{"type":"choice","instructions":"...","criteria":{"a":"..."}}}}'`
- 分工：主模型负责理解/规划/生成，Laya 负责高频小决策——决策下沉省 token；遇到判断需求先走 /decide，别用大模型硬判

## 使用规则（血泪，必守）
1. **state 必须肯定式描述**：否定句（"没有/不是/未"）触发 noul 盲区——同一事实"页面没有封禁提示"判封禁 99.8%❌，"状态正常"判未封禁 99%✅。描述一律改肯定式，别写否定
2. **组合判断，别只信单个 noul**：措辞前缀可翻转 noul（同一违规内容加"小红书笔记内容："前缀 noul 0.90→0.21），但 choice 仍兜底；用 choice+概率分布+常识三路对照；阈值建议 noul<0.3=否 / >0.7=是
3. **choice 比 noul 稳**：分类/路由用 choice；高风险决策 noul+choice 双确认
4. **score/分级类弱**：0-3 分级（impact/severity）实测中英都错，别用于精确打分
5. **时态/状态盲区**："请帮我处理退款"会判"已退款"（把请求当完成）——判断完成态时在 state 里显式给状态词

## 能力边界（实测）
- 不做文本生成、不做数值推理——**不适合行情方向预测**（Laya 直测 buy 偏置 97%、胜率≈随机；deepseek+Laya 混合两轮验证也不通过，详见 ai-trading-research）
- 不做对话/解释；把它当"模糊 if 语句"，控制流由主模型代码掌握

## 部署要点（细节见 references/laya-deployment.md）
- 权重：hf-mirror 下载 convaiinnovations/laya-multilingual（model.safetensors 644M + encoder/ + tokenizer/ + rl_agent_config.json）
- 环境：uv venv + torch CPU（`--index-url https://download.pytorch.org/whl/cpu`）+ `laya` 包 + transformers/safetensors
- ⚠️ venv **不能 mv**（torch lib rpath 硬编码绝对路径，移动后 libtorch_cpu.so 加载失败）——路径变了直接重建
- ⚠️ 内存 <4G 需 swap 兜底 + `torch.set_num_threads(2)`，否则加载阶段 OOM（exit 137）；3.6G 内存加载 ~120s 属正常
- ⚠️ 常驻服务占 ~3G 内存，扩容内存（3.6→8G）可让加载快 3 倍并安全并行

## 关联
- 交易信号验证（Laya 直测/混合架构失败教训、预筛窗口坑）→ ai-trading-research「LLM/决策模型信号源验证」
- Jev 开放/开源状态核实：官方闭源仅 SDK 开源；NanoJev/OpenJev 为第三方复刻；生态第三方工具潮（jev-harness token 门 / jev-mcp / jev-browser / jev-guard，均 MIT 封装官方 API）验证"高频小决策下沉"是市场方向——与本地 Laya 服务化（8123 /decide）同路线，若未来拿官方 key 可借鉴其工具形态
