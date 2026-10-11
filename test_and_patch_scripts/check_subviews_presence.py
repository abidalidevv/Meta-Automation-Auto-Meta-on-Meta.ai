import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    code = f.read()

for sid in ['subTabMode1', 'subTabMode2', 'subTabPromptsQueue', 'subViewMode1', 'subViewMode2', 'subViewQueue']:
    print(f'{sid}: {"FOUND" if sid in code else "NOT FOUND"}')
