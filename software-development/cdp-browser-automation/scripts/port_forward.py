#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""容器内端口转发：把绑定在 127.0.0.1 的 CDP 端口(9222)转发到 0.0.0.0:9223，
使容器外（宿主/隧道）可访问。容器内跑：nohup python3 port_forward.py &"""
import socket, threading, sys

SRC = ("127.0.0.1", 9222)
DST = ("0.0.0.0", 9223)

def forward(src, dst):
    try:
        while True:
            d = src.recv(65536)
            if not d: break
            dst.sendall(d)
    except Exception:
        pass
    finally:
        try: dst.shutdown(socket.SHUT_WR)
        except Exception: pass

def handle(client):
    try:
        remote = socket.create_connection(SRC)
    except Exception:
        client.close(); return
    threading.Thread(target=forward, args=(client, remote), daemon=True).start()
    threading.Thread(target=forward, args=(remote, client), daemon=True).start()

s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(DST); s.listen(50)
sys.stdout.write(f"listening {DST}\n"); sys.stdout.flush()
while True:
    c, _ = s.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()
