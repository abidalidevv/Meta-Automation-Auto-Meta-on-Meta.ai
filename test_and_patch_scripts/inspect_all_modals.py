with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="newProjectModal"')
print(text[idx:].encode('ascii', 'replace').decode('ascii'))
