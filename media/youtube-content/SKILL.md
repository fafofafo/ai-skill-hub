---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
version: 1.0.0
author: Teknium (teknium1), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [YouTube, Video, Transcripts, Media]
    related_skills: []
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

Use `uv` so the dependency is installed into the same Hermes-managed environment
that runs the helper script:

```bash
uv pip install youtube-transcript-api
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
uv run python SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
uv run python SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
uv run python SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
uv run python SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps` via `uv run python`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: run `uv pip install youtube-transcript-api` and retry.

## Invidious 备选通道（2026-09-22 配置）

**用途**：无广告下载视频/音频（学习用）、转录失败/反爬时的备选通道、绕过 youtube.com 直连障碍。Invidious = YouTube 开源替代前端（AGPL-3.0，视频仍来自 YouTube 官方流，无广告无追踪；违反 YouTube ToS 但非版权侵权）。

**已验证可用实例**（经七牛云 socks5 隧道 `127.0.0.1:1080`）：
- `invidious.nerdvpn.de` ✅（2026-09-22 实测通过）
- 备选：`yewtu.be`（慢/易超时）、`inv.nadeko.net`（常 418）——实例不稳定会变，测通再用

**命令**（必须先走隧道，本机直连境外实例易被墙）：
```bash
# 拉取视频信息
https_proxy=socks5://127.0.0.1:1080 yt-dlp -J --no-warnings "https://invidious.nerdvpn.de/watch?v=VIDEO_ID"
# 下载音频（学习/转录用）
https_proxy=socks5://127.0.0.1:1080 yt-dlp -x --audio-format mp3 -o "/tmp/%(id)s.%(ext)s" "https://invidious.nerdvpn.de/watch?v=VIDEO_ID"
```
- yt-dlp 路径：`~/.local/bin/yt-dlp`（agent-reach venv 也有）

**坑**：①公共实例会被谷歌封锁，418/超时=换实例 ②走 Invidious 下载 = 去广告，**影响 UP 主广告分成**（客观代价，学习用途可接受，商用素材要评估）③youtube-transcript-api 是主通道，Invidious 只是备选
