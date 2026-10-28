#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
img_metrics.py — 画面六维量化分析（纯 PIL 实现，无需 numpy/opencv）

用途：对任意图片（含视频抽帧）输出饱和度/高饱和像素/锐度(拉普拉斯)/边缘密度/明度/对比-柔度六维指标，
用于客观描述画风、与视觉模型定性描述互相印证、或对比多帧/多版本调色差异。

用法：
    python3 img_metrics.py <图片路径> [更多图片...]

口径说明：
- 饱和度：HSV S 通道均值与标准差（PIL convert('HSV')，S 取 0-255）
- 高饱和像素：S≥60% 与 S≥80% 两档像素占比
- 锐度：4-邻域拉普拉斯卷积的方差（与 OpenCV cv2.Laplacian(gray, CV_64F).var() 口径对齐）
  PIL Kernel 会裁剪负数，故用 scale=4.0 缩放后算方差再 ×16 还原真实值
- 边缘密度：FIND_EDGES 后统计 >20 / >40 的像素占比；另给 Sobel gx/gy 梯度幅值
- 明度：灰度均值 + HSV-V 均值（两者差异大 = 高饱和画面）
- 对比：灰度标准差 + P5-P95 动态范围
- 柔度：局部高频残差均值 / 全局对比（BoxBlur(3) 残差；<0.10 很柔 / <0.16 偏柔 / <0.24 中等 / ≥0.24 偏锐）
"""
import sys, math
from PIL import Image, ImageFilter, ImageStat, ImageChops


def analyze(path):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    N = W * H
    gray = im.convert('L')

    # 1 饱和度
    hsv = im.convert('HSV')
    S, V = hsv.getchannel('S'), hsv.getchannel('V')
    s_hist = S.histogram()
    s_mean = sum(i * c for i, c in enumerate(s_hist)) / N
    s_std = math.sqrt(max(sum((i ** 2) * c for i, c in enumerate(s_hist)) / N - s_mean ** 2, 0))

    # 2 高饱和像素
    hi60 = sum(s_hist[int(0.60 * 255):]) / N * 100
    hi80 = sum(s_hist[int(0.80 * 255):]) / N * 100

    # 3 锐度（拉普拉斯方差）
    lap = gray.filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=4.0, offset=128))
    lst = ImageStat.Stat(lap)
    lap_var = lst.stddev[0] ** 2 * 16
    lap_abs = abs(lst.mean[0] - 128) * 4

    # 4 边缘密度
    edge = gray.filter(ImageFilter.FIND_EDGES)
    e_hist = edge.histogram()
    ed20 = sum(e_hist[20:]) / N * 100
    ed40 = sum(e_hist[40:]) / N * 100
    edge_mean = sum(i * c for i, c in enumerate(e_hist)) / N
    gx = gray.filter(ImageFilter.Kernel((3, 3), [-1, 0, 1, -2, 0, 2, -1, 0, 1], scale=4.0, offset=128))
    gy = gray.filter(ImageFilter.Kernel((3, 3), [-1, -2, -1, 0, 0, 0, 1, 2, 1], scale=4.0, offset=128))
    sx = ImageStat.Stat(gx).stddev[0] * 4
    sy = ImageStat.Stat(gy).stddev[0] * 4
    sobel = math.hypot(sx, sy)

    # 5 明度
    g_hist = gray.histogram()
    g_mean = sum(i * c for i, c in enumerate(g_hist)) / N
    g_std = math.sqrt(max(sum((i ** 2) * c for i, c in enumerate(g_hist)) / N - g_mean ** 2, 0))
    v_mean = ImageStat.Stat(V).mean[0]

    # 6 对比 / 柔度
    smooth = gray.filter(ImageFilter.BoxBlur(3))
    res = ImageChops.difference(gray, smooth)
    res_mean = ImageStat.Stat(res).mean[0]
    softness = res_mean / g_std if g_std else 0
    verdict = '很柔' if softness < 0.10 else '偏柔' if softness < 0.16 else '中等' if softness < 0.24 else '偏锐'

    def pctile(hist, p):
        tgt = N * p / 100; acc = 0
        for i, c in enumerate(hist):
            acc += c
            if acc >= tgt: return i
        return 255
    p05, p50, p95 = pctile(g_hist, 5), pctile(g_hist, 50), pctile(g_hist, 95)

    # 7 色调（第六元素：主色相判定，2026-10-27 用户定）
    # 按 HSV 色相分 12 桶，S>40 才算有彩色像素，输出主色相桶+占比
    hdata = list(hsv.getdata())
    hue_buckets = {}
    colored = 0
    for (h, s, v) in hdata:
        if s > 40:
            colored += 1
            b = h // 30
            hue_buckets[b] = hue_buckets.get(b, 0) + 1
    HUE_NAMES = {
        0: "红/橙", 1: "橙/黄", 2: "黄/绿", 3: "绿/青", 4: "青",
        5: "青/蓝", 6: "蓝", 7: "蓝/紫", 8: "紫", 9: "紫/粉", 10: "粉/红", 11: "红",
    }
    if colored:
        sorted_buckets = sorted(hue_buckets.items(), key=lambda kv: -kv[1])
        top_pct = sorted_buckets[0][1] / colored * 100
        top_name = HUE_NAMES[sorted_buckets[0][0]]
        # 汇总：相邻桶合并成主色域
        main_hue = top_name
    else:
        main_hue, top_pct = "中性（低饱和）", 0.0

    r_mean, g_mean_c, b_mean = ImageStat.Stat(im).mean

    print(f"\n{'='*64}\n{path}    {W}x{H}    {N} px\n{'='*64}")
    print(f"[1 饱和度]     S 均值 {s_mean/255*100:.1f}%   S 标准差 {s_std/255*100:.1f}%")
    print(f"[2 高饱和像素]  S>=60%: {hi60:.2f}%   S>=80%: {hi80:.2f}%")
    print(f"[3 锐度 Lap]   Laplacian 方差 {lap_var:.1f}   |Lap| 均值 {lap_abs:.2f}")
    print(f"[4 边缘密度]    FIND_EDGES 均值 {edge_mean:.2f}   >20: {ed20:.2f}%   >40: {ed40:.2f}%")
    print(f"               Sobel 梯度幅值 {sobel:.1f}  (|gx| {sx:.1f} / |gy| {sy:.1f})")
    print(f"[5 明度]       灰度均值 {g_mean:.1f}/255 ({g_mean/255*100:.1f}%)   HSV-V {v_mean:.1f}/255   中位 {p50}")
    print(f"[6 对比/柔度]  灰度 std {g_std:.1f}   动态范围(P95-P5) {p95-p05}   局部高频残差 {res_mean:.2f}")
    print(f"               柔度指数 {softness:.3f} → {verdict}")
    print(f"[7 色调]       主色相 {main_hue}（占彩色 {top_pct:.1f}%）  [色温 R-B {r_mean-b_mean:+.1f}]")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    for p in sys.argv[1:]:
        try:
            analyze(p)
        except Exception as e:
            print(f"{p}: 分析失败 {e}")
