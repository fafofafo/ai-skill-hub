# 远程浏览器 + CDP 接管（实测 2026-08，Guru 接单全自动路径）

场景：用户坚持"只负责验证码，其他全自动"。平台（Guru）登录有 reCAPTCHA + JS 动态表单，
服务器端 curl/无头浏览器都过不了验证码 → 用"远程浏览器容器"让用户登录一次，AI 再 CDP 接管。

## 架构
```
用户浏览器 → linuxserver/chromium WebUI(Selkies, :3002 HTTP / :3003 HTTPS)
              └→ 桌面里的 chromium（真实 GUI，能过 reCAPTCHA）
AI ← CDP websocket ← 容器内 python 转发 127.0.0.1:9222 → 0.0.0.0:9223
   ← SSH 隧道(腾讯云 -L 9222:<容器IP>:9223)
```

## 部署（七牛云，Docker）
```bash
docker run -d --name chromium -p 3002:3000 -p 3003:3001 \
  -e PUID=1000 -e PGID=1000 -e TZ=Asia/Shanghai \
  -e CUSTOM_USER=trader -e PASSWORD=<webui密码> \
  --shm-size=512m --restart unless-stopped \
  lscr.io/linuxserver/chromium:latest
```
- WebUI 有 Basic Auth（CUSTOM_USER/PASSWORD），用户打开 3002 先输这两个才见桌面。
- 容器 IP：`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' chromium`

## 启用 CDP（关键三步，缺一不可）
1. **开调试端口**：容器内改 `/usr/bin/wrapped-chromium`，在 `--no-sandbox` 行后加：
   ```
   --remote-debugging-port=9222 \
   --remote-allow-origins=* \
   ```
   `--remote-allow-origins=*` 必加：Chrome 111+ 不认的话，CDP websocket 握手返回 **403 Forbidden**
   （报错会提示：Use the command line flag --remote-allow-origins=*）
2. **重启容器**（`docker restart chromium`）生效。⚠️ 重启会丢浏览器当前标签页；登录 cookie 若在
   /config 持久化则重登一次即可，**用户登录后不要再重启容器**。
3. **端口转发**（CDP 默认只绑容器内 127.0.0.1，外部连不上）：容器内跑 python TCP 转发：
   ```python
   import socket, threading
   def f(s,d):
       try:
           while True:
               b=s.recv(65536)
               if not b: break
               d.sendall(b)
       except: pass
       finally:
           try: d.shutdown(socket.SHUT_WR)
           except: pass
   def h(c):
       try: r=socket.create_connection(("127.0.0.1",9222))
       except: c.close(); return
       threading.Thread(target=f,args=(c,r),daemon=True).start()
       threading.Thread(target=f,args=(r,c),daemon=True).start()
   s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
   s.bind(("0.0.0.0",9223)); s.listen(50)
   while True:
       c,_=s.accept(); threading.Thread(target=h,args=(c,),daemon=True).start()
   ```
   `docker exec -d chromium sh -c 'nohup python3 /tmp/fwd.py > /tmp/fwd.log 2>&1 &'`

## 腾讯云接入
- 隧道：`ssh -N -L 9222:172.17.0.3:9223 -p 10008 root@your-server-ip`
  （目标 = 容器 IP:9223，在七牛云宿主侧解析）
- CDP 客户端：`uv venv /tmp/cdpenv && uv pip install --python /tmp/cdpenv/bin/python websocket-client`
- 用法：
  - `GET http://localhost:9222/json/list` — 列出标签页，拿 `webSocketDebuggerUrl`
  - websocket 连该 URL → 发 `{"id":1,"method":"Page.navigate","params":{"url":"..."}}`
  - `Runtime.evaluate` 传 JS（returnByValue:true）读标题/URL/body 文本/DOM
  - 工具：CDP 里 `location.href+'||'+document.title` 检查登录态；页面含 "Log In/Sign Up" = 未登录

## 已验证结论（Guru 2026-08）
- Guru 数据中心 IP 可访问（HTTP 200），但登录是 **JS 动态表单**（username/password 字段不在静态
  HTML，CDP 查询只有 hidden 的 __VIEWSTATE 等）→ 自动填表不可行，**用户必须在 WebUI 里手动
  输账号密码 + 过验证码**。AI 接管的是"登录后"的浏览操作。
- 登录态检查：打开 `guru.com/d/jobs/`，body 含 "Log In"/"Sign Up" 链接 = 未登录。

## 磁盘前提（七牛云 19G 系统盘太小）
- 先扩盘/挂新盘（`mkfs.ext4 /dev/sdb; mount /dev/sdb /mnt/docker`，写 /etc/fstab）。
- **Docker 两处存储都要迁到新盘**，只改 daemon.json data-root 不够：
  - `/var/lib/docker` → daemon.json `{"data-root":"/mnt/docker"}`
  - `/var/lib/containerd` → `mv /var/lib/containerd /mnt/docker/containerd && ln -s /mnt/docker/containerd /var/lib/containerd`
    （Docker 29 用 containerd snapshotter，镜像层解压写 /var/lib/containerd，不迁它照样满）
- 迁完 `systemctl restart docker`，容器 `--restart unless-stopped` 会自动拉起；桥有守护会恢复。
