#!/usr/bin/env python3
"""生成歌词 ASS 字幕（逐行浮现 fad，竖版）——配合 image-slideshow-video 使用
用法: gen_lyrics_ass.py 歌词.txt --total 298 --start 8 --out /tmp/lyrics.ass
      歌词文件每行一句；--total=视频/音乐总时长(秒)；--start=前奏后开始(秒)
"""
import argparse

def ts(sec):
    h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lyrics", help="歌词文件，每行一句")
    ap.add_argument("--total", type=float, required=True, help="视频/音乐总时长(秒)")
    ap.add_argument("--start", type=float, default=8.0, help="前奏后开始(秒)")
    ap.add_argument("--out", default="/tmp/lyrics.ass")
    ap.add_argument("--width", type=int, default=880)
    ap.add_argument("--height", type=int, default=1184)
    ap.add_argument("--fontsize", type=int, default=42)
    ap.add_argument("--fad", type=int, default=600)
    a = ap.parse_args()

    lines = [l.strip() for l in open(a.lyrics, encoding="utf-8") if l.strip()]
    if not lines:
        raise SystemExit("歌词文件为空")
    step = (a.total - a.start) / len(lines)
    header = f"""[Script Info]
Title: lyrics
ScriptType: v4.00+
PlayResX: {a.width}
PlayResY: {a.height}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei,{a.fontsize},&H00FFFFFF,&H000000FF,&H00101010,&H80000000,0,0,0,0,100,100,0,0,1,2.5,1,2,40,40,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for i, txt in enumerate(lines):
        s = a.start + i * step
        events.append(f"Dialogue: 0,{ts(s)},{ts(s+step)},Default,,0,0,0,,{{\\fad({a.fad},{a.fad})}}{txt}")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"OK {a.out}: {len(lines)} 行, 起始 {ts(a.start)}, 每行 {step:.1f}s")

if __name__ == "__main__":
    main()
