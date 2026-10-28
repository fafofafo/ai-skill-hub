# B站音频提取 + 开场独白手工分段（MV 无附件场景）

## 场景
用户只给「音乐：歌名+歌手」和技能名、没发 MP3 附件/链接 → 从 B站取完整版音频（2026-10-27 张宇《给你们》实测跑通）。

## 提取流程
1. 找 bvid：`bili search` CLI 对歌名常返回空 data → 用 `web_search「歌名 bilibili」`拿 bvid（选 duration 接近原版完整时长，如《给你们》281s）；确认 bvid 用 view API（带完整头）
2. view API 拿 cid（裸 curl 常返 412/HTML 出错页，必须带完整 Chrome 头 + buvid3 cookie）：
```bash
BUV="buvid3=$(cat /proc/sys/kernel/random/uuid)INITWIR1900"
HDRS=(-A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" -H "Accept: application/json" -H "Referer: https://www.bilibili.com/" -H "Origin: https://www.bilibili.com" -H "Cookie: $BUV; b_nut=1792000000")
curl -s "${HDRS[@]}" "https://api.bilibili.com/x/web-interface/view?bvid=$BV"   # → data.cid, data.duration
```
3. playurl 拿音频流：`https://api.bilibili.com/x/player/playurl?bvid=$BV&cid=$CID&fnval=16` → `data.dash.audio[]`，选 `bandwidth` 最大项（如 id 30280/130416），取 `baseUrl`
4. 下载 m4s：`curl -sL -A "Mozilla/5.0" -H "Referer: https://www.bilibili.com/" "$url" -o audio.m4s`
5. 转 mp3：`ffmpeg -y -v error -i audio.m4s -c:a libmp3lame -b:a 128k song.mp3`；ffprobe 验证时长
6. YouTube 官方 MV 是备选（yt-dlp）——腾讯云访问 YouTube 常超时，B站路径优先

## 开场独白检测与手工分段（血泪坑）
B站搬运视频常带开场独白/口播（《给你们》开头约 16s「什么是缘分的…」）。whisper 全音频转写后：
- **判据**：ts 首段文本不是歌词 → 自动 `lyrics_segment.py`（按句数比例映射到 whisper 段）会把歌词全挤到开头、末段异常长（59-280s）——只要歌词没铺满全歌（末段占比离谱）就是错位
- **修复步骤**：
  1. 打印 ts 全部 s/e 时间轴（ts_full.json 用 `s`/`e` 字段不是 start/end），找歌曲真实起点与副歌重复结构
  2. 抽关键时间点音频片段时间转写验证（`ffmpeg -ss X -t 8` 切段 + WhisperModel）确认歌曲从哪秒开始、段结构是否吻合官方歌词
  3. 按官方歌词段落 + whisper 真实 s/e 边界**手工构建 segments.json**：每段 start/end 用 whisper 锚点、theme 取该段核心句（副歌重复段换主题/换角度、首末图 theme=歌名），总时长=歌全长
  4. ASS 字幕同样按 whisper 逐句 s/e 映射官方歌词（长句 `\N` 拆两行，每行 ≤12 汉字）
- 图片数量公式照旧：N=ceil(歌唱时长/25)，首图=0→第一句歌词开始
- 手工 segments/字幕 后渲染脚本必须同步写（CUTS/frames 按新段边界），不要沿用旧的

## 手工调 WhisperModel 的模型路径
`make_music_video.py transcribe` 内部能定位模型，但自己内联 faster_whisper 时必须用完整快照路径：
`/home/ubuntu/models/whisper/models--Systran--faster-whisper-small/snapshots/<hash>`
（`~/models/whisper/small` 简写报 `HFValidationError: Repo id must be in the form 'repo_name' or 'namespace/repo_name'`；用 `find ~/models/whisper/models--Systran--faster-whisper-small -name model.bin` 定位 hash）
参数：`WhisperModel(路径, device="cpu", compute_type="int8", local_files_only=True)`；环境 `HF_HUB_OFFLINE=1 HF_HUB_DISABLE_XET=1 PYTHONPATH=`；转写结果文本不可信只取时间（mv1 铁律）。
