with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function switchToolsTab(')
if pos == -1:
    pos = text.find('switchToolsTab')
print(text[pos-50:pos+800].encode('ascii', 'replace').decode('ascii'))
