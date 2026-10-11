routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'router\.get\([\'"`][^\'"`]*(?:image|media|file|asset|thumb|download)', text, re.IGNORECASE)]
print('Matches in routes.js:', len(matches))
for m in matches:
    print(text[m:m+120])
