#!/usr/bin/env python3
"""官方歌词 + whisper 时间轴 → 精确 ASS 字幕 (mv1 流程第3步)
用法: 1) 编辑 mapping 列表(官方歌词行→转录段索引范围) 2) 运行
参考: 伍思凯《特别的爱给特别的你》实测映射 (33条)
时间轴来自 ts.json (whisper 转录, 只取时间); 文本用官方简体歌词
"""
import json, re

TS = "/tmp/mv_job/ts.json"        # whisper 转录 (时间轴)
OUT = "/tmp/mv_job/subs_official.ass"

# 官方歌词行 → 转录段索引范围 (每句: (文本, start_idx, end_idx))
mapping = [
    # 示例结构 (改歌时按实际段落重写此表)
    ("没有承诺 却被你抓得更紧", 0, 0),
    ("没有了你 我的世界雨下个不停", 1, 1),
    ("我付出一生的时间 想要忘记你", 2, 2),
    ("但是回忆 回忆 回忆 从我心里跳出来拥抱你", 3, 3),
    ("特别的爱 给特别的你", 4, 4),
    ("我的寂寞 逃不过你的眼睛", 5, 5),
    ("特别的爱 给特别的你", 6, 6),
    ("你让我越来越不相信自己", 7, 7),
    ("没有承诺 却被你抓得更紧", 8, 8),
    ("没有了你 我的世界雨下个不停", 9, 9),
    ("我付出一生的时间 想要忘记你", 10, 10),
    ("但是回忆 回忆 回忆 从我心里跳出来拥抱你", 11, 11),
    ("特别的爱 给特别的你", 12, 12),
    ("我的寂寞 逃不过你的眼睛", 13, 13),
    ("特别的爱 给特别的你", 14, 14),
    ("你让我越来越不相信自己", 15, 15),
    ("特别的爱 给特别的你", 16, 16),
    ("我的寂寞 逃不过你的眼睛", 17, 17),
    ("特别的爱 给特别的你", 18, 18),
    ("你让我越来越不相信自己", 19, 19),
    ("特别的爱 给特别的你", 20, 20),
    ("我还听见 你的声音 轻轻萦绕着我的心", 21, 22),
    ("我还不能 接受分离 就是永远不在一起", 23, 24),
    ("特别的爱 给特别的你", 25, 25),
    ("我的寂寞 逃不过你的眼睛", 26, 26),
    ("特别的爱 给特别的你", 27, 27),
    ("你让我越来越不相信自己", 28, 28),
    ("特别的爱 给特别的你", 29, 29),
    ("我的寂寞 逃不过你的眼睛", 30, 30),
    ("特别的爱 给特别的你", 31, 31),
    ("你让我越来越不相信自己", 32, 32),
    ("我还听见 你的声音 轻轻萦绕着我的心", 33, 34),
    ("我还不能 接受分离 就是永远不能在一起", 35, 36),
]

FONTSIZE = 60   # 用户拍板

segs = json.load(open(TS))["segments"]

def tsf(sec):
    m = int(sec // 60); s = sec % 60
    return f"0:{m:02d}:{s:05.2f}"

header = f"""[Script Info]
Title: 歌词字幕
ScriptType: v4.00+
PlayResX: 880
PlayResY: 1184
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,WenQuanYi Zen Hei,{FONTSIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H8C000000,-1,0,0,0,100,100,0,0,1,4,1.5,2,40,40,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
events = []
for text, s0, s1 in mapping:
    st = segs[s0]["s"]; en = segs[s1]["e"]
    events.append(f"Dialogue: 0,{tsf(st)},{tsf(en)},Default,,0,0,0,,{{\\fad(150,250)\\bord4\\blur0.6}}{text}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(header + "\n".join(events) + "\n")
print(f"[official-ass] 生成 {len(events)} 条官方歌词字幕 → {OUT}")
