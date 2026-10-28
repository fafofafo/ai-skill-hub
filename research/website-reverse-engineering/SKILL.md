---
name: website-reverse-engineering
description: "Use when 逆向研究网站/API（摸技术栈、找接口、判断鉴权）。WAF+登录墙侦察工作流。"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Reverse-Engineering, WAF, Recon, API, Auth]
    related_skills: [blocked-page-recovery]
---

# 网站逆向侦察（rea逆向）

## When to Use

用户说「rea逆向 <url>」或要求摸清某站技术栈/API/内容是否可获取时触发。目标：给出 架构表 + 关键发现 + 硬障碍评估 + 可行路径，让用户选方向。

## 工作流（按序执行）

1. **web_extract 先看渲染结果** — 常能直接拿到渲染后内容，先建基线。注意：爬虫/SEO 版与真实浏览器版响应可能不同（见 Pitfalls）。
2. **curl -sI + HTML 壳** — 识别技术栈（Vue/React SPA、JS bundle 路径、后端域名）。
3. **探测 WAF** — curl 某个 JS bundle URL：若返回的不是 JS 而是 WAF 拦截页，则站点有 WAF。雷池 SafeLine 特征：HTML 里有 `slg-*` 元素、"安全检测能力由...驱动" 文案。WAF 拦脚本指纹（curl 403），放行真实浏览器 → 之后一切用 browser_exec。
4. **browser_exec 打开页面** — `new_tab` → `wait_for_load` → `performance.getEntriesByType('resource')` 枚举全部请求 URL（JSON stringify → python 解析），定位 API 端点。
5. **读真实响应** — 页面上下文 fetch/XHR 跨域 API 会因无 CORS 头被浏览器拦成空 body；改用 CDP `Network.loadNetworkResource`（先 `Page.getFrameTree` 拿 frameId，options 带 `includeCredentials: true`）走浏览器网络栈，拿真实状态码与响应头。
6. **鉴权判定** — 响应头出现 `vary: Cookie` = 服务端按登录态返回内容（决定性信号）。匿名 200 + 空 body + content-type text/html = 登录墙在服务端，前端改 JS 无法绕过。
7. **登录机制** — 从页面组件/脚本推断：`popup-login-panel`、`jweixin`、`starpass` 等组件名 → 微信扫码/付费订阅体系。
8. **可行性评估 + 固定格式汇报**（见下），由用户定方向后再继续。

## 汇报格式（用户偏好，固定结构）

- **技术架构表**（层/发现，如 前端框架、后端、WAF、核心API）
- **关键发现**（API 端点、鉴权信号、WAF 类型）
- **硬障碍评估**（残酷诚实版：每条路径的代价，不粉饰）
- **建议路径**：A 合法付费 / B 注册免费额度 / C 破解(风险) / D 自产替代
- 结尾让用户选方向，再执行；不擅自走灰色路径

## 风险闸门（用户 SOUL 规则，always-on）

- 绕过付费墙/登录墙取内容 = 灰色操作：首次提出 → 完成侦察 + 如实点明侵权/法律风险（站点有版权声明时尤其）+ 给合法替代，让用户决定。
- 用户三次施压「强制执行」→ 拒绝 + 给合法替代，不执行。
- 用户是提示词/内容卖家：对提示词库类竞品，优先推荐 D「自产替代」（其 pic 系技能可自产同级提示词），而非抓取。

## Pitfalls

- curl 被 WAF 拦（403 + WAF HTML 页）≠ API 不可达；换真实浏览器复测，别下「接口封了」结论。
- JS bundle URL 返回 WAF 页 = 动态 JS 保护；别把 WAF 页当 bundle 内容做静态分析。
- 页面上下文 fetch 跨域 API 返回空 body 是浏览器 CORS 拦截（服务器可能已返回内容）；用 CDP `Network.loadNetworkResource` 或直接导航到 API URL 验证，别误读为「服务器返回空」。
- performance 条目只有 URL 没有响应体；要 body 必须走 CDP。
- `vary: Cookie` 比页面显示什么（404/登录墙/空）更可靠——SPA 匿名时 detail 接口返回空 → 页面渲染「页面不存在」，登录墙组件根本不出现，别以为登录墙不存在。
- SEO/爬虫版与浏览器版响应不同（web_extract 看到登录墙文案、浏览器看到 404）是服务端按客户端分流，不是抓取错误。
- Vue app 内部对象有循环引用，别 JSON.stringify 深层对象（TypeError circular）；只取浅层键。
