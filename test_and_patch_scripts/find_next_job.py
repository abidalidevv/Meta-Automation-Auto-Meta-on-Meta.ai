bridge_path = r'c:\Users\Ali\Desktop\meta automation\src\ui\side-panel\bridge-client.js'
with open(bridge_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'/next-job', text)]
for m in matches:
    print(text[m-200:m+400])
    print('='*50)
