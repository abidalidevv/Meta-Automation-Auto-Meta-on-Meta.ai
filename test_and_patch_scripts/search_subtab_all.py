with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'switchStep1SubTab' in l:
        print(f"Line {i+1}: {l.strip()}")
