#!/usr/bin/env python3
"""图片+背景乐+歌词字幕 一键视频生成器
用法:
  python3 make_music_video.py transcribe --audio in.mp3 --out ts.json
       # faster-whisper 词级时间戳（首次会下载/加载模型，模型已缓存）
  python3 make_music_video.py ass --ts ts.json --lyrics lyrics.txt --out subs.ass
       # 歌词(每行一条) → ASS 底部样式，字幕起止=语音起止
  python3 make_music_video.py render --images a.png,b.png,c.png --ass subs.ass \
       --audio in.mp3 --out out.mp4 [--w 880 --h 1184] [--crf 28]
"""
import argparse, json, os, sys, time, subprocess, re

WHISPER_MODEL = "small"
HF_ENDPOINT = "https://hf-mirror.com"
DOWNLOAD_ROOT = os.path.expanduser("~/models/whisper")

def transcribe(audio, out):
    os.environ["HF_ENDPOINT"] = HF_ENDPOINT
    from faster_whisper import WhisperModel
    print(f"[transcribe] 加载模型 {WHISPER_MODEL}...", flush=True)
    t0 = time.time()
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8",
                         download_root=DOWNLOAD_ROOT)
    print(f"[transcribe] 模型就绪 {time.time()-t0:.0f}s，转写 {audio}...", flush=True)
    t0 = time.time()
    segs, info = model.transcribe(audio, language="zh", word_timestamps=True,
                                  vad_filter=False)
    result = []
    for seg in segs:
        words = [{"w": w.word, "s": round(w.start, 2), "e": round(w.end, 2)}
                 for w in (seg.words or [])]
        result.append({"s": round(seg.start, 2), "e": round(seg.end, 2),
                       "text": seg.text, "words": words})
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"segments": result}, f, ensure_ascii=False, indent=1)
    print(f"[transcribe] 完成 {len(result)} 段，{time.time()-t0:.0f}s → {out}")
    for s in result[:5]:
        print(f"   [{s['s']:.1f}-{s['e']:.1f}] {s['text']}")

def ass(ts, lyrics, out):
    """歌词行(每行一条) → ASS。语音起止取 whisper 段；歌词行按序对应语音段。
    若行数与段数不等，按累计语音时长把段合并/拆分到 行数 份。"""
    data = json.load(open(ts, encoding="utf-8"))
    segs = data["segments"]
    lines = [l.rstrip() for l in open(lyrics, encoding="utf-8")
             if l.strip()]
    n = len(lines)
    if n == len(segs):
        pairs = list(zip(lines, segs))
    else:
        # 按语音累计时长把 segments 聚成 n 组（尽量在段边界断）
        total = sum(s["e"] - s["s"] for s in segs)
        per = total / n
        pairs, acc, idx = [], 0.0, 0
        for s in segs:
            span = s["e"] - s["s"]
            if acc + span <= per * (idx + 1) + 0.5:
                pairs.append((lines[min(idx, n-1)], s))
                acc += span
            else:
                idx += 1
                pairs.append((lines[min(idx, n-1)], s))
                acc = span
    def tsf(sec):
        m = int(sec // 60); s = sec % 60
        return f"0:{m:02d}:{s:05.2f}"
    header = """[Script Info]
Title: 歌词字幕
ScriptType: v4.00+
PlayResX: 880
PlayResY: 1184
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,WenQuanYi Zen Hei,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H8C000000,-1,0,0,0,100,100,0,0,1,4,1.5,2,40,40,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # 炫酷抖动：金色主字 + 霓虹描边发光 + 弹出震动（fscx/fscy 快速挤压交替 = 抖动感）
    ev = [f"Dialogue: 0,{tsf(p[1]['s'])},{tsf(p[1]['e'])},Default,,0,0,0,,{{\\fad(150,250)\\bord2.5\\blur0.6\\fscx100\\fscy100\\t(0,90,\\fscx112\\fscy90)\\t(90,180,\\fscx92\\fscy108)\\t(180,270,\\fscx108\\fscy94)\\t(270,360,\\fscx100\\fscy100)}}{p[0]}"
          for p in pairs]
    with open(out, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(ev) + "\n")
    print(f"[ass] 生成 {len(pairs)} 条字幕 → {out}")
    for (t, s), p in zip(pairs[:5], pairs[:5]):
        print(f"   {tsf(p[1]['s'])}-{tsf(p[1]['e'])} {t[:22]}")

def render(images, assf, audio, out, w, h, crf, still=False):
    imgs = [os.path.expanduser(i.strip()) for i in images.split(",") if i.strip()]
    n = len(imgs)
    if n < 2:
        print("[render] 至少 2 张图"); sys.exit(1)
    # 音乐时长
    probe = subprocess.run(["ffprobe", "-v", "quiet", "-show_format", audio],
        capture_output=True, text=True).stdout
    total = 30.0
    for line in probe.splitlines():
        if line.startswith("duration="):
            total = float(line.split("=")[1]); break
    per = total / n
    d = int(per * 25)  # 25fps 帧数/张
    fc = []
    if still:
        # 静态模式：无运镜，图片原样展示（scale 到统一尺寸）
        for i in range(n):
            fc.append(f"[{i}:v]scale={w}:{h}:flags=bicubic,setsar=1[v{i}]")
    else:
        # 去抖动 Ken Burns：输入先放大 2x（zoompan 取整误差相对小）+ 线性缓慢推近（无 sin 回摆）
        # 每张错相位改为不同起始缩放，保证各段有变化但都匀速稳定
        starts = [1.0, 1.06, 1.0, 1.06, 1.0, 1.06, 1.02, 1.04][:n]
        for i in range(n):
            z0 = starts[i]
            # z: 从 z0 线性到 z0+0.10（全程匀速，无速度突变→无抖动）
            zexp = f"min({z0}+on*{0.10/d:.8f},{z0+0.10})"
            fc.append(f"[{i}:v]scale=iw*2:ih*2:flags=bicubic,"
                      f"zoompan=z='{zexp}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                      f":d={d}:s={w}x{h}:fps=25,setsar=1[v{i}]")
    fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vcat]")
    fc.append(f"[vcat]ass={assf}[vout]")
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for im in imgs:
        if still:
            cmd += ["-loop", "1", "-t", f"{per}", "-i", im]
        else:
            cmd += ["-i", im]
    cmd += ["-i", audio,
            "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", f"{n}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-shortest", "-movflags", "+faststart", out]
    print(f"[render] {n} 图 × {per:.1f}s = {total:.0f}s 视频 → {out}")
    subprocess.run(cmd, check=True)
    print(f"[render] 完成 → {out}")

def viz_analyze(audio, out):
    """音频 → 32频段频谱JSON(40Hz~18kHz对数分段+低频节拍)。
    输出: {duration, fps:20, n_bands:32, bands_hz, beats, spec[帧][32], spec_hop_s}
    供 viz_render 的 p5.js 模板驱动频谱柱/脉冲环。依赖 numpy。"""
    import numpy as np, wave
    # 统一转 22.05kHz 单声道 wav(临时)
    tmp = out + ".tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", audio, "-ac", "1", "-ar", "22050", tmp], check=True)
    try:
        w = wave.open(tmp, "rb"); sr = w.getframerate(); n = w.getnframes()
        raw = w.readframes(n); w.close()
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        win, hop, nfft = 1024, 512, 1024
        n_frames = 1 + (len(data) - win) // hop
        spec_all = np.zeros((n_frames, nfft//2 + 1))
        for i in range(n_frames):
            seg = data[i*hop:i*hop+win]
            if len(seg) < win: seg = np.pad(seg, (0, win-len(seg)))
            seg = seg * np.hanning(win)
            spec_all[i] = np.abs(np.fft.rfft(seg)) ** 2
        freqs = np.fft.rfftfreq(nfft, 1/sr)
        n_bands = 32
        bands = np.logspace(np.log10(40.0), np.log10(18000.0), n_bands+1)
        band_energy = np.zeros((n_frames, n_bands))
        for b in range(n_bands):
            mask = (freqs >= bands[b]) & (freqs < bands[b+1])
            if mask.sum() > 0: band_energy[:, b] = spec_all[:, mask].mean(axis=1)
        for b in range(n_bands):
            q = np.percentile(band_energy[:, b], 99)
            if q > 0: band_energy[:, b] = np.clip(band_energy[:, b]/q, 0, 1)
        low_band = band_energy[:, :3].mean(axis=1)
        frame_t = np.arange(n_frames)*hop/sr
        beats = []
        for i in range(1, len(low_band)-1):
            if low_band[i] > 0.35 and low_band[i] >= low_band[i-1] and low_band[i] > low_band[i+1]:
                t = frame_t[i]
                if not beats or t - beats[-1] > 0.18: beats.append(round(float(t), 2))
        tl = {"duration": round(n/sr, 2), "fps": 20, "n_bands": n_bands,
              "bands_hz": [round(float(b), 1) for b in bands], "beats": beats,
              "spec": [[round(float(v), 4) for v in row] for row in band_energy[::2]],
              "spec_hop_s": round(2*hop/sr, 4)}
        with open(out, "w", encoding="utf-8") as f: json.dump(tl, f)
        print(f"[viz-analyze] {n/sr:.1f}s → 32频段×{len(tl['spec'])}帧, {len(beats)}拍 → {out}")
    finally:
        if os.path.exists(tmp): os.remove(tmp)

def viz_render(images, audio, tl, out, w=880, h=1184, crf=23, cfg="", fps=30, fmt="png"):
    """图片+频谱 → headless p5.js 渲染 → ffmpeg 合成。
    流程: 模板+注入TL → render_mv.js逐帧 → ffmpeg帧序列+音频合成。
    cfg: 'k=v,k=v' 覆盖模板参数(如 BAR_COUNT=60,BAR_W=10,SUB_R=255)
    fmt: png(清晰) / jpeg(长视频省磁盘)"""
    import json as _json, shutil
    HERE = os.path.dirname(os.path.abspath(__file__))
    workdir = os.path.dirname(os.path.abspath(out)) or "."
    os.makedirs(workdir, exist_ok=True)
    imgs = [os.path.expanduser(i.strip()) for i in images.split(",") if i.strip()]
    if len(imgs) < 1: print("[viz-render] 至少 1 张图"); sys.exit(1)
    # 图片复制到工作目录(相对路径加载)
    img_names = []
    for i, p in enumerate(imgs):
        dst = os.path.join(workdir, f"_viz_img_{i}.png")
        if os.path.abspath(p) != os.path.abspath(dst):
            shutil.copy(p, dst)
        img_names.append(os.path.basename(dst))
    # 1. 生成 sketch: TL + IMGS + CFG 全部内联(不用运行时注入, reload会丢 window 变量)
    tpl = open(os.path.join(HERE, "sketch_viz_template.html"), encoding="utf-8").read()
    tl_data = _json.load(open(tl, encoding="utf-8")) if isinstance(tl, str) else tl
    sketch = tpl.replace("const TL = window.__TL;", "const TL = " + _json.dumps(tl_data) + ";")
    # 内联 IMGS(替换模板的动态读取行)
    sketch = re.sub(r"const IMGS = [^\n]+;", "const IMGS = " + _json.dumps(img_names) + ";", sketch, count=1)
    # 内联 SWITCH_T: cfg 覆盖 > 歌长/图片数
    cfg_pairs = {}
    for kv in cfg.split(","):
        if "=" in kv:
            k, v = kv.split("=", 1)
            cfg_pairs[k.strip()] = float(v) if v.replace(".", "").isdigit() else v.strip()
    sw = cfg_pairs.get("SWITCH_T", tl_data["duration"] / len(img_names))
    sketch = re.sub(r"const SWITCH_T = [^\n]+;", f"const SWITCH_T = {sw};", sketch, count=1)
    # 内联 __C: 去掉 window.__CFG 合并(值已在下面直接替换)
    sketch = sketch.replace(", window.__CFG || {});", ");")
    for k, v in cfg_pairs.items():
        if k == "SWITCH_T": continue
        val = json.dumps(v) if isinstance(v, str) else str(v)
        sketch = re.sub(rf"({k}: )[^,]+", r"\g<1>" + val, sketch)
    sketch_path = os.path.join(workdir, "_viz_sketch.html")
    open(sketch_path, "w", encoding="utf-8").write(sketch)
    # 2. 复制依赖到工作目录(p5.min.js)
    for dep in ("p5.min.js",):
        dst = os.path.join(workdir, dep)
        if not os.path.exists(dst): shutil.copy(os.path.join(HERE, dep), dst)
    # 3. headless 渲染帧
    frames_dir = os.path.join(workdir, "_viz_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)
    # 音频时长 → 帧数
    probe = subprocess.run(["ffprobe", "-v", "quiet", "-show_format", audio], capture_output=True, text=True).stdout
    dur = 30.0
    for line in probe.splitlines():
        if line.startswith("duration="): dur = float(line.split("=")[1]); break
    nframes = int(round(dur * fps))
    node = "node"
    cmd = [node, os.path.join(HERE, "render_mv.js"), sketch_path,
           "--frames", str(nframes), "--output", frames_dir,
           "--width", str(w), "--height", str(h),
           "--format", fmt]
    print(f"[viz-render] 渲染 {nframes} 帧({dur:.1f}s@{fps}fps, {fmt})…")
    subprocess.run(cmd, check=True)
    # 4. ffmpeg 合成
    out_v = out if out.endswith(".mp4") else out + ".mp4"
    ext = "png" if fmt == "png" else "jpeg"
    cmd2 = ["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", f"{frames_dir}/frame-%04d.{ext}",
            "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest",
            "-movflags", "+faststart", out_v]
    subprocess.run(cmd2, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)
    if os.path.exists(sketch_path): os.remove(sketch_path)
    print(f"[viz-render] 完成 → {out_v}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("transcribe"); t.add_argument("--audio"); t.add_argument("--out")
    a = sub.add_parser("ass"); a.add_argument("--ts"); a.add_argument("--lyrics"); a.add_argument("--out")
    r = sub.add_parser("render")
    r.add_argument("--images"); r.add_argument("--ass"); r.add_argument("--audio"); r.add_argument("--out")
    r.add_argument("--w", type=int, default=880); r.add_argument("--h", type=int, default=1184)
    r.add_argument("--crf", type=int, default=28)
    r.add_argument("--still", action="store_true", help="静态模式（无运镜）")
    vz = sub.add_parser("viz-analyze")
    vz.add_argument("--audio"); vz.add_argument("--out")
    vr = sub.add_parser("viz-render")
    vr.add_argument("--images"); vr.add_argument("--audio"); vr.add_argument("--tl"); vr.add_argument("--out")
    vr.add_argument("--w", type=int, default=880); vr.add_argument("--h", type=int, default=1184)
    vr.add_argument("--crf", type=int, default=23)
    vr.add_argument("--fps", type=int, default=30)
    vr.add_argument("--cfg", default="", help="覆盖模板参数 k=v,k=v (BAR_COUNT/BAR_W/SUB_R等)")
    vr.add_argument("--format", default="png", choices=["png", "jpeg"], help="帧格式: png清晰/jpeg小体积(长视频用jpeg)")
    args = p.parse_args()
    if args.cmd == "transcribe": transcribe(args.audio, args.out)
    elif args.cmd == "ass": ass(args.ts, args.lyrics, args.out)
    elif args.cmd == "render": render(args.images, args.ass, args.audio, args.out,
                                      args.w, args.h, args.crf, args.still)
    elif args.cmd == "viz-analyze": viz_analyze(args.audio, args.out)
    elif args.cmd == "viz-render": viz_render(args.images, args.audio, args.tl, args.out,
                                              args.w, args.h, args.crf, args.cfg, args.fps, args.format)
