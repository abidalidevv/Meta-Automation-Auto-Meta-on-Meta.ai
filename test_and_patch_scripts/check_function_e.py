utils_path = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\utils-D8jN6fhl.js'
with open(utils_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.rfind('function E(')
if pos == -1:
    pos = text.rfind('E=')
print('Pos of E:', pos)
print(text[pos-100:pos+800])
