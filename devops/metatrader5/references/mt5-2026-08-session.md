# MT5 部署实测命令链（2026-08-29 会话）

> 目标：把 MT5 跑在能访问国际网络的云主机（本例七牛云 Ubuntu 24.04，1.9G 内存），供 AI agent 接入。
> 已达成：MT5 终端在 Docker 内真实运行 + noVNC 界面可用。
> 未达成（会话结束时）：demo 账户尚未开、8001 自动化桥未通（需先开 demo 并登录，`initialize()` 才能连上）。

## 网络前提验证
```bash
# 腾讯云/国内云：MetaQuotes 全超时 → 不可行
curl -sI https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe   # 腾讯云: 无响应
# 七牛云（可直连国际网络）：HTTP 200, content-length 23784536
```

## 1. 装 Docker + 拉镜像
```bash
apt-get install -y docker.io && systemctl start docker
# 内存不足先加 swap
fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
docker pull gmag11/metatrader5_vnc:latest   # ~6.7GB
```

## 2. 启动容器
```bash
docker run -d --name mt5 \
  -p 3000:3000 -p 8001:8001 \
  -v /opt/mt5_config:/config \
  -e CUSTOM_USER=trader -e PASSWORD=<pass> -e TZ=Asia/Shanghai \
  --restart unless-stopped gmag11/metatrader5_vnc:latest
# 首次 5-10 分钟自动装 MT5，日志看进度：
docker logs mt5 | grep -E '\[[0-9]/7\]'
# 确认终端跑起来：
docker exec mt5 ps aux | grep terminal64
# noVNC 可用（返回 401=需登录，正常）：
curl -sI http://localhost:3000 | head -1
```

## 3. 修复 mt5linux（8001 前提）—— 9 处 Python 3.11 语法
```bash
# 文件在挂载卷上，宿主机直接改（/config → /opt/mt5_config）
DIR=/opt/mt5_config/.local/lib/python3.11/site-packages/mt5linux
python3 - <<'EOF'
import re, glob
pat = re.compile(r'\{\s*\n\s*([^}\n]+)\}')   # 跨行 f-string → 单行
for f in glob.glob("$DIR/*.py"):
    src = open(f, encoding='utf-8').read()
    new, n = pat.subn(lambda m: '{' + m.group(1).strip() + '}', src)
    if n: open(f, 'w', encoding='utf-8').write(new); print(f, n)
EOF
# 验证容器内 3.11 可 import：
docker exec mt5 python3 -c "import mt5linux; print('OK')"
```
覆盖：metatrader5.py(6) + _runtime.py(1) + _base_runtime.py(2)。

## 4. 修复 Windows 侧 numpy 版本（MetaTrader5 库 import 崩溃）
```bash
docker exec -u abc mt5 sh -c 'cd /config && wine python.exe -m pip install "numpy<2" --force-reinstall'
# 症状已消除：AttributeError _ARRAY_API / numpy.core.multiarray failed to import
# 测试连接（注意：未开账户时 INIT: False 是正常的）：
docker exec -u abc mt5 sh -c 'cd /config && wine python.exe -c "import MetaTrader5 as mt5; print(\"INIT:\", mt5.initialize()); mt5.shutdown()"'
```

## 5. 权限与诊断
```bash
# .wine 归容器用户（KasmVNC 镜像为 abc），root 跑 wine 报 not owned → 用 -u abc
docker exec -u abc mt5 ...
# 无头截图看界面（Xvnc :1）：
docker exec mt5 sh -c 'DISPLAY=:1 ffmpeg -y -loglevel error -f x11grab -i :1 -frames:v 1 /tmp/s.png'
docker cp mt5:/tmp/s.png /tmp/mt5_screen.png
```

## 当前结论 / 下一步
- 开 demo：浏览器 `http://<host>:3000` 登录 noVNC → MT5 界面 File→Open an Account→MetaQuotes-Demo（GUI 手动最稳）。
- 终端登录 demo 后 `initialize()` 才能连上；之后再考虑 8001 桥或 MT5 原生 MCP（Build 6060+）。
- 8001 的 start.sh 参数 `-w wine python.exe` 与新版 rpyc_classic 不兼容，若走 RPyC 需绕过；更简路径是自建 HTTP 桥封装 wine python 的 MetaTrader5 调用。
