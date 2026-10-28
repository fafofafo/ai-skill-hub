#!/usr/bin/env python3
"""AI 视频自动生成器：分段口播 → 配音 → 文字卡片段 → 拼接完整 MP4。

用法：
  python3 gen_video.py --title "标题" --json seg.json --out out.mp4 [--voice zh-CN-YunxiNeural]

seg.json 格式（每段一个对象）：
[
  {"card": "文字卡大字（≤14字）", "sub": "卡片小字（可空）", "text": "本段口播全文"},
  ...
]

流程：每段 edge-tts 配音 → ffmpeg 合成深色背景+文字卡片段 → concat 完整视频。
依赖：~/video-venv（edge-tts，用 `uv venv ~/video-venv && uv pip install --python ~/video-venv/bin/python -i <pypi-mirror> edge-tts` 装）
      + 系统 ffmpeg + 中文字体（`sudo apt install -y fonts-wqy-zenhei`）
已知陷阱已内置：edge-tts 连续请求限流（每段间 sleep 2s + TTS 重试指数退避）；音频 <2KB 视为失败。
"""
import argparse
import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).parent
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
RES = "1920x1080"
FPS = 30


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"命令失败: {' '.join(cmd[:8])}...\n{r.stderr[-800:]}")


async def tts(text: str, out: Path, voice: str, retries: int = 4) -> None:
    import edge_tts
    last: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            await edge_tts.Communicate(text, voice).save(str(out))
            if out.stat().st_size > 2000:
                return
            raise RuntimeError("音频过小，可能为空")
        except Exception as e:  # noqa: BLE001
            last = e
            wait = 3 * attempt
            print(f"        ⚠ TTS 第{attempt}次失败({type(e).__name__})，{wait}s 后重试…")
            await asyncio.sleep(wait)
    raise RuntimeError(f"TTS 多次失败: {last}")


def card_clip(card: str, sub: str, audio: Path, out: Path) -> None:
    """一张深色文字卡 + 该段配音 → 片段 mp4（时长=音频）。"""
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(audio)]).decode().strip())
    n_chars = len(card)
    fsize = 120 if n_chars <= 8 else (100 if n_chars <= 12 else 84)
    # 换行：超长标题每行 ≤12 字
    if n_chars > 14:
        lines = [card[i:i + 12] for i in range(0, n_chars, 12)]
        card_txt = "\\n".join(lines)
    else:
        card_txt = card
    esc = lambda s: s.replace(":", "\\:").replace("'", "\\'")
    vf = (
        f"drawtext=fontfile={FONT}:text='{esc(card_txt)}':"
        f"fontcolor=white:fontsize={fsize}:line_spacing=20:"
        f"x=(w-text_w)/2:y=(h-text_h)/2-120"
    )
    if sub:
        vf += (f",drawtext=fontfile={FONT}:text='{esc(sub)}':"
               f"fontcolor=0x88c0ff:fontsize=48:"
               f"x=(w-text_w)/2:y=(h-text_h)/2+120")
    run(["ffmpeg", "-y", "-f", "lavfi", "-i",
         f"color=c=0x12121e:s={RES}:r={FPS}",
         "-i", str(audio),
         "-filter_complex", f"[0:v]{vf}[v]",
         "-map", "[v]", "-map", "1:a", "-shortest",
         "-c:v", "libx264", "-preset", "fast",
         "-c:a", "aac", "-b:a", "160k",
         "-pix_fmt", "yuv420p", str(out)])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--json", required=True, help="分段定义 json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--voice", default="zh-CN-YunxiNeural")
    args = ap.parse_args()

    segs = json.loads(Path(args.json).read_text(encoding="utf-8"))
    work = BASE / "videos" / ".work"
    work.mkdir(parents=True, exist_ok=True)
    clips = []

    for i, s in enumerate(segs, 1):
        audio = work / f"seg{i:02d}.mp3"
        clip = work / f"clip{i:02d}.mp4"
        print(f"  [{i}/{len(segs)}] 配音: {s['text'][:24]}…")
        asyncio.run(tts(s["text"], audio, args.voice))
        card_clip(s.get("card", f"第{i}节"), s.get("sub", ""), audio, clip)
        clips.append(clip)
        print(f"        → {clip.name} 完成")
        time.sleep(2)  # 节间间隔，避免 edge-tts 限流

    # concat
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips), encoding="utf-8")
    out = Path(args.out)
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(out)])
    print(f"\n🎬 完成: {out} ({out.stat().st_size/1024/1024:.1f} MB)")

    for c in clips:
        c.unlink(missing_ok=True)
    print("中间片段已清理，配音保留在 videos/.work/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
