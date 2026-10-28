# social-auto-upload 安装配置踩坑（2026-09 实测）

## 安装
```bash
mkdir -p ~/tools && cd ~/tools
git clone --depth 1 https://github.com/dreammis/social-auto-upload.git
cd social-auto-upload
uv sync            # 装 patchright 等（uv 建的 venv 无 pip，用 uv pip install 补）
cp conf.example.py conf.py
UV_INDEX_URL=https://mirrors.cloud.tencent.com/pypi/simple uv pip install playwright pillow
```

## ⚠️ 浏览器内核（最大坑）
patchright 默认找**它专属的 chromium build**（版本号如 1208）；缺失时所有 launcher 报 `Executable doesn't exist at ...chromium_headless_shell-<版本>...`。
- 报错 `unknown flag 'disable-field-trial-config'` = 用系统 Chrome（/usr/bin/google-chrome），不可用；但**已存在的 ms-playwright chromium 可以**（实测 chromium-1234/chrome-linux64/chrome 跑通登录+verify_notes）

优先方案：官方 CDN 装专属 build（不要设 npmmirror 镜像，会 Download failure）：
```bash
unset PLAYWRIGHT_DOWNLOAD_HOST
.venv/bin/python -m playwright install chromium-headless-shell
```
CDN 卡 0% 时（被墙）不要死等：`kill` 下载进程，改用缓存里已有的完整版 chromium：
`executable_path="/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome"`

## conf.py 关键配置
```python
LOCAL_CHROME_PATH = "/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome"  # 有现成 chromium 就填，别填系统 Chrome
LOCAL_CHROME_HEADLESS = True
DEBUG_MODE = True
```
⚠️ 填了 LOCAL_CHROME_PATH 后，**裸 `chromium.launch(headless=...)` 的代码不会自动用它**——须在每个 launch 处加 `if LOCAL_CHROME_PATH: options['executable_path']=LOCAL_CHROME_PATH`（或 kwargs 展开）。

## 登录（无头服务器）
`sau xiaohongshu login --account <名> --headless` → 无头模式生成**终端二维码+PNG 图片**，PNG 存 `cookies/xiaohongshu_<名>_xhs_login_qrcode_<时间戳>.png`，用 MEDIA 发图让用户扫码。
- CLI 登录实际走 **`uploader/xiaohongshu_uploader/main.py` 的 xiaohongshu_setup**，不是 `myUtils/login.py`——改 launch 先 grep 真实入口（sau_cli.py 分发），别改错文件
- 二维码 **5 分钟过期**，过期需重跑
- 用户扫的是哪个号就绑定哪个号（要先用小号就明确让用户登小号）
- 登录成功后 cookie 存 `cookies/xiaohongshu_<名>.json`
- cookie 失效判据：verify_notes.py 报"未找到 note-card"≠一定没登录；写调试脚本抓 page.url，跳 `creator.xiaohongshu.com/login?...redirectReason=401` = cookie 过期要重登，页面正常加载=选择器变了

## 常用命令
```bash
.venv/bin/sau xiaohongshu check --account <名>       # cookie 校验
.venv/bin/sau xiaohongshu upload-note --account <名> --images a.png b.png --title T --note N --tags t1,t2
```
