#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guru 自动找单器：抓任务列表 → 筛选匹配关键词 → 输出候选单子
用法: python3 guru_job_finder.py  （部署到 ~/.hermes/scripts/ 供 cron no_agent 使用）
cron 建议: every 6h, no_agent=true, 有匹配单推送、无匹配静默
"""
import re, subprocess, datetime

KEYWORDS = ["chatbot", "chat bot", "ai agent", "automation", "gpt", "llm",
            "python", "plugin", "integration", "api", "rag", "n8n",
            "developer", "machine learning", "copilot", " ai ", " ai\n", " ai."]
EXCLUDE = ["data collection", "paid", "complaint", "survey", "video editing",
           "receptionist", "writers", "translation", "readers", "lyric"]

def fetch(url):
    try:
        out = subprocess.run(["curl", "-s", "-m", "20", "-A",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", url],
            capture_output=True, text=True)
        return out.stdout
    except Exception:
        return ""

def parse_jobs(html):
    jobs = {}
    for m in re.finditer(r'<a[^>]*href="(/jobs/([^"]+))"[^>]*>([^<]{5,100})</a>', html):
        link, title = m.group(1), m.group(3).strip()
        if title and "/jobs/" in link and title not in jobs:
            jobs[title] = link
    return jobs

def main():
    html = fetch("https://www.guru.com/d/jobs/")
    jobs = parse_jobs(html)
    now = datetime.datetime.now().strftime("%m-%d %H:%M")
    hits = []
    for title, link in jobs.items():
        tl = " " + title.lower() + " "
        # 子串误报：'ai' 会命中 'paid'，靠排除词表过滤
        if any(k in tl for k in KEYWORDS) and not any(x in tl for x in EXCLUDE):
            hits.append((title, link))
    if not hits:
        print(f"[Guru 找单 {now}] 抓取 {len(jobs)} 个任务，暂无匹配 AI/开发 类单子。")
        return
    print(f"\U0001F916【Guru 匹配单子】{now}（共{len(jobs)}单，筛出{len(hits)}个匹配）")
    for t, l in hits[:10]:
        print(f"• {t}")
        print(f"  https://www.guru.com{l.split('&')[0]}")

if __name__ == "__main__":
    main()
