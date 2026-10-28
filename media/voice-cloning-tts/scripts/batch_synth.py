#!/usr/bin/env python3
"""批量合成长文案为配音（硅基流动 CosyVoice2 固定音色）。

用法:
  python3 batch_synth.py chunks.json <uri> out.mp3 [workers]

chunks.json: ["文本块1", "文本块2", ...]（每块 ≤300 字，无空格，由调用方预处理）
uri: 固定音色 uri（如 speech:<your-voice-uri>:...），查 ~/项目目录/音色库.md
输出: out.mp3（ffmpeg concat 拼接）

动态克隆（无固定音色）不走此脚本：直接在合成请求里带 references。
"""
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

import yaml

MODEL = "FunAudioLLM/CosyVoice2-0.5B"
URL = "https://api.siliconflow.cn/v1/audio/speech"


def load_key() -> str:
    cfg = yaml.safe_load(open(os.path.expanduser("~/.hermes/config.yaml")))
    return cfg["auxiliary"]["vision"]["api_key"]


def synth(idx: int, text: str, uri: str, key: str, tmp: str):
    payload = {"model": MODEL, "voice": uri, "input": text, "response_format": "mp3"}
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
                out = os.path.join(tmp, f"chunk_{idx:02d}.mp3")
                open(out, "wb").write(data)
                return idx, len(data), None
        except Exception as e:
            if attempt == 2:
                return idx, 0, repr(e)
    return idx, 0, "unknown error"


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    chunks_file, uri, out_file = sys.argv[1], sys.argv[2], sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    key = load_key()
    chunks = json.load(open(chunks_file))
    if not isinstance(chunks, list):
        sys.exit("chunks.json 需为字符串数组")
    tmp = tempfile.mkdtemp(prefix="synth_")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(synth, i + 1, c, uri, key, tmp) for i, c in enumerate(chunks)]
        for f in concurrent.futures.as_completed(futs):
            results.append(f.result())
    results.sort()
    fails = [i for i, _, e in results if e]
    if fails:
        print("失败块:", fails)
        sys.exit(1)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for i, _, _ in results:
            f.write(f"file '{os.path.join(tmp, f'chunk_{i:02d}.mp3')}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out_file],
        check=True,
    )
    print(f"完成: {out_file} ({len(chunks)} chunks)")


if __name__ == "__main__":
    main()
