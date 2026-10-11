with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('onclick="importRawPrompts()"')
print(text[pos-100:pos+300].encode('ascii', 'replace').decode('ascii'))
