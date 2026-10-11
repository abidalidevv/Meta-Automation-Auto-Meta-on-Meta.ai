with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1005, min(1045, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')
