routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'orchestrator', text)]
for m in matches[:5]:
    print(text[m-20:m+100])
