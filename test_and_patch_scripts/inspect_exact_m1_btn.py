index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('onclick="importRawPrompts()"')
print(repr(text[pos-100:pos+150]))
