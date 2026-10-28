#!/usr/bin/env python3
"""音频预分析: MP3 -> 32 频段频谱 timeline_spec.json（STFT, 对数分频, 低频鼓点检测）
用法: python3 audio_timeline.py in.mp3 out_timeline_spec.json
依赖: numpy, wave, ffmpeg(抽 wav)
输出: {"duration", "fps", "n_bands", "bands_hz", "beats":[秒], "spec":[[...32...],...], "spec_hop_s"}
spec 行索引: t / spec_hop_s 向下取整; fps=2*hop 行距的倒数(约 21.5 行/s, 30fps 渲染按帧查足够)
"""
import json, subprocess, sys, os
import numpy as np, wave

def main():
    src, out = sys.argv[1], sys.argv[2]
    wav = src + ".wav"
    # 22050 mono 抽 wav（STFT 够用，文件小快）
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-ac", "1", "-ar", "22050", wav], check=True)
    w = wave.open(wav, "rb")
    sr = w.getframerate()
    data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    w.close()
    os.remove(wav)

    win, hop, nfft = 1024, 512, 1024
    n_frames = 1 + (len(data) - win) // hop
    spec = np.zeros((n_frames, nfft // 2 + 1))
    for i in range(n_frames):
        seg = data[i*hop:i*hop+win]
        if len(seg) < win:
            seg = np.pad(seg, (0, win - len(seg)))
        seg = seg * np.hanning(win)
        spec[i] = np.abs(np.fft.rfft(seg))**2

    freqs = np.fft.rfftfreq(nfft, 1/sr)
    n_bands = 32
    bands = np.logspace(np.log10(40.0), np.log10(18000.0), n_bands + 1)  # 40Hz~18kHz 对数分段
    band_energy = np.zeros((n_frames, n_bands))
    for b in range(n_bands):
        mask = (freqs >= bands[b]) & (freqs < bands[b+1])
        if mask.sum() > 0:
            band_energy[:, b] = spec[:, mask].mean(axis=1)
    for b in range(n_bands):  # 99 分位归一化防过曝
        q = np.percentile(band_energy[:, b], 99)
        if q > 0:
            band_energy[:, b] = np.clip(band_energy[:, b] / q, 0, 1)

    # 低频(前3段)鼓点检测: 包络峰值 + 200ms 抑制
    low_band = band_energy[:, :3].mean(axis=1)
    frame_t = np.arange(n_frames) * hop / sr
    beats = []
    for i in range(1, len(low_band) - 1):
        if low_band[i] > 0.35 and low_band[i] >= low_band[i-1] and low_band[i] > low_band[i+1]:
            t = float(frame_t[i])
            if not beats or t - beats[-1] > 0.18:
                beats.append(round(t, 2))

    tl = {
        "duration": round(len(data) / sr, 2), "fps": 20, "n_bands": n_bands,
        "bands_hz": [round(float(b), 1) for b in bands],
        "beats": beats,
        "spec": [[round(float(v), 4) for v in row] for row in band_energy[::2]],  # 抽半行距≈43行/s
        "spec_hop_s": round(2 * hop / sr, 4),
    }
    json.dump(tl, open(out, "w"))
    print(f"duration={tl['duration']}s bands={n_bands} spec_rows={len(tl['spec'])} beats={len(beats)}")

if __name__ == "__main__":
    main()
