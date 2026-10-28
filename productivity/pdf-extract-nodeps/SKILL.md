---
name: pdf-extract-nodeps
description: Use when 从 PDF 提取文本但无 PDF 库可用（PyPI 受限/离线）。纯 stdlib 提取器。
---

# 零依赖 PDF 文本提取（stdlib only）

## When to Use
- 需要从 PDF 提取文本，但 pymupdf/marker 装不上（PyPI 被墙/超时/离线）或不想装大依赖。
- 首选仍是 ocr-and-documents 的 pymupdf/marker/web_extract（质量更高）；本技能是**无依赖兜底**。
- 实测覆盖：ReportLab 生成的文本型 PDF（含中文 CID/TrueType 子集字体）。

## 用法
```bash
python scripts/pdf_extract_nodeps.py <file.pdf>
# 输出：每页文本行到 stdout
```
文件含 NUL 字节时 stdout 可能被当二进制——重定向到文件后 `re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', txt)` 清理再看。

## 陷阱（每条都是血泪）
1. **按位置切对象，勿按 `endobj` 正则**：二进制流内容里可能碰巧出现 `endobj`/`endstream` 子串，正则切分会把对象截断（rfind 找真正的结尾）。对象边界 = 下一个 `N 0 obj` 的位置。
2. **流按 `/Length N` 精确截取**，不要 find('endstream')——同样防二进制伪标记。
3. **ASCII85 + Flate 双层过滤**：ReportLab 常用 `[ /ASCII85Decode /FlateDecode ]`——先 a85decode（**先剥掉结尾 `~>`**，否则 Non-Ascii85 digit: ~）再 zlib。
4. **Tf 用资源名（/F2+0），ToUnicode CMap 按 /BaseFont 名（AAAAAA+...）**——必须从页面 Resources 字典建 资源名→BaseFont 映射，否则全部字符查不到映射渲染成 '?'。
5. **多字体同名映射覆盖**：两个子集字体可以共用 0-255 字符码空间但映射不同——每个字体独立 cmap，按当前 Tf 切换，不能合并成一个字典。
6. **ReportLab 转义**：空格写成 `\\ `（反斜杠反斜杠空格→空格）、字符码用文本八进制 `\001`（→字节 0x01）；按 PDF 转义规则解析。
7. **ToUnicode 值按 UTF-16BE 解码**（2 字节大端），不是 UTF-8——用 `v.decode('utf-16-be')`。
8. **ToUnicode 流本身也要 dec_stream**（FlateDecode 压缩），在解压后找 bfchar/bfrange，别在未解压字节里搜。

## 结构
- `scripts/pdf_extract_nodeps.py`：完整提取器（对象切分→流解码→CMap 映射→Tf 跟踪→文本输出）

> 注：与 ocr-and-documents（pymupdf/marker 路线）重叠，但它是 user-owned 技能，无法并入；本技能只承载 stdlib 兜底路线。