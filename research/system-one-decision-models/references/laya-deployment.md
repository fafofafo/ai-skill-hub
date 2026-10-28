# Laya-multilingual 部署细节（实测命令）

## 下载权重（hf-mirror，HF 直连常失败）
```bash
mkdir -p ~/models/laya-multilingual/encoder ~/models/laya-multilingual/tokenizer
cd ~/models/laya-multilingual
base=https://hf-mirror.com/convaiinnovations/laya-multilingual/resolve/main
curl -sL -o model.safetensors "$base/model.safetensors"
curl -sL -o rl_agent_config.json "$base/rl_agent_config.json"
curl -sL -o encoder/config.json "$base/encoder/config.json"
curl -sL -o tokenizer/tokenizer.json "$base/tokenizer/tokenizer.json"
curl -sL -o tokenizer/tokenizer_config.json "$base/tokenizer/tokenizer_config.json"
```
（并行 curl & wait 可提速；模型 644M）

## 环境（uv venv，torch CPU 从官方 index）
```bash
uv venv ~/venvs/laya-venv --python 3.11
uv pip install --python ~/venvs/laya-venv/bin/python torch --index-url https://download.pytorch.org/whl/cpu
uv pip install --python ~/venvs/laya-venv/bin/python transformers==5.17.0 safetensors numpy laya
```
- 装完验证：`~/venvs/laya-venv/bin/python -c "import torch, laya; print(torch.__version__, laya.__version__)"`
- ⚠️ venv 路径定了就不能 mv（torch rpath 硬编码），换路径=重建

## 一次性推理（不常驻时）
```python
import sys; sys.path.insert(0, "/home/ubuntu/venvs/laya-venv/lib/python3.11/site-packages")
import torch; torch.set_num_threads(2)   # 内存小时必设，防 OOM
import laya
agent = laya.load("/home/ubuntu/models/laya-multilingual")
r = agent.system_one(state, questions)   # state: str; questions: dict
```

## 常驻服务（推荐，主模型高频调用）
- 服务：`~/models/laya-multilingual/scripts/laya_server.py`（POST /decide + GET /health，127.0.0.1:8123）
- 守护：`~/bin/laya_server_guard.sh`（健康失败自动拉起）
- 启动：`nohup ~/venvs/laya-venv/bin/python ~/models/laya-multilingual/scripts/laya_server.py >> ~/.hermes/logs/laya_server.log 2>&1 &`
- 验证：`curl -s http://127.0.0.1:8123/health` → {"ok":true,"ready":true}

## 问题格式（三种类型）
```json
{"type": "choice", "instructions": "...", "criteria": {"optA": "描述A", "optB": "描述B"}}
{"type": "score", "instructions": "...", "criteria": ["等级0描述", "等级1描述", ...]}
{"type": "noul", "instructions": "..."}   // 返回 0-1 概率，高=是
```

## 实测性能基线（3.6G 内存 + 4 核 CPU + swap）
- 加载 120-143s（内存紧张走 swap；8G 内存应 ~40s）
- 单次判断 0.3-2.2s（服务常驻后稳定 ~0.34s 同题重复）
- 峰值内存 ~3G RAM + 2.8G swap（OOM 时加 /swapfile2 3G 兜底）

## 关键坑汇总
- 加载阶段 OOM（exit 137）= 内存不足 → 加 swap 或扩内存，别改代码
- Tokenizer 256k 词表（mmBERT）加载内存大，属正常
- 官方 laya 包 0.3.4 加载本地目录即可，无需 HF 登录
