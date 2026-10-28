---
name: srt-whiteboard-animation
description: Use when 用户要求把图片/字幕做成白板手绘动画视频。已验证全流程+Linux字体坑。
version: 1.0.0
metadata:
  hermes:
    tags: [白板动画, 手绘, 视频, mp4]
---

# SRT 白板动画（已验证可跑 2026-09-16）

把图/SRT 字幕做成暖米黄底手绘动画 MP4。两次实测：示例猴子山 8.6s、RLT 四格漫画 11.6s 均成功。

## 准备（一次性，GitHub 被墙用镜像）
```bash
cd /tmp && rm -rf srt-wb && git clone --depth 1 https://ghfast.top/https://github.com/geeklee/srt-whiteboard-animation.git srt-wb
cd srt-wb && python3 scripts/prepare_env.py   # 输出 ENV_PY=<venv路径>
```

## 快速路径：图 → 白板动画（无需 SRT/人工标注）
1. 输入图转 PNG（JPEG/PNG 均可）：`python3 -c "from PIL import Image; Image.open('in.jpg').convert('RGB').save('scene-01.png')"`
2. 自动生成 N 分区标注（用 scripts/make_annotation.py）：
```bash
python3 scripts/make_annotation.py scene-01.png scene-01.annotation.json --cols 2 --rows 2 --duration 2800
# cols×rows 分区按 Z 字阅读序依次揭示；duration=每格毫秒
```
3. 渲染：
```bash
<ENV_PY> scripts/render_stream_whiteboard.py scene-01.png scene-01.annotation.json out.mp4 assets/drawing-hand.png --ink-path grid --color-fill contour-wipe
```

## SRT 路径（字幕驱动分镜）
```bash
python3 scripts/parse_srt.py 字幕.srt --target-sec 30 --min-sec 25 --max-sec 35  # 出分镜建议
# 之后按 SKILL.md 流程：线稿 → 标注 → 预览台调整 → 渲染
```

## ⚠️ 坑（血泪）
- **Linux 字体坑**：render_annotation_preview.py 写死 `C:/Windows/Fonts/msyh.ttc`，Linux 直接 OSError: cannot open resource。修复：开头加 `import os` + 回退 `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`（渲染主脚本 render_stream_whiteboard.py 无字体依赖，可跳过预览直接渲染）
- 渲染主脚本不需要预览图；预览图只是人工核对区域用
- 输出为暖米黄底+手绘笔迹，不是照片风；任何图都能套（分区揭示+笔迹），不要求图本身是线稿
- 分区多了时长线性增加：N 格 × (duration+300ms) ≈ 总时长

## 📐 输出尺寸规范（仅当用户明确要求白板动画时，2026-09-16）
- **触发条件**：用户明确说"白板动画/手绘动画"才用本技能；没强调时正常用 runhub-image-gen 出图即可，不套白板动画
- **每张图独立成片**：一次只画一张，一张图一个 MP4，不拼图、不合并
- **视频尺寸贴合原图**：渲染加 `--exact-size`（输出=原图尺寸对齐 grid_edge=10 的倍数，差 ≤9px）
- 需打补丁：① stream_render.py Config 加 `exact_size: bool = False` 字段；② render_stream_whiteboard.py 的 `_parse_args` 加 `--exact-size` + `_build_cfg` 透传 + 尺寸逻辑分支（对齐 grid 倍数，否则 `_to_grid_blocks` 报"必须是 10 的整数倍"）
- 单图标注：1 个 element=整图（region 全画布），duration 按图复杂度 4-6s
- 渲染速度：1536×2048 约 2.5 分钟/张（CPU）

## 参考
- 上游：geeklee/srt-whiteboard-animation（MIT，3328★，2026-07 后未更新，一次性能用）
- 完整标注格式见上游 README/annotation 示例（element: region/reveal/handPath）
