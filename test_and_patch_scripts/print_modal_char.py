with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for j in range(1615, min(len(lines), 1675)):
    print(f'{j+1}: {lines[j].strip()[:95]}')
