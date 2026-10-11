with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "handleModalCharImage" in l or "handleM1CharFile" in l or "modalCharImageBase64" in l:
        print(f'{i+1}: {l.strip()[:95]}')
