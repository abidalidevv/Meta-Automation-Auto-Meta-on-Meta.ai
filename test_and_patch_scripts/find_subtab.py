import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'switchStep1SubTab' in l:
        print(f'{i+1}: {l.strip()}')
        for j in range(i, min(i+35, len(lines))):
            print(f'  {j+1}: {lines[j].strip()}')
        break
