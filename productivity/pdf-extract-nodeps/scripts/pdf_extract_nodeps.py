#!/usr/bin/env python3
"""Zero-dependency PDF text extractor (stdlib: zlib, re, base64, sys). Handles
ReportLab text PDFs: ASCII85+Flate filters, TrueType subset fonts + ToUnicode
CMap (1-byte codes), multi-font char-code sharing, octal escapes, UTF-16BE.
USAGE: python pdf_extract_nodeps.py <file.pdf>
"""
import sys, zlib, re, base64


def extract(path):
    data = open(path, 'rb').read()
    starts = [m.start() for m in re.finditer(rb'\d+ 0 obj', data)]
    if not starts:
        raise ValueError('No PDF objects found')
    objs = {}
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(data)
        num = int(re.search(rb'(\d+) 0 obj', data[s:s + 20]).group(1))
        objs[num] = data[s:e]

    def dec_stream(body):
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

    name_map = {}
    for num, body in objs.items():
        if re.search(rb'/F1 \d+ 0 R', body) and re.search(rb'/F\d+\+\d+', body):
            for res in re.finditer(rb'/([A-Za-z0-9+]+) (\d+) 0 R', body):
                rname, objno = res.group(1).decode('latin1'), int(res.group(2))
                if objno in objs:
                    bf = re.search(rb'/BaseFont /(\S+)', objs[objno])
                    if bf:
                        name_map[rname] = bf.group(1).decode('latin1')
            break

    cmaps = {}
    for num, body in objs.items():
        fm = re.search(rb'/BaseFont /(\S+) .*?/ToUnicode (\d+) 0 R', body, re.DOTALL)
        if not fm:
            continue
        fname = fm.group(1).decode('latin1')
        cm = dec_stream(objs[int(fm.group(2))])
        d = {}
        for bf in re.finditer(rb'<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{4,8})>', cm):
            d[int(bf.group(1), 16)] = bytes.fromhex(bf.group(2).decode('ascii'))
        for br in re.finditer(rb'<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{2})>\s*<([0-9A-Fa-f]{4,8})>', cm):
            lo, hi, base = int(br.group(1), 16), int(br.group(2), 16), int(br.group(3), 16)
            for c in range(lo, hi + 1):
                d[c] = (base + (c - lo)).to_bytes(2, 'big')
        cmaps[fname] = d

    def decode_str(s):
        out, i = [], 0
        while i < len(s):
            b = s[i]
            if b == 0x5c and i + 1 < len(s):
                nxt = s[i + 1]
                if nxt == 0x5c and i + 2 < len(s) and s[i + 2] == 0x20:
                    out.append(0x20); i += 3  # ReportLab escaped space "\\ "
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
        out = []
        for c in cids:
            v = cmap.get(c)
            out.append(v.decode('utf-16-be', 'replace') if v else '?')
        return ''.join(out)

    pat = re.compile(rb'/([A-Za-z0-9+]+)\s+[\d.]+\s+Tf|\(((?:[^()\\]|\\.)*)\)\s*Tj|\[((?:[^\[\]\\]|\\.)*)\]\s*TJ')
    for num in sorted(objs):
        body = objs[num]
        if b'/MediaBox' in body and b'/Contents' in body:
            ref = re.search(rb'/Contents (\d+) 0 R', body)
            if not ref:
                continue
            c = dec_stream(objs[int(ref.group(1))])
            print(f'=== 页 (obj{num}) ===')
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python pdf_extract_nodeps.py <file.pdf>', file=sys.stderr)
        sys.exit(2)
    extract(sys.argv[1])
