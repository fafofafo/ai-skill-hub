---
name: pdf-stdlib-extraction
description: Use when 要提取 PDF 文本但 pymupdf/poppler 装不上或断网。纯 Python 标准库解析。
---

# PDF 文本提取（纯 Python 标准库兜底）

## When to Use
- `read_file` 报 .pdf extraction failed / 手头没有 pymupdf、pdfplumber、pdftotext、gs，且 **PyPI/网络装不上包**（离线服务器、PyPI 被墙/超时）。
- 有正常环境时优先用 bundled `ocr-and-documents` / `pdf` 技能（pymupdf 秒出）；**本技能是断网兜底**。

## 第一步：确认真的没库
```
python3 -c "import fitz" 2>/dev/null && echo pymupdf-ok || echo no-pymupdf
which pdftotext qpdf gs   # 有则直接用
```
都没有 → 跑 `scripts/pdf_text_stdlib.py <file.pdf>`（脚本本身零依赖，zlib/base64/re 均标准库）。

## 脚本用法
```
python3 scripts/pdf_text_stdlib.py document.pdf   # 打印各页文本到 stdout
```

## 解析管线（ReportLab 生成的中文 PDF 常见结构）
1. 按 `\d+ 0 obj` 的**起始位置**切对象（见坑 1），每段 = 当前 obj 头到下一个 obj 头。
2. 流 payload 用对象字典里的 `/Length N` **精确切 N 字节**（见坑 2）。
3. 按 `/Filter` 顺序**逆序**解码：`/ASCII85Decode` → 去掉尾部 `~>` → `base64.a85decode` → `zlib.decompress`（见坑 3）。
4. TrueType 子集字体（`/BaseFont /AAAAAA+...`、`/FirstChar 0 /LastChar 255`、`/Subtype /TrueType`）→ 字符串是 **1 字节字符码 0-255**；`/ToUnicode N 0 R` 指向的 CMap 本身是**流**，先解压再解析 `beginbfchar <code2hex> <utf16be4-8hex>` / `beginbfrange`（见坑 4）。
5. 渲染时按 `Tf` 当前**资源名**选对应字体的 CMap（见坑 5、6）。
6. 括号字符串里的 `\ooo` 是**八进制转义**（1-3 位），逐字节解回字符码。

## Pitfalls（每条都是本会话踩过 30+ 分钟换来的）
- **不要用 `re.finditer(rb'(\d+) 0 obj(.*?)endobj')` 切对象**——ASCII85/二进制流里会碰巧出现字面 `endobj`/`endstream`，非贪婪匹配提前截断 body，流变残缺。按 obj 头位置切到下一个 obj 头。
- **流 payload 别用 `rfind(b'endstream')` 定位**——二进制内容可能含 `endstream` 字样。读 `/Length N` 直接切 N 字节（/Length 可能是 `N 0 R` 间接引用时再解引用）。
- **Filter 是链，按逆序解**：`/Filter [ /ASCII85Decode /FlateDecode ]` 要先 a85 再 zlib。ASCII85 结尾 `~>` 必须去掉（`raw[:-2]`），否则 a85decode 报 `Non-Ascii85 digit found: ~`。
- **ToUnicode CMap 是压缩流，先解压再读**——直接在 obj body 里搜 `beginbfchar` 永远搜不到（内容在 FlateDecode 流内）。
- **CMap 目标值是 UTF-16BE**（`<0062>`=技），`.decode('utf-8')` 会出乱码——必须 `bytes.fromhex(...).decode('utf-16-be')`。
- **`Tf` 用资源名（`/F2+0`），`/BaseFont` 是另一串（`AAAAAA+WenQuanYiZenHei-0`）**——从页面 Resources 字典（`/F2+0 9 0 R`）解析资源名→对象号→对象 `/BaseFont`，建 name_map 再渲染。不映射 = 全输出 `?`。
- **多个中文字体共享 0-255 码位但映射不同**——必须跟踪当前字体（遇到 `Tf` 切换），每个 Tj 用当前字体的 CMap，否则后写的 CMap 覆盖先写的，全部乱码。
- **ReportLab 把空格编码成 `\\ `（反斜杠反斜杠空格）**——解析八进制前先特判 `\\ `→空格，否则正文里每个空格前多一个 `\`。
- **调试信号**：全输出 `?` = CMap 没查中（多为 name_map 没建/字体混用）；汉字乱码 = 编解码用错（UTF-8 而非 UTF-16BE）；偶发乱码 = 对象切错/流不完整。先检查这三个，别从头重写。
- 文件名带 URL 编码（`%E6%8A%80...`）时 `read_file` 会报 File not found——用 shell 通配或 `ls` 找真实文件名再传。

## 相关：截断的 store 模式 zip 恢复（同一离线获取场景）

代理/网络中途截断下载（HTTP 200 但每次 size 不同、`zipfile.ZipFile` 报 "not a zip file"、`file` 却说 zip）——`file` 只查头部，central directory（尾部）被切掉时它照样通过。对 **compression method 0（store）** 压缩的 zip 可以手动恢复：扫 `PK\x03\x04` 本地文件头 → 解析 30 字节定长头（method/csize/usize/nlen/elen）→ 内容在 `offset+30+nlen+elen` 起共 csize 字节 → 直接写文件；method 8（deflate）条目用 `zlib.decompress`。**`len(content) != usize` 的条目=条目内被截断，跳过**，绝不写猜测字节。
