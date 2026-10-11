with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="newProjectModal"')
idx_end = text.find('id="mainStepper"')
if idx_end == -1:
    idx_end = idx + 4000
print(text[idx:idx_end][:4000].encode('ascii', 'replace').decode('ascii'))
