# 小红书删除笔记（patchright 无头流程）

## 定位
- 页面：`https://creator.xiaohongshu.com/new/note-manager`（笔记管理）
- cookie：`~/tools/social-auto-upload/cookies/xiaohongshu_用户测试.json`

## 关键 DOM 结构（2026-09 实测）
- 每篇笔记卡片：`div.note-card`
- 标题元素：`[class*='title']`（`.note-card__title`）
- 操作区（悬停卡片后出现）：`[class*='action-btn--del']` = 删除按钮
- 删除确认弹窗按钮文案：**「确定」**（不是“删除”/“确认”）

## 坑（都踩过）
- ❌ `pg.locator('text="标题"')` 不可靠：同标题渲染多份、选择器不命中 → 用“枚举所有 note-card 读标题文本匹配”
- ❌ 确认按钮先试 `has-text("删除")` 会找不到 → 顺序应为：`确定` → `确认` → `.ant-btn-primary`
- ❌ 脚本异常要打印（except 里 print），否则静默“删了 0 条”没法定位
- hover 卡片本体（不是标题）后再点删除按钮
- 删除后卡片数会变，循环里每次重新 count

## 可复用删除片段（关键逻辑）
```python
cards = pg.locator("div.note-card")
n = await cards.count()
for i in range(n):
    t = (await cards.nth(i).locator("[class*='title']").first.inner_text(timeout=2000)).strip()
    if kw in t:
        target = cards.nth(i); break
await target.hover(); await pg.wait_for_timeout(1500)
await target.locator("[class*='action-btn--del']").first.click(timeout=5000)
await pg.wait_for_timeout(1500)
for sel in ['button:has-text("确定")', '.ant-btn-primary', 'button:has-text("确认")']:
    try:
        await pg.locator(sel).first.click(timeout=2500); break
    except Exception: continue
await pg.wait_for_timeout(3000)
```

## 验证发布状态
打开笔记管理页，抓 `[class*='note-card'] [class*='title']` 的 all_inner_texts 列表即可确认哪些笔记在线。
