# Guru 海外接单 · 服务器自动化边界与远程浏览器方案（2026-08 实测）

## 为什么服务器端登录 Guru 不可行（根因，别重复试）
1. **登录表单是 JS 动态渲染**（Angular/React SPA）：用户名/密码输入框**不在静态 HTML 里**。`curl` 抓登录页只能拿到隐藏的 social-login clientID + __VIEWSTATE，没有 user/password 字段可提交。
2. **reCAPTCHA**：登录/注册页加载 `recaptcha/api.js`。数据中心 IP（腾讯云/七牛云都是）一律被判为机器人。`hdnIsCaptchaEnabled=True`。
3. **browser_exec（服务器无头浏览器）加载 Guru 超时**（90s/120s/180s 均超时；页面资源重 + 数据中心到 Guru 的浏览器流量慢）。curl 能通（HTTP 200）但浏览器不行——不要再用 browser_exec 试 Guru。
4. Upwork 则是**封所有数据中心 IP（HTTP 403）**，与 Guru 机制不同但结果一样：服务器端操作不了。

结论：**投递报价必须发生在"已登录的账号会话"里，而该会话在用户手机/家用浏览器——AI 服务器够不着**。这是平台反机器人墙，不是网络/配置问题，不要向用户承诺全自动登录操作。

## 已证伪的路径（不要再花时间）
- curl 模拟登录（JS 动态表单 + reCAPTCHA）❌
- browser_exec 加载 Guru ❌（超时）
- 复用用户手机登录会话 ❌（会话隔离，服务器拿不到 cookie）
- 七牛云换 IP 访问 Upwork ❌（403 同样发生）

## 可行路径：远程浏览器方案（用户只管验证码）
用户诉求"只负责验证码、其他 AI 全自动"时，用七牛云跑一个远程桌面浏览器容器，用户登录一次后会话留在服务器：
```bash
docker run -d --name chromium \
  -p 3002:3000 -p 3003:3001 \
  -e PUID=1000 -e PGID=1000 -e TZ=Asia/Shanghai \
  -e CUSTOM_USER=trader -e PASSWORD=<设置> \
  --shm-size=512m --restart unless-stopped \
  lscr.io/linuxserver/chromium:latest
```
- 用户访问 `http://<七牛云IP>:3002` → 登录 WebUI（CUSTOM_USER/PASSWORD）→ 在远程浏览器里开 Guru → 登录过验证码（仅此一次）
- WebUI 返回 401 = 正常（有认证，用 CUSTOM_USER/PASSWORD 登录）
- **必须放行云安全组端口 3002/3003**（云安全组在主机 UFW 之外；主机 ufw allow 不够，要用户在云控制台加规则）

## 磁盘前提：七牛云 19G 装不下 chromium（解压 ~1.2G）
云盘扩容常表现为**新增一块数据盘（如 /dev/sdb 50G，未挂载）**而不是扩展系统盘。步骤：
1. `mkfs.ext4 /dev/sdb && mkdir /mnt/docker && mount /dev/sdb /mnt/docker && echo '/dev/sdb /mnt/docker ext4 defaults 0 2' >> /etc/fstab`
2. **Docker 29 用 containerd snapshotter**：`daemon.json` 的 `data-root` 只移 docker 镜像层，**解压仍写 `/var/lib/containerd`（在系统盘）**，磁盘满照样失败。必须同时迁移：
   - `systemctl stop docker`
   - `rsync -a /var/lib/docker/ /mnt/docker/` → `echo '{"data-root": "/mnt/docker"}' > /etc/docker/daemon.json`
   - `mv /var/lib/containerd /mnt/docker/containerd && ln -s /mnt/docker/containerd /var/lib/containerd`
   - `systemctl start docker`（容器 --restart unless-stopped 会自动拉起，桥守护会拉起桥）
3. 迁移完成后系统盘从 90% → ~59%；chromium 拉取才成功。

## 自动找单（已验证可用，无需登录）
- 任务列表 `curl https://www.guru.com/d/jobs/` 可抓（无需登录），正则提取 `/jobs/<slug>/<id>` 链接。
- 脚本 `~/项目目录/guru_job_finder.py` → 复制 `~/.hermes/scripts/`，cron `no_agent` 每 6h：有匹配单推送、无匹配静默（watchdog 模式，零 token）。
- 关键词子串坑：`"ai"` 匹配到 `"paid"`/`"detail"`。用排除词表 + 长关键词（chatbot/ai agent/automation/gpt/plugin/developer/api/integration/rag）。
