with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function goToStep(')
if pos == -1:
    pos = text.find('function switchStep(')
print(text[pos-50:pos+800].encode('ascii', 'replace').decode('ascii'))
