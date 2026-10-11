with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'id="step-2-panel"', text)]
print("Matches for id=step-2-panel:", matches)
if len(matches) > 1:
    print("Match 1 snippet:")
    print(text[matches[0]:matches[0]+200].encode('ascii', 'replace').decode('ascii'))
    print("Match 2 snippet:")
    print(text[matches[1]:matches[1]+200].encode('ascii', 'replace').decode('ascii'))
