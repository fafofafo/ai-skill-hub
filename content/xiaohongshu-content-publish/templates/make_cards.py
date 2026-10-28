#!/usr/bin/env python3
"""小红书信息图批量生成模板（RunningHub 复古底图 + PIL 叠中文）。
用法：改 SERIES/CARDS 数组（name, 顶部大标题, 底部技术要点, 底图提示词），
     底图提示词末尾统一加 "no text, no letters, no words"（图内文字用 PIL 叠，避免 AI 中文翻车）。
运行：python3 make_cards.py （需 venv 含 PIL + runhub_img；队列满自动重试 30s）
"""
import sys, os, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_BIG = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
STYLE = ("Modern pencil illustration, 1950s-60s retro travel poster, silkscreen texture, "
         "bold saturated high-contrast palette, flat color blocks, misregistration grain, "
         "mid-century optimistic graphic simplification, cinematic composition")

# name, 顶部大标题, 底部技术要点(每行一条), 底图提示词(意象直指主题)
CARDS = [
    ("封面", "标题", "副标题\n一句话说明", "A vintage scene ... no text, no letters, no words"),
]

OUT = Path.home() / "tools" / "runhub" / "系列名"


def gen_base(prompt, path):
    import runhub_img  # ~/tools/runhub/runhub_img.py
    for attempt in range(6):
        try:
            runhub_img.t2i(STYLE + ". " + prompt, ratio="3:4", res="2k", out=str(path))
            return Image.open(path).convert("RGB")
        except Exception as e:
            print(f"  队列重试 {attempt+1}: {str(e)[:60]}，30s 后重试")
            time.sleep(30)  # RunningHub 421 TASK_QUEUE_MAXED 时等待释放
    raise RuntimeError("多次重试失败")


def overlay(img, big, sub):
    W, H = img.size
    d = ImageDraw.Draw(img, "RGBA")
    f_big = ImageFont.truetype(FONT_BIG, int(W * 0.075))
    f_sub = ImageFont.truetype(FONT_BIG, int(W * 0.046))
    d.rectangle([0, 0, W, int(H * 0.13)], fill=(20, 24, 40, 205))
    d.text((W // 2, int(H * 0.062)), big, font=f_big, fill=(255, 235, 140), anchor="mm")
    lines = sub.split("\n")
    bh = int(H * 0.30)
    d.rectangle([0, H - bh, W, H], fill=(15, 18, 32, 218))
    y = H - bh + int(H * 0.028)
    for i, ln in enumerate(lines):
        d.text((W // 2, y + i * int(H * 0.055)), ln, font=f_sub, fill=(245, 245, 250), anchor="mm")
    return img


def main():
    os.chdir(Path.home() / "tools" / "runhub")
    sys.path.insert(0, str(Path.home() / "tools" / "runhub"))
    OUT.mkdir(parents=True, exist_ok=True)
    for name, big, sub, prompt in CARDS:
        final_p = OUT / f"{name}.png"
        if final_p.exists():
            print(f"跳过: {name}")
            continue
        print(f"▶ {name}…")
        img = gen_base(prompt, OUT / f"_{name}_base.png")
        img = overlay(img, big, sub)
        img.save(final_p)
        print(f"  ✅ {name}")
        time.sleep(3)  # 错峰，降低撞队列概率


if __name__ == "__main__":
    main()
