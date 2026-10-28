#!/usr/bin/env python3
"""出图后视觉复核（pic 家族通用）。

用法:
    python3 scripts/vision_check.py --image /tmp/x.png --question "简述：1)主体 2)色调 3)左上主标题逐字读 4)右上+底部署名 5)乱码"
    python3 scripts/vision_check.py --image a.png --images b.png --question "..." --out /tmp/check.txt

为什么用这个脚本：内置 vision_analyze 的后端模型未必支持视觉请求；硅基流动 Qwen3-VL 实测稳定。
输出默认同时打印并落文件——长回答会把 process log 尾部截断，落文件后 read_file 更可靠。
"""
import argparse, base64, io, json, os, sys, time, urllib.request

ENV_CANDIDATES = [
    os.path.expanduser('~/.hermes/agent-memory-data/backup.env'),
    os.path.expanduser('~/backup.env'),
]
API = 'https://api.siliconflow.cn/v1/chat/completions'
MODEL = 'Qwen/Qwen3-VL-32B-Instruct'


def api_key():
    for path in ENV_CANDIDATES:
        if not os.path.exists(path):
            continue
        for line in open(path, encoding='utf-8'):
            if line.startswith('SILICONFLOW_API_KEY='):
                return line.split('=', 1)[1].strip()
    sys.exit('SILICONFLOW_API_KEY 未找到（检查 backup.env）')


def encode(path, max_width):
    from PIL import Image
    im = Image.open(path)
    dims = f'{im.width}x{im.height}'
    # 宽 <=640 才稳；720/800 实测 read timeout
    if im.width > max_width:
        im = im.resize((max_width, int(im.height * max_width / im.width)))
    buf = io.BytesIO()
    im.convert('RGB').save(buf, format='JPEG', quality=80)
    return dims, base64.b64encode(buf.getvalue()).decode()


def ask(key, b64, question, retries=3, timeout=240):
    payload = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': [
            {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{b64}'}},
            {'type': 'text', 'text': question},
        ]}],
        'max_tokens': 500,
    }
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                API, method='POST',
                headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {key}'},
                data=json.dumps(payload).encode())
            resp = json.load(urllib.request.urlopen(req, timeout=timeout))
            return resp['choices'][0]['message']['content']
        except Exception as exc:  # 瞬时 500/timeout 直接重试即可
            last = exc
            time.sleep(8)
    return f'复核失败: {type(last).__name__}: {last}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', action='append', required=True)
    ap.add_argument('--question', required=True)
    ap.add_argument('--out', default=None)
    ap.add_argument('--max-width', type=int, default=640)
    args = ap.parse_args()

    key = api_key()
    chunks = []
    for path in args.image:
        dims, b64 = encode(path, args.max_width)
        answer = ask(key, b64, args.question)
        chunks.append(f'=== {path} ({dims}) ===\n{answer}\n')
    text = '\n'.join(chunks)
    print(text)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print(f'[saved] {args.out}')


if __name__ == '__main__':
    main()
