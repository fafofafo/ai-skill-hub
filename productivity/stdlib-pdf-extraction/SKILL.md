---
name: stdlib-pdf-extraction
description: Use when 提取 PDF 文本但 pymupdf/pdftotext 装不上或离线。纯标准库。
---

# 纯标准库 PDF 文本提取（无依赖 fallback）

## 何时用
- pymupdf/marker-pdf 装不上（PyPI 超时/被墙）、`pdftotext`/`gs` 不存在，却要读 PDF 文本。
- 典型场景：ReportLab/导出工具生成的**文本型 PDF**（最常见，含中文/数字/符号）。
- 扫描件（纯图片 PDF）此路不通 → 走 `pdftoppm`+vision 或 marker-pdf。

## 用法
```bash
python scripts/extract_nodeps.py document.pdf [more.pdf ...]
```
只依赖 stdlib（zlib/base64/re）。输出每页文本到 stdout。

## 核心技术点（三页 ReportLab PDF 实测验证）

1. **对象按位置切分，勿用 `endobj` 正则**：二进制流内容里可能碰巧出现 `endobj`/`endstream` 字样（ASCII85 编码含小写字母），非贪婪 `(.*?)endobj` 会提前截断 body。用 `re.finditer(rb'\d+ 0 obj', data)` 的位置切段。
2. **流按 `/Length N` 精确截取**：找到 `stream\r?\n` 后读 N 字节（N 在对象字典里），别搜 `endstream` 定位（同样会被二进制内容干扰）。
3. **ASCII85 + Flate 双层解码**：`/Filter [ /ASCII85Decode /FlateDecode ]` → 先 `raw[:-2] if raw.endswith(b'~>')` 去尾部标记，`base64.a85decode()`，再 `zlib.decompress()`。
4. **TrueType 子集字体的字符码映射**：子集字体（`/BaseFont /AAAAAA+WenQuanYiZenHei-0`）用**自定义字符码 0-255**，每个字体一个 `/ToUnicode N 0 R` CMap（`bfchar <src> <dst>` + `bfrange <lo> <hi> <base>`）。**必须按字体分别存映射**：多个子集字体字符码区间重叠（F2+0 与 F2+1 的 0x01 不同字），只用最后一个 CMap 会全部乱码。
5. **Tf 资源名 → BaseFont 名映射**：内容流里 `/F2+0 18 Tf` 用的是资源名；从页面 Resources 字典（`/F2+0 9 0 R` → obj9 的 `/BaseFont`）建 name_map，否则查不到 CMap。
6. **PDF 字符串转义**：`\ooo` 八进制 → 单字节（`\001` = 0x01）；**ReportLab 把空格编码为 `\\ `（反斜杠反斜杠空格）** → 必须解为空格，否则标题带反斜杠；标准 `\n`/`\t` 等照常。
7. **ToUnicode 值是 UTF-16BE**（2 字节），`v.decode('utf-16-be')`——不是 UTF-8。ASCII 字符也是 `\x00H` 两字节。

## 诊断顺序（乱码/空输出时）
1. `cmap: 0` → ToUnicode 没解出来：检查 dec_stream 是否真的解压成功（ASCII85 的 `~>` 没去会报 Non-Ascii85 digit）。
2. 全文 `?` → 要么字符码没进 CMap（字体映射错：name_map 没建/字符码区间重叠被覆盖），要么渲染时用了 UTF-8 解 UTF-16BE。
3. 中文正常但夹杂反斜杠 → `\\ ` 空格转义没处理。
4. 对象被截断（内容流长度 < /Length）→ 对象切分用了 endobj 正则，改位置切分。

## 边界
- 仅文本层；复杂排版/表格/公式不做（那是 pymupdf/marker 的活）。
- 标准工具可用时优先 pymupdf（见 ocr-and-documents）；本技能只在无依赖时兜底。
