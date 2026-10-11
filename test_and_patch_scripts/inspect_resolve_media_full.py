app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function resolveMediaUrl(')
print(text[pos:pos+700].encode('ascii', 'replace').decode('ascii'))
