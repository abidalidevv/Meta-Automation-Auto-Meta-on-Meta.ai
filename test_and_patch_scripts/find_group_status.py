with open(r'c:\Users\Ali\Desktop\meta automation\assets\index.ts-BdeTBz9V.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'PROMPT_GROUP_STATUS', text)]
for m in matches:
    print(text[m-50:m+300])
