# RunningHub 接口逆向（从 SPA JS chunk）

## 场景
网页功能在已发现的 API 里找不到对应端点时，从前端 JS 挖真实请求路径和请求体字段。

## 步骤
1. 抓页面 HTML（curl 或七牛云中转），取 `/_nuxt/*.js` 主 chunk 名：`grep -o 'src="[^"]*\.js[^"]*"' page.html`。
2. 抓主 chunk + 目标页面组件 chunk。路由表在主 chunk：`{path:"/xxx",name:"...",component:()=>import("./XXXX.js")}` → 按页面路径找到对应组件 chunk 名。
3. 本地 grep 真实 API 路径：`grep -oE '"/api/[a-zA-Z0-9/_.-]*"' chunk.js | sort -u`。
4. 找请求构造：grep `post("/api/..."` 附近的代码拿 body 字段名（例如 skuList 请求体是 `{categoryType, tagIds:[], search:"", ...}`——字段名常与直觉不同）。
5. 组件间关系：页面组件 import 的 store/工具 chunk 里才有真正的请求函数，主 chunk 通常只有 API 定义（`xxxRes:function(e){return t.post("/api/xxx",e)}`）；跟着 import 链找发起调用的组件，再找它构造的 body。

## 坑
- 大 chunk 用 `ssh 'cat file' > local` 回传会截断（管道半途断开）——直接在远程 grep，或分片拉取；主 chunk 常 2-3MB。
- 请求字段名常与直觉不同：市场搜索是 `search` 不是 `keyword`；分页是 `pageNo/pageSize`；页面组件有默认 query 结构（isWhitelist/isSelf/isThirdParty 等布尔），缺了可能搜索失效。
- SPA 返回的 HTML 不含数据（Nuxt 客户端渲染），别在 HTML 里找结果，找 XHR 端点。
- 前端路由 `/xxx`、`/call-api/...` 是页面路由不是 API；真正的接口在 `/api/...`。
- 分页接口常有 bug（pageNo 被忽略、永远同页）——翻页前先验证 total 是否变化。
