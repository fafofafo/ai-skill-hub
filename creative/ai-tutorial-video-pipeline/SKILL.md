---
name: ai-tutorial-video-pipeline
description: Use when 把脚本批量做成教程口播视频 MP4。画面必须"有内容"（信息卡而非插画）。
version: 1.0.0
---

# AI 教程视频自动生产流水线（脚本 → MP4）

## 何时用
用户做"AI 工具/教程"类口播视频（B站/视频号等），需要把文字脚本批量变成可发布的 MP4。已应用于 `~/ai-video-content/`（20 条选题库 + 全套脚本 + 合成流水线）。

## 核心用户偏好（最重要，用户两次纠正过）
**教程视频画面必须展示"内容"**：要点文字、关键命令、步骤编号、数据。
- 用户原话："这个视频展示内容不行，需要图文并茂的展示"、"视频全程没有内容展示"
- 画面形式 = **信息内容卡**（主标题 + 副标题 + 要点列表 + 底部关键信息条），PIL 生成
- 不要用"科技插画 / AI 生成图"当教程主体画面（只能当封面点缀）
- 配音讲什么，画面就显示什么

## 分工约定（用户明确）
- **Agent 负责**：选题、脚本、配音、信息卡、视频合成、内容库管理、数据复盘
- **用户负责**：平台注册、API 申请、屏幕录制素材（需用户设备）、发布、扫码登录
- 登录墙（B站等）：只能用户扫码授权，Agent 绝不猜密码

## 流水线（5 步）
1. **选题库/看板**：`选题库.tsv`（编号|标题|定位|优先级|脚本|录制|发布 状态列）；`gen_script.py --status` 看进度
2. **脚本**：每选题一个 `NN_脚本_*.md`（3 个标题备选 + 封面文案 + 简介 + 带时间轴口播稿 + 屏幕演示步骤 + 标签）
3. **分段内容定义**：`NN_content.json`（每段：`card` 标题 / `sub` 副标题 / `bullets` 要点列表 / `footer` 底部关键信息）
4. **配音**：edge-tts，zh-CN-YunxiNeural（男声）或 Xiaoxiao（女声）
5. **合成**：信息卡(PIL) + 配音 → 逐段 mp4 → concat 完整视频

## 环境依赖（一次性）
```bash
sudo apt-get install -y fonts-wqy-zenhei        # 中文字体 wqy-zenhei.ttc
~/.hermes/bin/uv venv ~/video-venv
~/.hermes/bin/uv pip install --python ~/video-venv/bin/python -i http://mirrors.tencentyun.com/pypi/simple pillow edge-tts
```
- PIL 加载 ttc：`ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", size, index=0)`
- ffmpeg 的 drawtext 支持 ttc 渲染中文（已验证）

## 关键脚本（位于 ~/ai-video-content/）
| 脚本 | 作用 |
|---|---|
| `make_cards.py` | content.json → 信息卡 PNG（1920×1080，渐变背景+圆点要点+底部信息条） |
| `img_video.py` | 卡片/图片 + 配音 → 完整 MP4（`--notitle` 画面自带标题时不叠 drawtext） |
| `gen_video.py` | 纯文字卡版（备选；批量时注意限流） |
| `gen_script.py` | 选题库 → 脚本骨架 + 看板状态 |

## 陷阱（全部实测踩过）
1. **edge-tts 限流**：连续多段生成报 `NoAudioReceived`。必须：每段重试（最多 4 次，退避 3s×attempt）+ 段间 `sleep 2`。单条 CLI 成功 ≠ 批量能过。
2. **信息卡已含标题时别叠 drawtext**：会重叠 → 用 `--notitle`。
3. **图片比例**：素材须 16:9（如 1672×941）；非标用 `scale=1920:1080:force_original_aspect_ratio=decrease,pad=...`。
4. **看不了图**：当前模型无视觉，图片顺序/内容靠文件名约定（`01.png`=段1）+ 用户验收；合成后抽帧用 `MEDIA:` 发用户确认。
5. **中文长标题**：信息卡标题超长自动缩字号；要点自动换行（PIL 逐字 wrap）。

## 验证
- `ffprobe -show_entries format=duration,size` 检查时长/体积
- 抽帧：`ffmpeg -ss N -i in.mp4 -frames:v 1 out.png` 发用户验收
- 交付后必须请用户确认：内容密度、排版、图片顺序

## 参考
- `references/commands-and-pitfalls.md` — 完整命令与错误实录
