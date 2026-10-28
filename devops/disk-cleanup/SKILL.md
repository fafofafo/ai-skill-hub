---
name: disk-cleanup
description: Use when 清点/清理服务器磁盘空间。定位大户、分类清理、防删占用中文件。
---

# Disk Cleanup（服务器磁盘清点与安全清理）

服务器磁盘告警时按此流程。目标：定位大户 → 分类 → 清理 → 复测，**不删占用中/数据类文件**。

## 流程（按序）

1. **清点**：`df -hT /` 看整体（Type=ext4 的根分区是主要目标，tmpfs 无关）；`du -xhd1 /` 逐层定位大户（典型 /home、/tmp、/var）。
2. **逐层下钻**：`du -xhd1 <大目录>` 找真正占空间的子目录（如 ~/.cache/uv 常达 9G）。
3. **分类三档**：
   - **可安全清**（缓存/临时/日志）：`uv cache clean`（大头，uv 包缓存常 9G+）、`pip cache purge`、`npm cache clean --force`、`sudo journalctl --vacuum-size=100M`（journal 需 sudo，非 root 直接跑会 Permission denied）。
   - **占用中不可删**：删任何看似临时的目录前先 `lsof +D <dir>` 查进程——大文件可能被活跃进程 mmap（如 /tmp/venv_shazam 被 BGM 识别进程占用 5.4G），无脑 rm 会破坏运行中的任务。
   - **需用户确认**：备份（.hermes.bak.*、hermes_backups、backups）、模型缓存（HF hub、playwright 旧版本 chromium——删了要重下），属数据类，先问再动。
4. **清理后复测**：`df -hT /` 汇报释放量；逐项确认删了什么、保留了什么及理由（用户偏好先结论后明细）。

## Pitfalls

- **删除前必须查占用**：`lsof +D <dir>` 返回空才算无主；进程正在用（venv/模型/临时库）的文件删除会破坏运行中任务，是最贵的错误。
- **磁盘满的故障伪装**：满盘会让应用以诡异方式失败（headless 浏览器起不来/页面加载失败→报 "Waiting for selector canvas failed"；写盘静默失败）。长任务（渲染/批量/下载）中途报这种错且已有部分产物落盘时，**先 `df -h` 再调试应用**。
- **大数据量任务开跑前先查余量**：估算产物总量再启动（如 9672 帧 JPEG≈1.4G+），确认空余 ≥ 产物 2-3 倍；产物帧保留好，腾出空间后从断点续跑（工具支持 --start 快进则优先续跑不重算）。
- **du 两次结果可能不一致**：/tmp 大文件并发增删时以当前 `df` + lsof 为准，别纠结 du 数字。
- **缓存类重下即恢复**（uv/pip/npm），删了只是下次下载慢点，优先级最高；数据类（备份/模型）删了不可逆，永远先问。
- **journal 清理要 sudo**：普通用户 vacuum 会报 Permission denied 且 free 0B，直接补 sudo 一步到位。
- **根路径删除命令会被 approval 拦截**：属正常，明确路径后继续，别绕开。
