---
name: code-driven-mv
description: "Use when 代码直出动画MV：音频节拍驱动p5.js逐帧绘制→headless渲染→ffmpeg合成。"
---

# 代码直出动画 MV（2026-09-29 实测，P0-P3 全通，零成本）

Opus 5.5 "代码直出 MV" 思路的可复刻路线：**不依赖任何视频生成模型**，预分析音频 → p5.js 写代码逐帧绘制 → headless Chrome 渲染 → ffmpeg 合成。15s/30fps/450帧：纯动画 46s 渲染，静态图版 150s。

## 触发
- 用户研究/要求"代码直出 MV"、"AI 写代码画视频"、"Opus 5.5 思路"，或 MP3（可+多图）要带动态动画而非静态轮播的配乐视频
- 该技能是 musicvideo（静态图+字幕）的动画升级路线；纯静态图+歌词字幕场景仍走 musicvideo

## 流程（脚本 scripts/audio_timeline.py + scripts/render_mv.js）
```bash
# 1. 音频预分析：STFT(win1024/hop512, 22050 mono wav) → 40Hz~18kHz 对数分 32 频段
#    + 99分位归一化 + 低频鼓点检测 → timeline_spec.json{duration,n_bands,beats,spec[][],spec_hop_s}
python3 scripts/audio_timeline.py in.mp3 /tmp/timeline_spec.json

# 2. 写 sketch.html（见下方规格）

# 3. 逐帧渲染（puppeteer-core + Playwright chromium）
NODE_PATH=<p5js技能目录>/scripts/node_modules node scripts/render_mv.js sketch.html \
  --frames 450 --width 880 --height 1184 --chrome <playwright-chromium路径>

# 4. 合成（音频原样进）
ffmpeg -y -framerate 30 -i frames/frame-%04d.png -i in.mp3 -c:v libx264 -crf 23 -pix_fmt yuv420p -c:a aac -b:a 128k -shortest -movflags +faststart out.mp4

# 5. 验证：多时刻抽帧 MD5 全不同（确认动态非静止）+ vision 看帧确认无重叠/溢出；
#    频谱柱/粒子是否真随乐起伏用 vision 读帧 + 读时间戳调试文字（画 L:/M: 值），勿信像素统计
```

## sketch.html 规格（必须遵守）
- **timeline 内嵌 JS 常量**（写文件时把 timeline JSON 注入 HTML），不要 fetch——file:// 下 CORS 失败；32×323 spec 内嵌后 HTML ~80KB 正常
- p5.js **必须 noLoop() + window._p5Ready=true**（render 脚本逐帧 redraw 精确对应，否则丢帧/跳帧）
- 动画由时间驱动：`frameCount/FPS` 查 timeline 频谱/节拍，**不用实时 FFT**（headless 音频不稳定）
- 关键参数：randomSeed/noiseSeed 固定（可复现）、pixelDensity(1)、p5.disableFriendlyErrors=true

## 三大可视化系统（用户参数指南已落地，实测平衡点）
### 频谱柱
- 两种布局：居中 32 根（3px 柱+1px 间距）或**铺满整屏 80 根**（BAR_W=7px，间距=(W-80*BAR_W)/79 自适应）；对数频段映射在预分析完成，JS 不用重映射
- **用户最终配色与尺寸（2026-09-29 拍板，覆盖早期版，含用户最后纠正）**：**白色主字+深色描边（"白色泛黑"，与字幕实际渲染一致）** + **更粗** + **带泛光**——44 根 × BAR_W=14px，**BAR_MAXH=150**（演进：80 → "稍微长一些"110 → "再长一些"200 → 用户看片后最终拍板 150），贴底 BAR_Y=H-14；**颜色=musicvideo 字幕实测色：白 RGB(250,234,217) + 黑描边**（早期以为"金色与字幕一致"是错的——ASS 代码 `&H0000D7FF` 解析像金但 ffmpeg 实际渲染成白字泛黑；**以成品抽帧实测为准**）。**alpha 必须 255**（半透明会被底色拉暗：alpha110→色差27，alpha255→色差0）。早期 hue 45-55/80根/BAR_MAXH120/alpha110 及"金色 RGB(255,215,0)"已被本规格取代
- **泛光（复刻字幕 blur0.6 发光，两层绘制）**：先 `gctx.save(); gctx.filter='blur(5px)'` 画半透明白色发光层（`fill(255,255,255,140)`，矩形扩边 3px→`rect(x-3, y-3, w+6, h+6)`），再 `gctx.restore()` 画黑描边层（`fill(0,0,0,255)` 扩 3px）最后实心白色核心层 `fill(250,234,217,255)`。**blur 半径 >7px 会糊满全屏**（柱宽才 14px）；blur 4-5px+alpha 120-140 柱侧 6px 有可见光晕。泛光层很耗渲染（450 帧 203s vs 纯色 51s），后台跑。白柱的泛光在全图（暖黄背景）上会被淹没，vision 可能误报"无泛光"——用纯色背景隔离测试确认实现存在
- **感知压缩 `pv(v)=sqrt(min(1,max(0,v)))`**：线性映射下归一化值多 0.001~0.1 不可见，sqrt 让弱信号可见（关键）
- Attack/Decay ≈1:2.5：att 0.6（反应快）/ dec 0.35（消失慢）→ 柱高中位 199px/P90 275px
- 灵敏度 sens 1.1；过高(1.6)+慢衰减→32 柱全饱和顶上限，过低(0.9)→偏矮无起伏
- **先参数扫描再渲染**：Python 里用同差分方程 `bar += (target-bar)*(att if target>bar else dec)` 跑完整时间轴看柱高分布，秒级找平衡，别每版 60s 渲染
### 粒子
- 上限 700；发射按 low/mid/high 加权；速度=固定值0.5+energy×3.0（防静音静止）；尺寸 2.5×(0.5+low×2.5)（低频强变大）；颜色 280+low×70（低频暖紫→高频蓝紫）
### 脉冲环
- 上限 3，低频鼓点触发；半径 70 起扩散到 55% 屏宽；衰减 0.90/帧（短促不糊）

## 节拍响应 = 平滑能量衰减，不硬触发（用户拍板：缓和、短、慢）
```js
let beatE = 0;
if (isBeat) beatE = 1;
beatE *= 0.88;   // 快速柔和回落
// 所有效果乘 beatE：主图呼吸 1+beatE*0.004、频谱增强 1+beatE*0.15、标题亮度微调
```
硬触发（每拍 if 跳一个值）显剧烈——用户明确拒绝。实测节拍点帧差 ~5.8/255 为舒适量级。

## 静态图片混合（用户 2026-09-29 拍板，最终 v11 规格）
- **图片完全静态且铺满全屏**：主图用原生 `drawingContext.drawImage(ni, 0, 0, W, H)`（`preload()` 里 `new Image()` 加载同目录图），**不依赖 p5 的 image()**——p5 image 渲染 + screenshot 组合易出右侧白边；**无 Ken Burns、无节拍呼吸、无位移**（用户先要运镜后两次改口拍板静态——默认直接静态，除非明确要求运镜）
- 多图按 SWITCH_T 秒切换；**必须交叉淡化（cross-fade）**：前图保持 + 后图淡入，过渡 2s 无硬切。旧版"当前图 fade 从 0 淡入"会在每 33s 切换瞬间透明度归 0 → 露出深色背景 → 闪黑断层感（用户报"图片断层/背景乐断层"瑕疵，根因是切换闪黑不是音频问题）。实现：`fadeDur=2.0/SWITCH_T`；`phase<fadeDur` 时先 `globalAlpha=(1-phase/fadeDur)` 画前图再 `globalAlpha=phase/fadeDur` 画后图，否则后图全不透明。主图区连续帧像素差 ≈0.6/255 即静态达标；切换边界亮度必须连续（120→119 渐变，无突降）
- 叠加层（花瓣/频谱柱/脉冲环/标题）半透明、颜色呼应主图、不遮挡主体
- 图片加载用 `preload()` + `loadImage`（相对路径，HTML 与图同目录）

## 花瓣系统（用户先要桃花瓣，后**拍板去掉花瓣**）
- **默认无花瓣**（2026-09-29 最终规格）；用户要花瓣时按下方桃花瓣配方，满屏 90 朵飘落
- 桃花瓣配方：五瓣花常驻飘落，**size 18-40px**、下落 0.8-2.4px/帧、左右摇摆(swayAmp 90)+自旋(±0.025)、桃红 hue 338-352 alpha 45-75
- **桃花瓣形态（从樱花改拍板桃花）**：圆润宽大、宽≈长——外瓣 `ellipse(0,-s*0.36,s*0.95,s*0.92)`（深粉 hue,65,bright*0.92）+ 内瓣高光 `ellipse(0,-s*0.44,s*0.6,s*0.7)`（浅粉），**8 根金黄放射花蕊丝**（strokeWeight max(1,s*0.06)，line 至 r*0.22）+ 金黄花心圆；先端圆钝无 V 缺口是桃花对樱花的关键区分（樱花=V 缺+无金蕊）
- 音乐强(low>0.3)时摇摆速度×1.5
- 越界回收：`y>H+size` 时重新 spawn 从顶部落下；`randomSeed` 固定保证可复现
- 花瓣很小(≤40px)叠在复杂插画背景上时 vision/像素检测都难辨认，先用纯色背景 + 大尺寸单帧验证花瓣形态（petal_test 手法），再合回正式渲染

## 坑（血泪）
- **p5.js 必须本地引用，不走 CDN**：headless 下 cdnjs 加载间歇性失败（PAGEERR `p5 is not defined`，canvas 已建但 draw 不执行，帧变黑/空）。把 p5.min.js 下载到 sketch 同目录，`<script src="p5.min.js">` 相对引用；下载一次存档复用（~/项目目录/outputs/mv_poc/p5.min.js）
- **帧输出必须 `canvas.toDataURL('image/png')`，禁用 `canvas.screenshot()`**：screenshot 会把 canvas 内容截窄留白边（880px 宽被截到 ~700px，右侧整列纯白；canvas 内部像素其实正确，被截层骗了）。toDataURL 序列化 100% 精确，且渲染从 150s 提速到 53s
- **headless 渲染必须用 Playwright 的 chromium**（~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome）；不能用 /usr/bin/chromium 或 google-chrome——它们指向 **snap 版**，AppArmor 挡 file:// 访问和 /tmp 写入（ERR_FILE_NOT_FOUND / Permission denied），先查 Playwright 缓存
- **p5 colorMode(HSB) 下 `fill(255,215,0)` 会按 HSB 解析**（三个数=色相/饱和度/明度，不是 RGB）：要填精确 RGB 色先 `colorMode(RGB,255)` 再 fill，画完切回 `colorMode(HSB,360,100,100,100)`（频谱柱金色就是这个坑——HSB 模式直填 (255,215,0) 出来的不是目标金）
- puppeteer-core 装在哪就 NODE_PATH 指向哪（p5js 技能 scripts 下 node_modules 是现成位置）；不要装完整 puppeteer（自带浏览器下载、GitHub 被墙）
- **像素验证会被图片背景骗**：频谱柱区域下方若是插画彩色街道/招牌，彩色像素检测全算进去=假满柱。用 vision 读帧 + 读时间戳调试文字（画 L:/M: 值）做真实验证
- **全图上 vision 判"无泛光/无花瓣"会被复杂背景骗**：blur 泛光/小花瓣叠在暖黄灯光插画上会被同色系背景淹没，vision 会误报"没有发光"。先用纯色/深色背景 + 大尺寸单帧隔离测试（画几根柱/几朵花），vision 确认效果真实存在后再合回正式渲染——渲染层有、全图看不见，是背景同色淹没不是实现失败
- **图片铺满验证的数组索引陷阱**：PIL 数组是 `img[y, x]`（shape H×W×C），验右侧白边要 `img[:, x_start:x_end]` 而不是 `img[x_start:x_end]`——x/y 写反会取到错误区域得出假结论（先查 shape 再下判断）
- 图片版渲染 ~3fps（纯动画 ~10fps），大图 450 帧约 2.5 分钟——图片版预期慢，后台跑
- **IMGS/SWITCH_T/CFG 必须内联写死进 sketch HTML，禁止运行时注入+reload（2026-09-29 血泪）**：`page.evaluate` 设置 `window.__IMGS/__CFG` 后 `page.reload()` 会**清空所有 window 变量**→ 图片列表回退模板默认、SWITCH_T 错乱 → 全片只显示第一张图（症状：9 张图视频 5-70s 全是 img1）。修法：Python 生成 sketch 时用 `re.sub` 把 IMGS 数组、SWITCH_T、CFG 直接替换模板行写死进 HTML，render_mv.js 不再传 --imgs/--json。新写 headless 模板一律内联，别依赖 reload 后保留的注入变量
- **长视频(>2min)必须用 JPEG 帧输出**：PNG 帧 ~1.5MB/帧，5 分钟歌 30fps ≈ 8964 帧 ≈ 13GB 超磁盘（剩 9.5GB 会失败）。render_mv.js 支持 `--format jpeg`（~430KB/帧，8964 帧 ≈ 4GB），viz-render 透传 `--format jpeg`。**jpeg 帧扩展名是 `.jpeg`，ffmpeg 输入通配必须写 `%04d.jpeg`，写 `%04d.jpg` 匹配不到文件**（render_mv.js 生成 .jpeg）。渲染前先 `df -h` 查磁盘预算
- 渲染途中音频被 /tmp 清理 → 从已有成品 MP4 `-vn -c:a copy` 抽回（原流可能 AAC 非 MP3，抽 .m4a 即可）
- 验证抽帧用 `ffmpeg -ss <t> -i out.mp4 -frames:v 1`，MD5 不同才证明动态

## 用户偏好（延续 musicvideo）
- 图片完全静态；节拍动效缓和/短/慢，忌爆闪剧烈
- **频谱柱/元素颜色 = musicvideo 字幕实际渲染色**：白主字 (250,234,217) + 深描边 (47,35,45)，"白色泛黑"，**不是金色**（2026-09-29 用户纠正；先信成品抽帧实测，不信 ASS 代码解析）
- 交付默认只发邮箱（QQ SMTP）；未主动要求不发企微；POC 演示可直接企微发（<20MB）
- 竖版 3:4（880x1184）或 720x1280；产物归档 ~/项目目录/outputs/mv_poc/

## 相关
- code-driven-video（早期 P0 版，已被本技能取代，勿再加载）：本技能为其完整演化
- p5js 技能（bundled）：headless 渲染脚本 export-frames.js/render.sh 的依赖即 puppeteer-core，参考其 6 阶段管线与 per-clip 架构
- musicvideo（user-owned）：歌词词级时间戳（faster-whisper）+ ASS 叠加可在本路线上做歌词字幕同步。**字幕叠加=两步**：viz-render 先出无字幕视频，再 `ffmpeg -i video.mp4 -vf "ass=subs.ass" -c:a copy out.mp4`（viz 视频无字幕，叠加安全，不违反"禁止二次叠加"铁律）。字幕样式（用户 2026-09-29 最终拍板）：**Fontsize 60** + PrimaryColour 纯白 `&H00FFFFFF` + OutlineColour 黑 `&H00000000` + Outline 4 = 白字泛黑（"放大"的两次反馈最终定格 60，不是 70）；字体 WenQuanYi Zen Hei（系统仅有 wqy-zenhei，简繁字形都含）；歌词正文必须**简体中文**
- **歌词必须搜官方歌词，whisper 转录文本不可作字幕正文（2026-09-29 血泪）**：whisper 对已发布歌曲误识严重——《特别的爱给特别的你》被误认"词曲 李宗盛"（实为陈家丽词/伍思凯曲）、“我付出一生的时间”误成“我不處理想的時間”、“轻轻萦绕着我的心”误成“輕輕一繞著”；繁体/简体混杂。**流程：先 web_search 官方歌词 → 按歌曲段落结构人工建 (歌词行, 转录段起止索引) 映射表 → 用转录段的时间边界 + 官方歌词文本生成 ASS**。whisper 只可信时间轴，不可信文本。映射表做法见 /tmp/mv_real/make_official_ass.py 先例
