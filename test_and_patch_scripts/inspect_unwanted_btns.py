with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'Start Generating Now|Open Worker Farm', text, re.IGNORECASE)]
for i, m in enumerate(matches):
    print(f"=== MATCH {i+1} at {m} ===")
    print(text[max(0, m-150):min(len(text), m+250)].encode('ascii', 'replace').decode('ascii'))
