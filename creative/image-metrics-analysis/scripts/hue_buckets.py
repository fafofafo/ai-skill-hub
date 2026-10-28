#!/usr/bin/env python3
"""色相分布量化（学色调用，VL 不可用时补充五元素分析）。

用法:
    python3 scripts/hue_buckets.py <图片1> [图片2 ...]

输出: 每张图按 30° 色相桶统计有色彩像素（S>40）占比，标出主导色相区间。
用途: R-B 只给冷暖方向；色相桶分布给「主色相到底是什么色、占多少」。
例: 青(120-150°)占 62-72% + 青蓝(150-180°)占 13-26% → 「青蓝系 85-95% 绝对主导」。
"""
import collections
import sys
from PIL import Image

BUCKET_NAMES = {
    0: "红/橙(0-30)", 1: "橙/黄(30-60)", 2: "黄/绿(60-90)", 3: "绿/青(90-120)",
    4: "青(120-150)", 5: "青/蓝(150-180)", 6: "蓝(180-210)", 7: "蓝/紫(210-240)",
    8: "紫/粉(240-270)", 9: "粉/红(270-300)", 10: "红(300-330)", 11: "红(330-360)",
}

for path in sys.argv[1:]:
    im = Image.open(path).convert("RGB")
    hsv = im.convert("HSV")
    hue_buckets = collections.Counter()
    for (h, s, v) in hsv.getdata():
        if s > 40:  # 只统计有色彩像素，跳过灰白/中性色
            hue_buckets[h // 30] += 1
    total_colored = sum(hue_buckets.values())
    print(f"=== {path.split('/')[-1]} ===")
    if total_colored == 0:
        print("  无彩色像素（画面为纯灰/纯黑白）")
        continue
    for bucket in range(12):
        pct = hue_buckets[bucket] / total_colored * 100
        if pct > 1:
            print(f"  {BUCKET_NAMES[bucket]:<12} {pct:5.1f}%")
