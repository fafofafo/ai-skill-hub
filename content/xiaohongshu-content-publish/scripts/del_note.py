#!/usr/bin/env python3
"""删除小红书指定标题的所有笔记（用户测试号）。
用法: python3 del_note.py "标题关键词" ["关键词2" ...]
依赖: ~/tools/social-auto-upload/.venv/bin/python（patchright 环境）
坑: 确认弹窗按钮文案是「确定」；匹配用卡片枚举+inner_text（text= 选择器不可靠）。
"""
import asyncio, sys
from patchright.async_api import async_playwright

ACCOUNT_FILE = "/home/ubuntu/tools/social-auto-upload/cookies/xiaohongshu_用户测试.json"

async def main(keywords):
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(storage_state=ACCOUNT_FILE)
        pg = await ctx.new_page()
        await pg.goto("https://creator.xiaohongshu.com/new/note-manager", timeout=40000)
        await pg.wait_for_timeout(9000)
        for kw in keywords:
            deleted = 0
            for rnd in range(6):
                try:
                    cards = pg.locator("div.note-card")
                    n = await cards.count()
                    target = None
                    for i in range(n):
                        t = (await cards.nth(i).locator("[class*='title']").first.inner_text(timeout=2000)).strip()
                        if kw in t:
                            target = cards.nth(i)
                            break
                    if target is None:
                        break
                    await target.hover()
                    await pg.wait_for_timeout(1500)
                    await target.locator("[class*='action-btn--del']").first.click(timeout=5000)
                    await pg.wait_for_timeout(1500)
                    for sel in ['button:has-text("确定")', '.ant-btn-primary', 'button:has-text("确认")']:
                        try:
                            await pg.locator(sel).first.click(timeout=2500)
                            break
                        except Exception:
                            continue
                    await pg.wait_for_timeout(3000)
                    deleted += 1
                except Exception as e:
                    print(f"第{rnd}轮异常: {str(e)[:100]}")
                    break
            print(f"== [{kw}] 删除 {deleted} 条")
        await b.close()

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
