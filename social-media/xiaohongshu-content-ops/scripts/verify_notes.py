#!/usr/bin/env python3
"""验证小红书笔记已上线：打开笔记管理页抓取在线笔记标题。

用法: cd ~/tools/social-auto-upload && .venv/bin/python verify_notes.py
(2026-09-08 实测可用; patchright 在 social-auto-upload 的 venv 里)
"""
from patchright.sync_api import sync_playwright

STATE = '/home/ubuntu/tools/social-auto-upload/cookies/xiaohongshu_用户测试.json'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # cookie 是 playwright storage_state 格式 {cookies:[...], origins:[...]}，直接加载
    ctx = browser.new_context(storage_state=STATE)
    page = ctx.new_page()
    try:
        page.goto('https://creator.xiaohongshu.com/new/note-manager', timeout=60000)
        page.wait_for_timeout(9000)
        try:
            page.locator("div.note-card").first.wait_for(timeout=15000)
        except Exception:
            print("未找到 note-card（可能未登录或页面未加载）")
        cards = page.locator("div.note-card")
        print(f"在线笔记数: {cards.count()}")
        for t in cards.locator("[class*='title']").all_inner_texts():
            print("-", t.strip()[:70])
    except Exception as e:
        print(f"脚本异常: {e}")
    finally:
        browser.close()
