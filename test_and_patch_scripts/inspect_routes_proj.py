with open(r'E:\stickman-video-automation\studio\server\routes.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "router.get('/projects/:id'" in l or "router.get('/projects/:id'," in l:
        for j in range(i, min(len(lines), i + 45)):
            print(f'{j+1}: {lines[j].strip()[:95]}')
        break
