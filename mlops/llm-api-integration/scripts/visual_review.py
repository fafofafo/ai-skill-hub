#!/usr/bin/env python3
"""图片视觉复核（硅基流动 Qwen3-VL-32B）。

内置 vision_analyze 工具底层走火山 doubao，常见 404（UnsupportedModel）——
图片/海报分析直接用本脚本，别在 vision_analyze 上耗时间。

用法:
  python3 visual_review.py <图片路径> ["自定义问题"]
  默认问题覆盖 pic 系列复核 6 项：人物外观/画风/背景/色调/FAFO标注/乱码。
"""
import base64, json, sys, urllib.request

# key 从 backup.env 读（SILICONFLOW_API_KEY），勿硬编码
KEY = None
for line in open('/home/ubuntu/.hermes/agent-memory-data/backup.env', encoding='utf-8'):
    if line.startswith('SILICONFLOW_API_KEY='):
        KEY = line.split('=', 1)[1].strip()
        break
if not KEY:
    sys.exit('SILICONFLOW_API_KEY not found in backup.env')

img_path = sys.argv[1]
question = (sys.argv[2] if len(sys.argv) > 2 else (
    '详细描述这张图：1) 人物外观（发型发色、服饰颜色）2) 画风（3D渲染还是插画？逆光？）'
    '3) 背景 4) 色调（饱和度、曝光）5) 是否有「FAFO工作室」文字标注（位置、清晰度）'
    '6) 有无乱码文字'))

img_b64 = base64.b64encode(open(img_path, 'rb').read()).decode()
req = urllib.request.Request(
    'https://api.siliconflow.cn/v1/chat/completions',
    method='POST',
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {KEY}'},
    data=json.dumps({
        'model': 'Qwen/Qwen3-VL-32B-Instruct',
        'messages': [{'role': 'user', 'content': [
            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{img_b64}'}},
            {'type': 'text', 'text': question},
        ]}],
    }).encode(),
)
# 大图/长 prompt 偶发读超时：重试一次，timeout 设 150-200s
for attempt in range(2):
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=200))
        break
    except Exception as e:
        if attempt == 0:
            continue
        sys.exit(f'调用失败: {e}')
print(resp['choices'][0]['message']['content'])
