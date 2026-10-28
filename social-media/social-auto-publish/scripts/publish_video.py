#!/usr/bin/env python3
"""小红书发视频一键封装（sau 后台 + 日志轮询 + 成功判定）。

用法:
  python publish_video.py --account 用户测试 --file /path/v.mp4 \
      --title "标题" --desc "正文" --tags "tag1,tag2" --thumbnail /path/cover.jpg

行为: 清 PYTHONPATH（execute_code 内核污染）→ 后台起 sau xiaohongshu upload-video
→ 轮询日志（默认 300s）→ 打印成功/失败判定。cwd 自动切到 ~/tools/social-auto-upload。
"""
import argparse
import os
import subprocess
import sys
import time

SAU_DIR = os.path.expanduser("~/tools/social-auto-upload")
SAU = os.path.join(SAU_DIR, ".venv/bin/sau")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--account", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", default="")
    ap.add_argument("--tags", default="")
    ap.add_argument("--thumbnail", default="")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--log", default="publish.log")
    args = ap.parse_args()

    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    cmd = [SAU, "xiaohongshu", "upload-video",
           "--account", args.account,
           "--file", args.file,
           "--title", args.title]
    if args.desc:
        cmd += ["--desc", args.desc]
    if args.tags:
        cmd += ["--tags", args.tags]
    if args.thumbnail:
        cmd += ["--thumbnail", args.thumbnail]

    log_path = os.path.join(SAU_DIR, args.log)
    with open(log_path, "w") as logf:
        p = subprocess.Popen(cmd, cwd=SAU_DIR, env=env, stdout=logf,
                             stderr=subprocess.STDOUT, start_new_session=True)
    print(f"PID {p.pid} 日志 {log_path}")

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        time.sleep(5)
        rc = p.poll()
        if rc is not None:
            break
    rc = p.poll()
    with open(log_path) as f:
        log = f.read()
    if rc == 0 and "视频发布成功" in log:
        print("SUCCESS: 视频发布成功")
        print(log[-2000:])
        return 0
    print(f"FAIL rc={rc} —— 看日志尾部：")
    print(log[-3000:])
    return 1


if __name__ == "__main__":
    sys.exit(main())
