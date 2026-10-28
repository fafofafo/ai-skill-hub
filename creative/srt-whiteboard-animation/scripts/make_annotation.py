#!/usr/bin/env python3
"""按 cols×rows 网格自动生成白板动画 annotation.json（Z 字阅读序）
用法: python3 make_annotation.py <图片> <输出annotation.json> [--cols 2] [--rows 2] [--duration 2800] [--story "..."]
"""
import json, sys, argparse
from PIL import Image

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("output")
    ap.add_argument("--cols", type=int, default=2)
    ap.add_argument("--rows", type=int, default=2)
    ap.add_argument("--duration", type=int, default=2800, help="每格揭示时长 ms")
    ap.add_argument("--story", default="", help="场景简述")
    a = ap.parse_args()

    img = Image.open(a.image).convert("RGB")
    W, H = img.size
    cw, ch = W // a.cols, H // a.rows
    elements = []
    for r in range(a.rows):
        for c in range(a.cols):
            i = r * a.cols + c + 1
            ox, oy = c * cw, r * ch
            elements.append({
                "id": f"cell_{r}_{c}", "label": f"分区{i}",
                "sequence": i, "narrativeRole": f"第{i}格",
                "subtitle": "", "type": "structure",
                "region": {"x": ox, "y": oy, "width": cw, "height": ch},
                "reveal": {"direction": "top_to_bottom", "startMs": 300 + (i-1)*(a.duration+300),
                           "durationMs": a.duration, "maskPaddingPx": 18, "protectedRegions": []},
                "handPath": {"start": [ox + cw//2, oy + 40], "end": [ox + cw//2, oy + ch - 40],
                             "easing": "easeInOut"},
            })
    total = 300 + len(elements) * (a.duration + 300)
    ann = {"sceneId": "scene-01", "canvas": {"width": W, "height": H},
           "storyBasis": a.story, "sceneDurationMs": total, "elements": elements}
    json.dump(ann, open(a.output, "w"), ensure_ascii=False, indent=2)
    print(f"OK {a.cols}x{a.rows}={len(elements)} 分区, 总时长 {total}ms -> {a.output}")

if __name__ == "__main__":
    main()
