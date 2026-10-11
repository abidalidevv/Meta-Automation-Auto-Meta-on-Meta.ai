with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m1_start = text.find('id="modalMode1Container"')
m2_start = text.find('id="modalMode2Container"')
print(text[m1_start:m2_start].encode('ascii', 'replace').decode('ascii'))
