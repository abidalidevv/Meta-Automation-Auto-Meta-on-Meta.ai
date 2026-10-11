with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
modal_start = text.find('id="newProjectModal"')
modal_end = text.find('<!--', modal_start + 10)
print('Modal excerpt (first 2500 chars):')
print(text[modal_start:modal_start+2500])
