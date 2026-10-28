#!/usr/bin/env python3
"""小红书创作平台诊断探针（social-auto-publish skill 配套）。

用法:
  python3 xhs_diag.py <cookies.json路径> [account名]

作用: 用已存 cookie 打开小红书创作平台发布页，dump 页面 body 文本 + file input 数 + 按钮列表。
判定: 看 body 文本里有没有「绑定手机号」横幅（未绑定=不能发布）、当前上传模式、可点按钮。
依赖: patchright（social-auto-upload 的 .venv 内已装）。
"""
import asyncio, sys
from patchright.async_api import async_playwright

COOKIE = sys.argv[1] if len(sys.argv) > 1 else "cookies/xiaohongshu_用户测试.json"
URL = "https://creator.xiaohongshu.com/publish/publish?source=official"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(storage_state=COOKIE)
        pg = await ctx.new_page()
        await pg.goto(URL, timeout=40000)
        await pg.wait_for_timeout(4000)
        print("URL:", pg.url[:100])
        txt = await pg.locator("body").inner_text()
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        print("=== 页面文本(前50行) ===")
        print("\n".join(lines[:50]))
        print("\n=== 关键检测 ===")
        if "绑定手机号" in txt:
            print("⚠️ 检测到「未绑定手机号」横幅 → 该账号不能发布，需 APP 端绑定手机号")
        else:
            print("✅ 未见手机号限制横幅")
        print("file input 数量:", await pg.locator("input[type=file]").count())
        btns = await pg.locator("button").all_text_contents()
        print("按钮:", [x.strip()[:20] for x in btns if x.strip()][:12])
        await b.close()

asyncio.run(main())
