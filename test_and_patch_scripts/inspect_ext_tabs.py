with open(r'c:\Users\Ali\Desktop\meta automation\assets\index.html-Cb5LKqTn.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
# find tabs or navigation in extension
tabs = re.findall(r'value:"([a-zA-Z0-9_-]+)",label:[^}]+', text)
print("Tabs found:", set(tabs[:20]))

# Also search for 'random' or placeholder image
matches = [m.start() for m in re.finditer(r'placeholder|thumbnail|gallery', text, re.I)]
print("Placeholder / thumbnail matches:", len(matches))
for m in matches[:5]:
    print(text[m-30:m+100].encode('ascii', 'replace').decode('ascii'))
