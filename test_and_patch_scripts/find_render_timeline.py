app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'renderTimeline|renderScenes|sceneCard|playerCanvasImage', text)]
print('Matches in app_v2.js:', len(matches))
for m in matches[:10]:
    print(text[m-20:m+250].encode('ascii', 'replace').decode('ascii'))
    print('='*50)
