wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'job_\$\{Date\.now\(\)\}', text)]
print('Matches:', len(matches))
for m in matches:
    print(text[m-50:m+200])
    print('='*50)
