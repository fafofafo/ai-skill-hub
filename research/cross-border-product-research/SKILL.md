---
name: cross-border-product-research
description: Use when 跨境电商选品/供应商调研（Amazon、1688、Alibaba、Google Trends）。
version: 1.0.0
---

# 跨境电商选品调研通道（2026-10 实测）

## 数据通道可用性（腾讯云数据中心 IP 实测）
- **Amazon Best Sellers**：七牛云代理可抓（无验证码），选品榜单数据 ✅
- **Google Trends**：本机直连被墙；**七牛云 + pytrends** 可跑（pytrends 装 /root/gt-venv，**必须降级 urllib3<2**，否则 Retry.__init__() method_whitelist 报错）
- **1688**：云 IP 全拒（bixi.alicdn.com punish 页，cloud_ip_bl 黑名单），curl/playwright/七牛云都过不去 → **需用户本机（住宅 IP）操作**
- **Alibaba 国际站**：搜索页弹滑块 CAPTCHA（云 IP），但**商品详情页 web_extract 可直接抓**（含价格/MOQ/样品价/销量/店铺评分/响应时间）→ 用 web_search 拿详情页链接再 web_extract
- **web_search/web_extract 后端不稳**：会随机超时/换后端（Exa/Parallel/Keenable），失败重试即可

## Google Trends 季节验证
- 逐词单查拿季节形态（组内归一化会压制小词，绝对量不可比但形态可比）
- 周粒度数据：tail(12) 是 12 周不是 12 个月，年度对比要按年份聚合（yearly mean）
- 关键判据：峰值月 + 淡季基线 + 1月缓冲（如圣诞品 1 月=12 月的 60% → 弱季节化成立）

## 供应商清单要点
- Alibaba 详情页数据比 1688 更贴合出口场景（FOB/MOQ/样品价）；拿样/小批量走 1688（国内 MOQ 低）
- 注意 alibaba MOQ 常 500-1500（出口整柜逻辑），与"小批量快反 100-200 件"冲突 → 小批量必须走 1688 或找低 MOQ 供应商
- 询价模板必备 6 问：重量/包装尺寸（FBA 1lb 分界）、无标版、MOQ+样品、小批量交期、CE/REACH 报告、专利自查截图

## 黑五时间窗
- 黑五 = 11 月第 4 个周五（2026-11-27）；行业备货节奏 = 9 月完成；空运 7-10 天 → 10/15 前下单仍可赶上
- 已晚于行业节奏时：小批量快反（1-2 SKU × 100-200 件空运试水）替代大批量备货

## 专利初查（低成本）
- Google Patents + 判例库（courtlistener）web 搜即可做初步风险判断，正式下单前对供应商实拍图复核
- 例：ChomChom 核心 US 8,117,706 覆盖滚筒结构，静电手套不落入；权利人打假激进（移除 320+ listing）
