#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CDP 控制客户端：导航 + 执行 JS。
用法:
  python cdp_op.py --navigate <url>     # 打开页面，返回 标题||URL||正文前400字符
  python cdp_op.py --js '<js code>'     # 执行 JS，返回其值（returnByValue）
依赖: websocket-client  (uv pip install --python <venv>/bin/python websocket-client)
前提: 本机已建隧道到远程 chromium 的 CDP 端口（见 cdp-browser-automation 技能）。
"""
import sys, json, time, urllib.request
import websocket

CDP = "http://localhost:9222"  # 经隧道映射到远程容器的 CDP 端口

def get_page_ws():
    with urllib.request.urlopen(f"{CDP}/json/list", timeout=10) as r:
        tabs = json.load(r)
    for t in tabs:
        if t.get("type") == "page":
            return t.get("webSocketDebuggerUrl")
    return None

def main():
    ws_url = get_page_ws()
    if not ws_url:
        print("NO_PAGE_TAB"); return
    ws = websocket.create_connection(ws_url, timeout=30)
    counter = [0]
    def send(method, params=None):
        counter[0] += 1
        cid = counter[0]
        ws.send(json.dumps({"id": cid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == cid:
                return msg
    if sys.argv[1] == "--navigate":
        send("Page.navigate", {"url": sys.argv[2]})
        time.sleep(8)
        r = send("Runtime.evaluate", {
            "expression": "document.title+'||'+location.href+'||'+(document.body?document.body.innerText.slice(0,400):'')",
            "returnByValue": True})
        print(r.get("result", {}).get("result", {}).get("value", "EMPTY"))
    elif sys.argv[1] == "--js":
        r = send("Runtime.evaluate", {"expression": sys.argv[2], "returnByValue": True})
        print(r.get("result", {}).get("result", {}).get("value", "EMPTY"))
    ws.close()

if __name__ == "__main__":
    main()
