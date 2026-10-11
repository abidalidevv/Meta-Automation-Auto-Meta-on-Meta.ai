with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('newProjectModal')
print("Position:", idx)
if idx != -1:
    print(text[idx-50:idx+600].encode('ascii', 'replace').decode('ascii'))
