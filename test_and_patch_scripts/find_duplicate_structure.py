with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<section id=[\'"]step-1-panel[\'"]', text)]
print('step-1-panel matches:', matches)

matches_main = [m.start() for m in re.finditer(r'<main class=[\'"]main-container[\'"]', text)]
print('main-container matches:', matches_main)
