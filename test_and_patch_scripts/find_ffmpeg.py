re_path = r'E:\stickman-video-automation\studio\server\render_engine.js'
with open(re_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'ffmpeg', text, re.IGNORECASE)]
print('Matches in render_engine.js:', len(matches))
for m in matches[:10]:
    print(text[m-20:m+120])
    print('-'*30)
