# WeChat 公众号 article — full fetch + parse recipe

Verified 2026-08 on a Tencent Cloud headless box. This recipe fetched and
parsed a 3.2 MB article page where `web_extract` returned
`CRAWL_UNKNOWN_ERROR` and the browser tool timed out.

## Fetch (curl + realistic UA)

```bash
curl -sL --max-time 60 \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" \
  "https://mp.weixin.qq.com/s/<ARTICLE_ID>" -o wx_article.html
```

- No cookies/login needed for public 公众号 articles.
- Save to a file — the page is ~3 MB and you'll re-parse it.
- Do NOT use `head`/`tail` truncation; the body text is deep in the HTML.

## Parse (python3, stdlib only)

```python
import re, html, datetime

raw = open('wx_article.html', encoding='utf-8', errors='ignore').read()

# Title
m = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.S)
title = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()

# Author / account name
m = re.search(r'var nickname = "(.*?)"', raw, re.S)
account = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()

# Publish time: unix timestamp in `var ct`, display as UTC+8
m = re.search(r'var ct = "(\d+)"', raw)
pub = datetime.datetime.fromtimestamp(
    int(m.group(1)), datetime.timezone(datetime.timedelta(hours=8))
).strftime('%Y-%m-%d %H:%M')

# Body: #js_content div, greedy up to the next <script>
m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<script', raw, re.S)
if not m:
    m = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*<script', raw, re.S)
body = m.group(1)

# Block tags -> newlines, then strip remaining tags
body = re.sub(r'<(br|/p|/div|/section|/h\d|/li)[^>]*>', '\n', body)
body = re.sub(r'<[^>]+>', '', body)
body = re.sub(r'\n{3,}', '\n\n', html.unescape(body))
print(title); print(account); print(pub); print(body[:8000])
```

## Field reference

| Metadata | Where in HTML | Notes |
|---|---|---|
| Title | `<h1 ...>...</h1>` | Strip tags + unescape |
| Account | `var nickname = "..."` | The 公众号 name (authenticity check #1) |
| Publish time | `var ct = "<unix_ts>"` | Also check `id="publish_time"` text as backup |
| Body | `<div id="js_content">...</div>` | Falls back to `class="rich_media_content"` |

## After extraction

- The title/account/date are your first authenticity signal (a random "AI
  座谈客" account vs official source changes how much weight the article
  carries).
- Then verify the article's *claims* against primary sources before relaying
  them (official docs / upstream repo), and check them against the user's own
  installed version.
