with open(r'E:\stickman-video-automation\studio\server\project_manager.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "getProject(" in l or "createProject(" in l or "character" in l:
        print(f'{i+1}: {l.strip()[:95]}')
