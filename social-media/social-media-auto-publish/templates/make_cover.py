#!/usr/bin/env python3
"""PIL 生成小红书封面图（1080x1440 竖版，中文大字）。
用法: python3 make_cover.py [输出路径]
依赖: pillow；中文字体 wqy-zenhei（Ubuntu: fonts-wqy-zenhei）
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
W, H = 1080, 1440
OUT = sys.argv[1] if len(sys.argv) > 1 else "封面.png"

img = Image.new("RGB", (W, H), (15, 23, 42))
d = ImageDraw.Draw(img)
big = ImageFont.truetype(FONT, 78)
mid = ImageFont.truetype(FONT, 44)
sm = ImageFont.truetype(FONT, 32)

d.text((W/2, 300), "我用 AI 团队", font=big, fill=(255, 255, 255), anchor="mm")
d.text((W/2, 400), "替我干活", font=big, fill=(255, 255, 255), anchor="mm")
d.text((W/2, 530), "每天省 3 小时", font=big, fill=(250, 204, 21), anchor="mm")
d.text((W/2, 700), "副标题（改这里）", font=mid, fill=(180, 190, 210), anchor="mm")
d.text((W/2, 860), "要点1 → 要点2 → 要点3", font=mid, fill=(120, 220, 180), anchor="mm")
d.text((W/2, 1080), "引导语：评论区扣 XX 领取", font=sm, fill=(250, 204, 21), anchor="mm")
d.text((W/2, 1300), "日期/署名", font=sm, fill=(120, 128, 150), anchor="mm")

img.save(OUT)
print(f"✅ 封面已生成: {OUT}")
