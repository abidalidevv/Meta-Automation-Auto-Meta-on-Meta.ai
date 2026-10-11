with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="lightboxModal"')
print("Position:", idx)
if idx != -1:
    print(text[idx-50:idx+250].encode('ascii', 'replace').decode('ascii'))
