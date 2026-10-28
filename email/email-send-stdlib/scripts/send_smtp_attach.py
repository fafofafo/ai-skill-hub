#!/usr/bin/env python3
"""发带附件邮件（stdlib smtplib）。密码/授权码从环境变量 SMTP_CODE 读，不落盘。
用法: SMTP_CODE=<授权码> python3 send_smtp_attach.py <收件人> <附件路径> [主题]
例:   SMTP_CODE=xxxx python3 send_smtp_attach.py me@qq.com /tmp/video.mp4 "视频文件"
QQ:  smtp.qq.com:465  (授权码在 QQ邮箱设置→账户→开启SMTP服务)
"""
import os, sys, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.qq.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SENDER = os.environ.get("SMTP_SENDER", "")  # 必填：发件邮箱
CODE = os.environ.get("SMTP_CODE", "")      # 必填：授权码（不是密码）

if not SENDER or not CODE:
    sys.exit("需要 SMTP_SENDER 和 SMTP_CODE 环境变量")
if len(sys.argv) < 3:
    sys.exit("用法: send_smtp_attach.py <收件人> <附件路径> [主题]")

TO = sys.argv[1]
ATTACH = sys.argv[2]
SUBJECT = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(ATTACH)

msg = MIMEMultipart()
msg["From"] = SENDER
msg["To"] = TO
msg["Subject"] = SUBJECT
msg.attach(MIMEText(f"附件: {os.path.basename(ATTACH)}\n\n自动发送。", "plain", "utf-8"))

with open(ATTACH, "rb") as f:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=os.path.basename(ATTACH))
    msg.attach(part)

# 大附件：timeout 必须加大（默认 60s 传 20MB+ 会 write timeout）
server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=300)
server.login(SENDER, CODE)
server.sendmail(SENDER, [TO], msg.as_string())
server.quit()
print("✅ 发送成功（SMTP 已接受；如需送达确认走 IMAP 读回）")
