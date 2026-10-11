import re

with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find subViewMode2 differently
idx1 = text.find('"subViewMode2"')
idx2 = text.find('"subViewPromptsQueue"')

subview_text = text[idx1:idx2]

print('subViewMode2 length:', len(subview_text))
print(subview_text[:200].encode('ascii', 'replace').decode('ascii'))

# Get all onclick handlers
buttons = re.findall(r'onclick="([^"]+)"', subview_text)
print('\nButtons in Step 1 subViewMode2 (Groq AI tab):')
for b in buttons[:25]:
    print(' -', b.encode('ascii', 'replace').decode('ascii'))
