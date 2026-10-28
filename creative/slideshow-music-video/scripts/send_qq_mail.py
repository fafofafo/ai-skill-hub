#!/usr/bin/env python3
"""QQ 邮箱带附件发送模板（smtplib，无需 himalaya）。
用法: QQ_SMTP_CODE='<授权码>' python3 send_qq_mail.py <附件路径> <主题>
授权码：QQ邮箱→设置→账户→开启SMTP→生成（可随时撤销）；不留文件/知识库。
"""
import smtplib, sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

SENDER = "345469023@qq.com"
AUTH = os.environ["QQ_SMTP_CODE"]
TO = "345469023@qq.com"

att = sys.argv[1]
subject = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(att)
body = sys.argv[3] if len(sys.argv) > 3 else f"附件：{os.path.basename(att)}\n来自 Hermes 自动发送。\n"

msg = MIMEMultipart()
msg["From"] = f"Hermes <{SENDER}>"
msg["To"] = TO
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain", "utf-8"))

# 按扩展名给 MIME 类型（视频/文档通用）
ext_map = {".mp4": ("video", "mp4"), ".png": ("image", "png"), ".jpg": ("image", "jpeg"), ".pdf": ("application", "pdf"), ".md": ("text", "markdown"), ".zip": ("application", "zip")}
sub = os.path.splitext(att)[1].lower()
mtype, msub = ext_map.get(sub, ("application", "octet-stream"))

with open(att, "rb") as f:
    part = MIMEBase(mtype, msub)
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=os.path.basename(att))
    msg.attach(part)

# ⚠️ 大附件（>10MB）SSL 传输慢：timeout 必须 ≥300，否则 write timeout
server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=300)
server.login(SENDER, AUTH)
server.sendmail(SENDER, [TO], msg.as_string())
server.quit()
print("✅ 邮件发送成功")

# 验证（读回收件箱确认）：可选，发送后建议做
# import imaplib, email
# M = imaplib.IMAP4_SSL("imap.qq.com", 993, timeout=60)
# M.login(SENDER, AUTH); M.select("INBOX")
# typ, data = M.search(None, "ALL"); ids = data[0].split()
# for i in ids[-2:]:
#     typ, d = M.fetch(i, "(BODY.PEEK[HEADER.FIELDS (SUBJECT DATE)])")
#     msg = email.message_from_bytes(d[0][1])
#     print(f"[{i.decode()}] {msg['Date']} | {msg['Subject']}")
# M.logout()
