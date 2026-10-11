with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'resolveMediaUrl', text)]
print('Matches in app_v2.js:', len(matches))
for m in matches:
    print(text[m-20:m+80].encode('ascii', 'replace').decode('ascii'))
