#!/usr/bin/env python3
"""Extract text from a text-layer PDF using ONLY Python stdlib.

Fallback for offline/blocked-PyPI boxes where pymupdf/pdfplumber/poppler
cannot be installed. Handles ReportLab-style PDFs (common for Chinese docs):
ASCII85+Flate double-encoded streams, TrueType-subset fonts with a /ToUnicode
CMap stream, octal-escape text strings, and '\\ ' encoded spaces.

Usage: python3 pdf_text_stdlib.py <file.pdf>
"""
import sys, re, zlib, base64


def dec_stream(body):
    """Extract a stream payload by its /Length and reverse its /Filter chain."""
    m = re.search(rb'stream\r?\n', body)
    if not m:
        return b''
    start = m.end()
    lm = re.search(rb'/Length (\d+)', body[:start])
    raw = body[start:start + int(lm.group(1))] if lm else body[start:body.rfind(b'endstream')]
    raw = raw.rstrip(b'\r\n')
    try:
        if b'/ASCII85Decode' in body:
            r = raw[:-2] if raw.endswith(b'~>') else raw
            raw = base64.a85decode(r)
        return zlib.decompress(raw)
    except Exception:
        try:
            return zlib.decompress(raw)
        except Exception:
            return raw


def parse_cmap(cm):
    """Parse a decompressed ToUnicode CMap into {charcode:int -> utf16be bytes}."""
    d = {}
    for bf in re.finditer(rb'<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{4,8})>', cm):
        d[int(bf.group(1), 16)] = bytes.fromhex(bf.group(2).decode('ascii'))
    for br in re.finditer(rb'<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{4,8})>', cm):
        lo, hi, base = int(br.group(1), 16), int(br.group(2), 16), int(br.group(3), 16)
        for c in range(lo, hi + 1):
            d[c] = (base + (c - lo)).to_bytes(2, 'big')
    return d


def decode_str(s):
    """Resolve PDF literal-string escapes (octal \\ooo, \\  = space, etc.) to bytes."""
    out, i = [], 0
    while i < len(s):
        b = s[i]
        if b == 0x5c and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == 0x5c and i + 2 < len(s) and s[i + 2] == 0x20:  # ReportLab space
                out.append(0x20); i += 3
            elif nxt in b'01234567':
                j, val = i + 1, 0
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
    return ''.join((cmap.get(c).decode('utf-16-be', 'replace') if cmap.get(c) else '?') for c in cids)


def extract(path):
    data = open(path, 'rb').read()
    starts = [m.start() for m in re.finditer(rb'\d+ 0 obj', data)]
    objs = {}
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(data)
        num = int(re.search(rb'(\d+) 0 obj', data[s:s + 20]).group(1))
        objs[num] = data[s:e]

    # resource name (/F2+0) -> /BaseFont name (AAAAAA+X-0) via the Resources dict
    name_map = {}
    for body in objs.values():
        if b'/F1 ' in body or (b'/Font' in body and b'/Type /Page' in objs and False):
            pass
    for body in objs.values():
        for res in re.finditer(rb'/([A-Za-z0-9+]+) (\d+) 0 R', body):
            rname, ono = res.group(1).decode('latin1'), int(res.group(2))
            if ono in objs:
                bf = re.search(rb'/BaseFont /(\S+)', objs[ono])
                if bf:
                    name_map[rname] = bf.group(1).decode('latin1')

    # per-font ToUnicode CMap
    cmaps = {}
    for body in objs.values():
        fm = re.search(rb'/BaseFont /(\S+) .*?/ToUnicode (\d+) 0 R', body, re.DOTALL)
        if fm:
            cmaps[fm.group(1).decode('latin1')] = parse_cmap(dec_stream(objs[int(fm.group(2))]))

    pat = re.compile(rb'/([A-Za-z0-9+]+)\s+[\d.]+\s+Tf|\(((?:[^()\\]|\\.)*)\)\s*Tj|\[((?:[^\[\]\\]|\\.)*)\]\s*TJ')
    for num in sorted(objs):
        body = objs[num]
        if b'/MediaBox' in body and b'/Contents' in body:
            ref = re.search(rb'/Contents (\d+) 0 R', body)
            if not ref:
                continue
            c = dec_stream(objs[int(ref.group(1))])
            print(f'=== page (obj {num}) ===')
            cur = None
            for mm in pat.finditer(c):
                if mm.group(1) is not None:
                    cur = mm.group(1).decode('latin1')
                elif mm.group(2) is not None:
                    print(render(decode_str(mm.group(2)), cmaps.get(name_map.get(cur, ''), {})))
                elif mm.group(3) is not None:
                    cm = cmaps.get(name_map.get(cur, ''), {})
                    for st in re.findall(rb'\(((?:[^()\\]|\\.)*)\)', mm.group(3)):
                        print(render(decode_str(st), cm))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python3 pdf_text_stdlib.py <file.pdf>', file=sys.stderr)
        sys.exit(2)
    extract(sys.argv[1])
