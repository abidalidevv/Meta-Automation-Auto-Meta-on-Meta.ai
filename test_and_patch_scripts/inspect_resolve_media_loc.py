with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function resolveMediaUrl')
print(text[pos:pos+400].encode('ascii', 'replace').decode('ascii'))
