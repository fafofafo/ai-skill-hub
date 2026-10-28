---
name: mv1
description: Use when 用户发MP3+多图要生成MV（频谱柱+歌词字幕）。端到端：频谱分析→官方歌词→渲染→叠字幕→发邮箱。
---

# MV1：图片+音乐+歌词 → MV（2026-09-29 用户命名固化，伍思凯《特别的爱给特别的你》全流程实测）

## 触发
- 用户发 MP3（背景乐）+ 多张图片（按序展示）→ 说"做视频/MV/生成视频"
- 完整流程：**频谱分析 → 查官方歌词 → headless渲染 → 叠字幕 → 发邮箱**

## 图片顺序铁律（用户 2026-10-11 强调固化）
- **视频第一张图必须 = 用户消息里发的第一张图**（img_xxx 按消息出现顺序），禁止按文件 mtime/尺寸/名称排序
- 用户发图时：逐条记录 img_xxx 文件名在消息中的出现顺序，该顺序即 img1..imgN 顺序
- 若两批图相同（重复发送），去重后仍按**用户消息顺序**排，不是按时间戳
- 素材尺寸不统一时：统一转 880×1184（居中裁切 cover 填充，保持主体），img1 仍是用户第一张

## 成品规格（用户拍板，勿改）
- 竖版 3:4（880×1184，与素材一致）；时长=歌全长
- 主图原生 ctx.drawImage 铺满全屏（无黑边），每张图按歌长均分（SWITCH_T=duration/图片数），**交叉淡化 2s 切图**（前图保持后图淡入，杜绝闪黑断层）
- 频谱柱：白色带黑边（字幕同款），**BAR_MAXH=150**，44柱×14px，Attack 0.6/Decay 0.35，泛光 blur5
- 字幕：**Fontsize 60**，纯白 &H00FFFFFF + 黑描边 Outline 4（白字泛黑），**简体中文官方歌词**；**长句自动换行**（单行超宽时用 `\N` 拆行，每行 ≤ 12 个汉字，避免字幕出屏）（用户 2026-10-13 要求）
- 无脉冲环（用户要求只保留频谱柱）
- 交付：**默认发 QQ 邮箱**（授权码已存环境变量），发后 IMAP 读回验证；**只发邮箱，不压缩、不发预览版，发完即结束**（用户 2026-10-13 确认）

## 五步流程（全自动）
```bash
HERE=~/.hermes/skills/creative/musicvideo/scripts
WORK=/tmp/mv_job; mkdir -p $WORK
# 0. 素材就位: song.mp3 + img1..imgN.png(按序, 880x1184)

# 1. 音频→32频段频谱JSON (numpy STFT, ~40s/5min歌)
python3 $HERE/make_music_video.py viz-analyze --audio $WORK/song.mp3 --out $WORK/tl.json

# 2. 歌词时间轴: whisper 转录只取时间轴(不取文本), 官方歌词另行查证
HF_ENDPOINT=https://hf-mirror.com HF_HUB_DISABLE_XET=1 \
  python3 $HERE/make_music_video.py transcribe --audio $WORK/song.mp3 --out $WORK/ts.json

# 3. 官方歌词→ASS (简体, Fontsize60, 白字黑边): web_search 查官方歌词, 手动映射到转录段时间轴
#    (映射方法见 scripts/make_official_ass.py)
python3 scripts/make_official_ass.py  # 生成 subs_official.ass

# 4. headless 渲染 (8964帧/5min歌 ≈ 57min, 后台跑 --format jpeg 省磁盘)
python3 $HERE/make_music_video.py viz-render --images img1.png,...,img9.png \
  --audio $WORK/song.mp3 --tl $WORK/tl.json --out $WORK/mv.mp4 --fps 30 --format jpeg

# 5. 叠字幕 + 发邮箱
ffmpeg -y -v error -i $WORK/mv.mp4 -vf "ass=$WORK/subs_official.ass" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -c:a copy -movflags +faststart $WORK/final.mp4
SMTP_HOST=smtp.qq.com SMTP_PORT=465 SMTP_SENDER=345469023@qq.com \
  SMTP_CODE=$(grep QQ_SMTP_CODE ~/.hermes/.env | cut -d= -f2) \
  python3 ~/.hermes/skills/email/email-send-stdlib/scripts/send_smtp_attach.py \
  345469023@qq.com "$WORK/final.mp4" "MV标题"
# 发后 IMAP imap.qq.com:993 读回验证送达
```

## 官方歌词获取（关键！whisper 文本不可信）
- whisper 转录文本有**繁体+误识**（实测："我不處理想的時間"实为"我付出一生的时间"、"轻轻一绕着"实为"轻轻萦绕着"、"詞曲 李宗盛"实为"词：陈家丽 曲：伍思凯"）
- **先 web_search 查官方歌词（简体版）**，歌名+歌手查询；只把 whisper 的**时间轴**当参考，文本用官方
- 映射：官方歌词行 → 转录段索引（歌曲段落重复结构，人工映射一次），生成精确 ASS
- 参考脚本：`scripts/make_official_ass.py`（含完整映射逻辑，改歌词/时间即可复用）

## 铁律（血泪坑）
1. **headless 注入必须内联进 HTML，禁止运行时注入+reload**（reload 清空 window 变量→全片只显示第一张图）
2. **帧必须 canvas.toDataURL() 输出**（canvas.screenshot() 裁窄留白边）；长视频用 --format jpeg 省磁盘（单帧~430KB vs PNG 1.5MB）
3. **主图用原生 ctx.drawImage**（p5 image() 880×1184 右侧留白）
4. **chromium 用 Playwright 缓存版**（snap 版被 AppArmor 挡 file://）；puppeteer-core 软链自 p5js 技能 node_modules
5. **叠字幕前确认视频无字幕**（禁止二次叠加）；viz 渲染的视频是干净的，可安全 ass 叠加
6. **切换点亮度连续≠内容无跳变**：即使交叉淡化平滑，9 张差异大的插画切换仍会有"内容跳变感"——用户接受后不再反复调
7. 频谱柱参数：sqrt 感知压缩+灵敏度1.1+Attack 0.6/Decay 0.35；灵敏度过高会全饱和
8. 渲染耗时：5分钟歌=8964帧≈57min（后台跑，notify 完成）

## 验证清单（交付前）
- 9 图切换：抽每段中间帧，像素对比确认更像对应 imgN（9/9）
- 切换边界亮度连续无闪黑（交叉淡化生效）
- 字幕抽帧：简体、Fontsize 60、白字黑边、与频谱柱不重叠
- 邮件 IMAP 读回确认送达

## 相关
- 底层脚本：~/.hermes/skills/creative/musicvideo/scripts/make_music_video.py（viz-analyze/viz-render）
- 模板：~/.hermes/skills/creative/musicvideo/scripts/sketch_viz_template.html + render_mv.js + p5.min.js
- 案例成品：~/项目目录/outputs/special_love_citypop/（伍思凯《特别的爱给特别的你》Citypop版 v3 简体字幕）
