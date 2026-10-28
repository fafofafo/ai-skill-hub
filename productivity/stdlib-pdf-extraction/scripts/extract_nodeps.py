#!/usr/bin/env python3
"""纯标准库 PDF 文本提取（无 pip 依赖 fallback）。
支持 ReportLab 等生成的文本型 PDF：ASCII85+Flate 双层流、TrueType 子集字体
ToUnicode CMap（按字体分表）、八进制/\\ 空格转义、UTF-16BE 渲染。
用法: python extract_nodeps.py file.pdf [file2.pdf ...]
"""
import re, zlib, base64, argparse


def split_objects(data):
    """按对象头位置切分（勿用 endobj 正则——二进制流内可能碰巧出现 endobj）。"""
    starts = [m.start() for m in re.finditer(rb'\d+ 0 obj', data)]
    objs = {}
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(data)
        num = int(re.search(rb'(\d+) 0 obj', data[s:s + 20]).group(1))
        objs[num] = data[s:e]
    return objs


def dec_stream(body):
    """解压对象里的流：ASCII85(可选) + Flate。按 /Length 精确截取，不搜 endstream。"""
    m = re.search(rb'stream\r?\n', body)
    if not m:
        return b''
    start = m.end()
    lm = re.search(rb'/Length (\d+)', body[:start])
    raw = body[start:start + int(lm.group(1))] if lm else body[start:body.rfind(b'endstream')]
    raw = raw.rstrip(b'\r\n')
    try:
        if b'/ASCII85Decode' in body:
            r = raw[:-2] if raw.endswith(b'~>') else raw  # ~> 尾部标记必须去
            raw = base64.a85decode(r)
        return zlib.decompress(raw)
    except Exception:
        try:
            return zlib.decompress(raw)
        except Exception:
            return raw


def build_cmaps(objs):
    """每个字体的 ToUnicode CMap（字符码 -> UTF-16BE bytes）。必须按字体分表。"""
    cmaps = {}
    for body in objs.values():
        fm = re.search(rb'/BaseFont /(\S+) .*?/ToUnicode (\d+) 0 R', body, re.DOTALL)
        if not fm:
            continue
        fname = fm.group(1).decode('latin1')
        cm = dec_stream(objs[int(fm.group(2))])
        d = {}
        for bf in re.finditer(rb'<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{4,8})>', cm):
            d[int(bf.group(1), 16)] = bytes.fromhex(bf.group(2).decode('ascii'))
        for br in re.finditer(rb'<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{4,8})>', cm):
            lo = int(br.group(1), 16); hi = int(br.group(2), 16); base = int(br.group(3), 16)
            for c in range(lo, hi + 1):
                d[c] = (base + (c - lo)).to_bytes(2, 'big')
        cmaps[fname] = d
    return cmaps


def build_name_map(objs):
    """资源名(如 /F2+0) -> BaseFont 名。从 Resources 字典(/F2+0 9 0 R) + 对应字体对象。"""
    name_map = {}
    for body in objs.values():
        if not (re.search(rb'/F1 \d+ 0 R', body) and b'/F2' in body):
            continue
        for res in re.finditer(rb'/([A-Za-z0-9+]+) (\d+) 0 R', body):
            resname, objno = res.group(1).decode('latin1'), int(res.group(2))
            if objno in objs:
                bf = re.search(rb'/BaseFont /(\S+)', objs[objno])
                if bf:
                    name_map[resname] = bf.group(1).decode('latin1')
        break
    return name_map


def decode_str(s):
    """PDF 字符串转义：\\ooo 八进制、ReportLab 的 '\\ '=空格、标准 \\n/\\t。"""
    out = []
    i = 0
    while i < len(s):
        b = s[i]
        if b == 0x5c and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == 0x5c and i + 2 < len(s) and s[i + 2] == 0x20:
                out.append(0x20); i += 3  # ReportLab 空格编码为 '\\ '
            elif nxt in b'01234567':
                j = i + 1; val = 0
                while j < len(s) and j < i + 4 and s[j] in b'01234567':
                    val = val * 8 + (s[j] - 48); j += 1
                out.append(val); i = j
            elif nxt in b'ntrf\b':
                out.append({ord('n'): 10, ord('t'): 9, ord('r'): 13, ord('f'): 12, ord('\\'): 92}[nxt]); i += 2
            else:
                out.append(nxt); i += 2
        else:
            out.append(b); i += 1
    return out


def render(cids, cmap):
    out = []
    for c in cids:
        v = cmap.get(c)
        out.append(v.decode('utf-16-be', 'replace') if v else '?')  # ToUnicode 是 UTF-16BE
    return ''.join(out)


def extract(path):
    data = open(path, 'rb').read()
    objs = split_objects(data)
    cmaps = build_cmaps(objs)
    name_map = build_name_map(objs)
    pat = re.compile(rb'/([A-Za-z0-9+]+)\s+[\d.]+\s+Tf|\(((?:[^()\\]|\\.)*)\)\s*Tj|\[((?:[^\[\]\\]|\\.)*)\]\s*TJ')
    for num in sorted(objs):
        body = objs[num]
        if b'/MediaBox' not in body or b'/Contents' not in body:
            continue
        ref = re.search(rb'/Contents (\d+) 0 R', body)
        if not ref:
            continue
        c = dec_stream(objs[int(ref.group(1))])
        cur_font = None
        for mm in pat.finditer(c):
            if mm.group(1) is not None:
                cur_font = mm.group(1).decode('latin1')
            elif mm.group(2) is not None:
                cmap = cmaps.get(name_map.get(cur_font, ''), {})
                print(render(decode_str(mm.group(2)), cmap))
            elif mm.group(3) is not None:
                cmap = cmaps.get(name_map.get(cur_font, ''), {})
                for st in re.findall(rb'\(((?:[^()\\]|\\.)*)\)', mm.group(3)):
                    print(render(decode_str(st), cmap))


def main():
    ap = argparse.ArgumentParser(description='纯标准库 PDF 文本提取（无依赖）')
    ap.add_argument('files', nargs='+', help='PDF 文件路径')
    a = ap.parse_args()
    for f in a.files:
        print(f'=== {f} ===')
        extract(f)


if __name__ == '__main__':
    main()
