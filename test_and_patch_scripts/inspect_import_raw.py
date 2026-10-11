with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function importRawPrompts')
if pos == -1:
    pos = text.find('importRawPrompts')
print(text[pos-100:pos+1200].encode('ascii', 'replace').decode('ascii'))
