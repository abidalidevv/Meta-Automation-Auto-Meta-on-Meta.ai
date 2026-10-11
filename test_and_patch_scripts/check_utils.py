utils_path = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\utils-D8jN6fhl.js'
with open(utils_path, 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of utils:', len(text))
pos = 0
while True:
    pos = text.find('export', pos)
    if pos == -1:
        break
    print(text[pos:pos+300])
    pos += 1
