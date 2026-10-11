utils_path = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\utils-D8jN6fhl.js'
with open(utils_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
sub = text[-20000:]
matches = [m.start() for m in re.finditer(r'([a-zA-Z0-9_$]+)?\s*E\s*([=:(,])', sub)]
for m in matches:
    print(sub[m-20:m+80])
