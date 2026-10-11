routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("'/workers/:id/job'")
if pos == -1:
    pos = text.find('"/workers/:id/job"')
if pos == -1:
    pos = text.find('/workers/:id/job')
print('Pos:', pos)
print(text[pos-50:pos+800])
