---
name: wechat-article-extraction
description: "Read mp.weixin.qq.com 公众号 articles via curl + regex."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [wechat, chinese-content, extraction, curl, scraping]
    related_skills: [blocked-page-recovery, grounded-citations]
---

# WeChat 公众号 article extraction

Use when the user shares an `mp.weixin.qq.com/s/...` link (or pastes a 公众号
article) and you need its text — for reading, verifying, or discussing.
Recurring for this user: they're on WeCom and regularly share WeChat
articles without an explicit instruction (expected behaviour: read, verify
authenticity, discuss — don't rush to produce output/video).

## Why not the usual tools

- `web_extract` on `mp.weixin.qq.com` often fails with
  `CRAWL_UNKNOWN_ERROR` (no EXA/backend key, or the host refuses).
- The browser tool can hang for minutes on the ~3 MB page.
- A plain `curl` with a realistic User-Agent gets the full HTML every time.

**Go straight to curl — do not burn a browser timeout first.**

## Fetch

```bash
curl -sL --max-time 60 \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  "https://mp.weixin.qq.com/s/<ARTICLE_ID>" -o wx_article.html
```

Page is ~3 MB — parse in Python (stdlib), don't rely on head/tail truncation.

## Parse (python3, stdlib only)

See `references/wechat-mp.md` for the full recipe. Summary:

- **Title**: `<h1[^>]*>(.*?)</h1>` (strip tags + `html.unescape`)
- **Account/author**: `var nickname = "(.*?)"`
- **Publish time**: `var ct = "(\d+)"` — unix timestamp, display as UTC+8
- **Body**: `<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script`, then turn
  block tags (`<br|/p|/div|/section|/h\d|/li>`) into newlines, strip remaining
  tags, unescape, collapse 3+ newlines.

## Verify, then discuss (this user's expectation)

1. Extract title / account / publish date — first authenticity check.
2. Verify the article's **claims** against primary/official sources (official
   docs, the tool's real docs, upstream repo) before relaying them as fact.
3. Check relevance to the user's own environment (installed versions, whether
   the feature is reachable from their setup) — makes the discussion concrete.
4. Report a claim-by-claim verification table + what it means for the user;
   offer next steps. Do NOT start producing a video unless the user asks.

## Pitfalls

- Never relay the article's claims as truth without cross-checking at least
  one primary source.
- If the user's install differs from the article's described version, say so
  explicitly (their environment may be ahead/behind the article).
- Strip tags BEFORE collapsing whitespace, or you'll leave stray inline text
  concatenated across block boundaries.
