with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "async function submitNewProject" in l:
        for j in range(i, min(len(lines), i + 60)):
            clean = lines[j].strip()[:95].encode('ascii', 'replace').decode('ascii')
            print(f'{j+1}: {clean}')
        break
