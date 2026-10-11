wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'INSERT INTO jobs', text)]
print('Matches for INSERT INTO jobs:', len(matches))
for m in matches:
    print(text[m-20:m+250])
    print('='*50)
