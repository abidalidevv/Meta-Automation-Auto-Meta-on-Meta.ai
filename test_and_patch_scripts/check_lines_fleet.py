import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line_num in [2180, 3110]:
    start = max(0, line_num - 15)
    end = min(len(lines), line_num + 15)
    print(f'=== Around line {line_num} ===')
    for j in range(start, end):
        print(f'{j+1}: {lines[j].strip()}')
