---
name: musicvideo
description: Use when 用户发 MP3+多张图片要做配乐视频（歌词字幕同步/Ken Burns 运镜/频谱可视化特效）。一键出片。
---

# 图片 + 背景乐 + 歌词字幕 视频生成（2026-09-28 固化，v5 实测；2026-09-29 加 viz 可视化模式）

## 触发
- 用户发 MP3（背景乐，可能带人声）+ 多张图片（按序展示）→ 说"生成/做成视频/配字幕"
- 可替换某张图（说"第 N 张替换成这张"）

## 默认规格（用户偏好）
- 视频时长 = 背景乐全长（不用卡点）；图片平均分配展示
- 竖版 3:4（880x1184，与素材一致）；**图片静态展示（无运镜，零抖动，2026-09-28 用户拍板；运镜版用 --still 去掉，默认 render 即静态）**
- 字幕：**金色霓虹+抖动动画**（底部居中、金色主字+品红描边+发光 blur0.6+弹出震动 fscx/fscy 交替，v8 实测：20.2-20.8s 字幕区帧差 11-12=抖动中，落定后静止）；**语音起→字幕现 / 语音止→字幕隐**（faster-whisper 词级）
- 交付：**默认只发邮箱**（QQ SMTP），未主动要求不发企微
- 文件体积：crf 28（静态版 13MB/298s；运镜版 27MB）

## 三命令流程（脚本 scripts/make_music_video.py，用绝对路径）
```bash
# 1. 词级时间戳（faster-whisper，模型已缓存 ~/models/whisper，首次 ~3min 后续 ~45s）
python3 scripts/make_music_video.py transcribe --audio in.mp3 --out /tmp/ts.json

# 2. 歌词行(每行一条，用户提供或 ASR 文本) → ASS（起止=语音起止，底部样式）
python3 scripts/make_music_video.py ass --ts /tmp/ts.json --lyrics /tmp/lyrics.txt --out /tmp/subs.ass

# 3. 从原始图片一步渲染（默认静态 --still + 字幕 + 音乐，无旧字幕残留；去运镜）
python3 scripts/make_music_video.py render --images a.png,b.png,c.png --ass /tmp/subs.ass \
  --audio in.mp3 --out out.mp4 --w 880 --h 1184 --crf 28 --still
```

## 可视化特效模式（viz，2026-09-29 新增，已验证）
在 musicvideo 基础上叠加**频谱柱**（复刻歌词字幕白字黑边样式，随音乐起伏）：
```bash
# 1. 音频 → 32频段频谱JSON（numpy STFT，40Hz~18kHz 对数分段+低频节拍）
python3 scripts/make_music_video.py viz-analyze --audio in.mp3 --out /tmp/tl.json

# 2. 图片+频谱 → headless p5.js 逐帧渲染 → ffmpeg 合成
python3 scripts/make_music_video.py viz-render --images a.png,b.png --audio in.mp3 \
  --tl /tmp/tl.json --out out.mp4 [--w 880 --h 1184] [--crf 23] [--fps 30]
  [--cfg "BAR_COUNT=60,BAR_W=10,SUB_R=255,SUB_G=215,SUB_B=0,TITLE=我的MV"]  # 覆盖模板参数
```
- **默认样式**：主图原生ctx铺满全屏（无黑边）+ 白色带黑边频谱柱（泛光 blur5，BAR_MAXH 150）+ **交叉淡化切图（前图保持后图淡入 2s，杜绝切换闪黑断层）** + 字幕（Fontsize 60、纯白 &H00FFFFFF + 黑描边 Outline 4 = 白字泛黑）
- **cfg 可调**：BAR_COUNT柱数 / BAR_W柱宽 / BAR_MAXH高上限(默认150) / SUB_R,G,B主体色(默认字幕白250,234,217) / BORDER描边 / BLUR泛光 / TITLE标题 / SWITCH_T切图间隔
- **字幕样式已固化**：Fontsize 60 + PrimaryColour 纯白(&H00FFFFFF) + OutlineColour 黑(&H00000000) + Outline 4 = 白字黑边"白色泛黑"（用户 2026-09-29 拍板）
- **歌词必须用官方简体文本**（2026-09-29 用户要求）：whisper 转录文本有繁体/误识（如"我不處理想的時間"实为"我付出一生的时间"），**先 web_search 查官方歌词（简体），再用 whisper 时间轴做字幕**；歌曲《特别的爱给特别的你》= 伍思凯/词陈家丽（whisper 误标"词曲 李宗盛"）
- **简体字幕字幕验证**：ffmpeg ass 滤镜用 fontconfig 找字体，wqy-zenhei 支持简体；黑底测试帧上黑边不可见是正常的（黑边=黑色与黑底同色），彩色背景上正常显示
- 依赖：numpy + node + puppeteer-core（已软链到 scripts/node_modules）+ Playwright chromium（render_mv.js 自动探测）

## 关键流程细节
- **歌词来源优先级**：用户提供的歌词 > whisper 转录文本（whisper 文本可能繁体/误识，仅作时间轴参考）；歌词行数≠whisper段数时脚本自动按语音时长聚类
- **替换图片**：替换后重新按上传时间排序（ls --time-style=full-iso 精确到纳秒）
- **验证**：抽帧（select=eq(n,帧)）+ 像素分析（底部白像素：语音中>300，语音间隔<30）或用 vision 确认字幕内容/无叠字
- **发邮箱**：smtplib SMTP_SSL smtp.qq.com:465，授权码环境变量（QQ_SMTP_CODE），附件<50MB；发后 IMAP imap.qq.com:993 读回验证

## 铁律（血泪坑，勿再犯）
1. **从原始图片一步渲染**：禁止在已烧过字幕的视频上二次 ass 叠加（旧字幕无法清除=两层字幕叠一起，v2/v3 踩过）
2. **zoompan 去抖动配方（v6 起默认）**：输入先 `scale=iw*2:ih*2:flags=bicubic` 再 zoompan（取整误差相对小），z 用**线性匀速** `min(z0+on*步长,z0+0.10)`（z0 交替 [1.0,1.06,...]），**禁用 sin 回摆**（v2/v5 抖动=sin 加速突变+低分辨率取整跳动；实测 v6 相邻帧差 0.05-0.53 vs v3 18-43）
3. **时间戳工具选型**：faster-whisper 词级（±0.1s，首选，已装+模型缓存）> XingChenASR-Diarize（有时间戳但碎片化）> Qwen3-ASR（文本准但无时间戳）> SenseVoice（漏词严重，仅作粗定位）；硅基流动不支持 timestamp_granularities 参数（400）
4. **mp3 分段 seek**：`-ss` 必须放 `-i` 后（输出端 seek 精确）；放 `-i` 前快速 seek 会错乱段序
5. **Ken Burns 帧数**：d = 每张时长×25fps（298s/6张 ≈ 1243 帧/张）
6. **ASR 计费**：按音频时长秒数（非 token），细分段总时长不变费用不变；结果回显才占少量上下文
7. **字幕真实颜色=白字黑边，不是金色（2026-09-29 实测）**：ASS 代码写 `&H0000D7FF`(金色)，但实际成片抽帧 = 白色主字 (250,234,217) + 深紫黑描边 (47,35,45)。**以成片实测为准，别信 ASS 代码推色**；做配色对齐前先抽帧验色
8. **headless 渲染帧必须用 canvas.toDataURL()（2026-09-29 血泪）**：`canvas.screenshot()` 会把 880px 宽内容裁成 ~700px 留右侧白边——曾误判"图片没铺满"调试 1 小时。render_mv.js 已内置 toDataURL
9. **主图用原生 ctx.drawImage 铺满**：p5 的 `image()` 渲染 880×1184 时右侧留白，改用 `drawingContext.drawImage(ni,0,0,W,H)` 精确铺满
10. **headless 依赖**：puppeteer-core 软链自 p5js 技能 node_modules（勿删）；chromium 用 Playwright 的（snap 版被 AppArmor 挡 file://）；p5.min.js 本地化避免 CDN 时序问题
11. **频谱柱参数平衡**：sqrt 感知压缩（弱信号可见）+ 灵敏度 1.1 + Attack 0.6/Decay 0.35（≈1:2.5，反应快消失慢）；灵敏度过高(1.6+慢衰减)会 32 柱全饱和顶到上限，先跑稳态模拟找平衡点
12. **headless 注入必须内联进 HTML，不能运行时注入+reload（2026-09-29 血泪）**：`page.evaluate` 设置 `window.__IMGS/__CFG` 后 `page.reload()` 会**清空所有 window 变量**→ 图片列表回退模板默认、SWITCH_T 错乱 → 全片只显示第一张图。viz_render 已改为 Python 生成时把 IMGS/SWITCH_T/CFG 直接写死进 sketch HTML（re.sub 替换模板行）。**新写 headless 模板时禁止依赖 reload 后保留的注入变量**

## 相关
- 模型：faster-whisper small（~/models/whisper/，Hermes venv 已装 1.2.1）
- 案例：FAFO_romantic v5（298s 竖版 22 行字幕 38MB）→ ~/项目目录/outputs/
- 可视化模板：scripts/sketch_viz_template.html（图片+频谱柱）；POC 演化史在 ~/项目目录/outputs/mv_poc/
