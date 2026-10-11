with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Lines 185 to 200 ===')
for i in range(185, min(200, len(lines))):
    print(f'{i+1}: {repr(lines[i])}')

print('=== Lines 1010 to 1025 ===')
for i in range(1010, min(1025, len(lines))):
    print(f'{i+1}: {repr(lines[i])}')
