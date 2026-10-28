# 多视频复用 & ffmpeg concat 路径坑（2026-08-25）

## img_video.py 合成多视频时必须传绝对路径 + --seg

用同一套脚本批量做多个视频时，`img_video.py` 的默认参数只对 01 号视频有效，直接复用会踩两个坑：

### 坑 1：concat 相对路径双重拼接 → "Impossible to open"
**症状**：合成报 `Impossible to open '.../videos/xxx/videos/xxx/imgclip01.mp4'`（路径出现两次）。片段 clip 明明生成成功。
**根因**：`--work` 传**相对路径**（如 `videos/bibigpt_audio`）时，`str(clip)` 和 list 内容都是相对路径；ffmpeg concat demuxer 把 list 内 `file '...'` 路径**相对 list 文件所在目录**解析，于是相对路径又叠了一层 → 双重。
**修复**：全部用**绝对路径**：
```bash
python3 img_video.py \
  --seg /abs/path/videos/bibigpt_seg.json \
  --imgdir /abs/path/videos/bibigpt_frames \
  --work /abs/path/videos/bibigpt_audio \
  --out /abs/path/videos/bibigpt.mp4 --notitle
```

### 坑 2：漏传 --seg → "图片不足: 6 < 段落 7"
**症状**：多段视频（6 段）但报"图片不足 6 < 7"。
**根因**：`--seg` 默认 `videos/01_seg.json`（7 段）。换了新视频的 seg json 不传就会用旧段数。
**修复**：`--seg videos/<新视频>_seg.json` 显式传。

## 脚本参数速查（多视频复用时）

| 脚本 | 必传参数 |
|---|---|
| `make_audio.py` | `--json videos/X_seg.json --out videos/X_audio [--voice]`（从 seg 的 `text` 字段配音） |
| `gen_poll_images.py` | `--json videos/X_prompts_en.json --outdir videos/X_imgs` |
| `overlay_points.py` | `--json videos/X_seg.json --imgdir videos/X_imgs --outdir videos/X_frames` |
| `img_video.py` | `--seg ... --imgdir ... --work <配音目录> --out ... --notitle`（全绝对路径） |

## 通用原则
- **ffmpeg 涉及多个输入/输出路径时一律用绝对路径**，避免 concat demuxer 的相对目录解析差异。
- 配音目录可同时作为 `--work`（clip 会写到那，可接受）；要保持干净就单独建 work 目录。
