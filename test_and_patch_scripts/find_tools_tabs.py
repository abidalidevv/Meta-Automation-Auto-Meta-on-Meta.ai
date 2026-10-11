with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer(r'class=[\'"][^\'"]*tools-tab[^\'"]*[\'"]', html)]
print('Matches:', len(matches))
for m in matches:
    print(html[m-20:m+200].encode('ascii', 'replace').decode('ascii'))
    print('='*50)
