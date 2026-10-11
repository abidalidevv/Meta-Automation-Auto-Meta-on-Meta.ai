utils_path = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\utils-D8jN6fhl.js'
with open(utils_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'(?:const|let|var|function)\s+E\s*=', text)]
print('Matches for E =:', matches)
for m in matches:
    print(text[m:m+400])
