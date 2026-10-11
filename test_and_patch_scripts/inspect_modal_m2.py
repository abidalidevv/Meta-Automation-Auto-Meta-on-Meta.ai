with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="modalMode2Container"')
print(text[idx:idx+1500].encode('ascii', 'replace').decode('ascii'))
