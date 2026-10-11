app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('if (stepNum === 4)')
print('Found stepNum === 4 at:', pos)
if pos != -1:
    print(text[pos-100:pos+300].encode('ascii', 'replace').decode('ascii'))
else:
    pos2 = text.find('function goToStep(')
    print(text[pos2:pos2+1000].encode('ascii', 'replace').decode('ascii'))
