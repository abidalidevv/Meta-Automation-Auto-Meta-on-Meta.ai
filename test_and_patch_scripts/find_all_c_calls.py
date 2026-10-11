flow_ext = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\index.ts-D1zBd6hg.js'
with open(flow_ext, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'c\(\[\[', text)]
for m in matches:
    print(text[m:m+150])
    print('-'*40)
