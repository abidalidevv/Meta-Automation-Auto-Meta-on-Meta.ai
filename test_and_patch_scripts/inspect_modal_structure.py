with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx1 = text.find('id="newProjectModal"')
idx2 = text.find('class="main-container"')
print(text[idx1:idx2][:3000].encode('ascii', 'replace').decode('ascii'))
