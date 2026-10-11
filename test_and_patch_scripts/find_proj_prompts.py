with open(r'E:\stickman-video-automation\studio\server\routes.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("router.get('/projects/:id/prompts'")
print('Pos:', pos)
if pos != -1:
    print(text[pos:pos+600].encode('ascii', 'replace').decode('ascii'))
