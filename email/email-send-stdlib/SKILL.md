---
name: email-send-stdlib
description: Use when 发邮件/带附件邮件（QQ 等 SMTP）。stdlib smtplib 零依赖，含读回验证。
---

# 发邮件（stdlib smtplib，零依赖）

## 用户交付偏好（2026-09-29 起）
- **所有成品/结果默认发 QQ 邮箱**（345469023@qq.com），用户未主动要求时**不要**发企微/聊天附件。
- 授权码已存环境变量 `QQ_SMTP_CODE`，直接读即可，无需再向用户索要。

## When to Use
- 用户要求把文件/结果发到邮箱（本会话：把 22MB 视频发 QQ 邮箱）。
- himalaya/CLI 未配置时直接用 Python smtplib，无需安装任何东西。

## 流程
1. **确认发件账号 + SMTP 服务**：QQ 邮箱 = `smtp.qq.com:465`（SSL）；国内主流邮箱同理（163: smtp.163.com:465，Gmail: smtp.gmail.com:465 需应用专用密码）。
2. **授权码（不是登录密码）**：QQ 邮箱需用户在 设置→账户→开启 SMTP 服务→生成 16 位授权码。授权码通过**环境变量**传给脚本（`QQ_SMTP_CODE`），不留知识库/聊天。**2026-09-29 起用户已提供授权码并同意留存**（存环境变量供脚本读取，不再每次要码、不提示撤销）；若用户后续要求撤销再提醒。
3. **MIME 组装**：`MIMEMultipart` + `MIMEText(body, "plain", "utf-8")`（中文正文必须带 utf-8）+ 附件 `MIMEBase` + `encoders.encode_base64` + `Content-Disposition: attachment`。
4. **发送**：`smtplib.SMTP_SSL(host, 465, timeout=300)` → `login` → `sendmail`。
5. **读回验证（外部状态验证，必做）**：IMAP `imap.qq.com:993` 用同一授权码登录 → 收件箱最新一封的 From/Subject 吻合 → 才算发送成功（SMTP 250 只是服务器已接受，不证明送达）。**中文主题搜不到**：QQ IMAP 用 `SUBJECT "中文"` 搜索返回 0 命中，改用 `SINCE <DD-Mon-YYYY>` 拉当天邮件列最新几封头（From/Subject/附件名）；**且拉到的 Subject 是 RFC2047 base64**（`=?utf-8?b?...?=`），直接 grep 中文必然落空——必须 `email.header.decode_header(Subject)` 解码后再比对（逐段 decode 拼接）；带附件邮件比对附件 payload 大小与本地文件一致才算完整送达。

## 陷阱
- **QQ 邮箱附件上限（静默失败坑）**：QQ 附件上限约 50MB 且按 base64 传输后大小计（RFC822.SIZE ≈ 本地文件×1.33）；本地文件 ≥37MB 发送会**静默失败**——SMTP 无报错、脚本可能显示"已接受"，但收件箱永远收不到。超限先压缩再发（视频 `ffmpeg -crf 28` 一般 40MB→27MB），发完必须 IMAP 读回最新主题 + RFC822.SIZE（≈ 本地×1.33 视为完整）确认，不能信发送脚本的成功提示。**发送脚本输出为空（连 ✅ 都没有，只剩 cwd 行）同样是未发出信号**——IMAP 读回最新主题仍是上一封时直接重发一次再确认，不要当作成功继续。
- **大附件 SSL write 超时**：默认 `timeout=60` 传 20MB+ 附件会在 `sendall` 报 `TimeoutError: The write operation timed out` → 把 timeout 提到 300s（连接本身通，是传输慢）。
- **授权码不要硬编码进脚本/聊天**：环境变量传入；临时脚本用完删除。
- **中文文件名/主题**：Subject 建议用 ASCII 或加前缀说明（QQ 对 RFC2047 编码主题显示正常，但纯 ASCII 最稳）；附件 filename 用 ASCII。
- 连接慢时先 `openssl s_client -connect smtp.qq.com:465 -brief` 测连通，区分"网络不通"和"传输慢"。

## 脚本
- `scripts/send_smtp_attach.py`：调用形式是**位置参数** `SMTP_SENDER=<发件> SMTP_CODE=<授权码> python3 scripts/send_smtp_attach.py <收件人> <附件路径> [主题]`——环境变量名是 `SMTP_SENDER`/`SMTP_CODE`（不是 `SENDER`/`TO`，TO 是第一个位置参数不是环境变量），传错名会报 "需要 SMTP_SENDER 和 SMTP_CODE"；正文固定为"附件: …自动发送"，要自定义正文就自己写 MIMEText 不用此脚本。
