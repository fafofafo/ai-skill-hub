# linuxserver/chromium + CDP 部署配方（七牛云实测 2026-08-31）

目标：在云主机上跑一个带网页界面的 Chromium，真人通过 VNC WebUI 登录一次（过 reCAPTCHA），之后用 CDP 全自动接管。

## 0. 前置：磁盘
- 拉镜像 `lscr.io/linuxserver/chromium:latest`（压缩 ~1.2G，解压 ~4.6G）**解压时最吃空间**。
- Docker 29 的镜像/容器数据默认在 containerd snapshotter `/var/lib/containerd`（不是 `/var/lib/docker`）。
  - **只改 `/etc/docker/daemon.json` 的 `data-root` 不生效**——镜像解压仍写 `/var/lib/containerd`，系统盘照样满。
  - 迁移命令（新盘已挂载 `/mnt/docker` 时）：
    ```bash
    systemctl stop docker
    mv /var/lib/docker /var/lib/docker.bak      # 可删（验证后）
    echo '{"data-root": "/mnt/docker"}' > /etc/docker/daemon.json
    mv /var/lib/containerd /mnt/docker/containerd
    ln -s /mnt/docker/containerd /var/lib/containerd
    systemctl start docker
    ```
  - 迁移后验证：`docker ps` 容器自动恢复（--restart unless-stopped）；`df -h` 系统盘应释放。
- 七牛云扩容常是**新增一块盘（sdb）而非扩系统盘（vda）**——`lsblk` 确认，然后 `mkfs.ext4 -F /dev/sdb && mount /dev/sdb /mnt/docker`，写 `/etc/fstab`。

## 1. 起容器
```bash
docker run -d --name chromium \
  -p 3002:3000 -p 3003:3001 \
  -e PUID=1000 -e PGID=1000 -e TZ=Asia/Shanghai \
  -e CUSTOM_USER=trader -e PASSWORD=<webui密码> \
  --shm-size=512m --restart unless-stopped \
  lscr.io/linuxserver/chromium:latest
```
WebUI = `http://<host>:3002`（需云安全组放行该端口），登录 CUSTOM_USER/PASSWORD。

## 2. 开启 CDP（改容器内启动脚本）
容器内 `/usr/bin/wrapped-chromium` 是启动器，末尾调用 `${BIN} ... "$@"`。追加参数：
```bash
docker exec chromium sh -c "
  sed -i '/--no-sandbox/a\  --remote-debugging-port=9222 \\\\' /usr/bin/wrapped-chromium
  sed -i '/--remote-debugging-port=9222/a\  --remote-allow-origins=* \\\\' /usr/bin/wrapped-chromium
"
docker restart chromium   # 生效；重启后转发进程需重跑
```

## 3. 容器内端口转发（9222 只绑 127.0.0.1）
把 `scripts/port_forward.py` 复制进容器并后台跑：
```bash
docker cp port_forward.py chromium:/tmp/fwd.py
docker exec -d chromium sh -c 'nohup python3 /tmp/fwd.py > /tmp/fwd.log 2>&1 &'
docker exec chromium sh -c 'cat /tmp/fwd.log'   # "listening 9223"
IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' chromium)
curl -s "http://${IP}:9223/json/version"        # 宿主侧验证
```

## 4. 本机隧道
```bash
ssh -N -L 9222:<容器IP>:9223 -p 10008 -i <key> -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes root@<host>
# 本机验证：
curl -s http://localhost:9222/json/version
```

## 5. CDP 控制
见 `scripts/cdp_op.py`。安装 websocket-client（系统无 pip 时）：
```bash
uv pip install --python /tmp/cdpenv/bin/python websocket-client
```
导航+读页：`python cdp_op.py --navigate https://example.com`
执行 JS：`python cdp_op.py --js 'document.title'`

## 顺序铁律
**所有配置（CDP 参数、转发、隧道）先就绪 → 再让真人登录 → 之后绝不重启容器**。否则登录会话丢失，真人要重新过验证码。

## 已知坑
- WebUI 401 = 认证正常（需 CUSTOM_USER/PASSWORD）。
- 拉镜像中途 `no space left on device` = 磁盘不足，先迁移 containerd（见第 0 节）。
- 容器 IP 在 `docker restart` 后可能变化；隧道目标 IP 要随之更新。
