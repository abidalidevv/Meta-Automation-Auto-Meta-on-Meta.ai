import re

with open('E:/stickman-video-automation/extensions/veo-automation-with Mbmirza/assets/index.ts-D1zBd6hg.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'case"SCAN_CHARACTERS"', text)
if m:
    print(text[m.start()-50:m.start()+1200])
else:
    print("Not found SCAN_CHARACTERS")
