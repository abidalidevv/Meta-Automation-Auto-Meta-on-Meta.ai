app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'mediaGrid|renderMedia|renderAssets|thumbnail|thumb|assetsGrid', text, re.IGNORECASE)]
print('Matches in app_v2.js:', len(matches))
for m in matches[:15]:
    print(text[m-30:m+120].encode('ascii', 'replace').decode('ascii'))
    print('-'*40)
