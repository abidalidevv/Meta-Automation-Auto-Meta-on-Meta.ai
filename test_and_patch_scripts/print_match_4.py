flow_ext = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\index.ts-D1zBd6hg.js'
with open(flow_ext, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('c([["mode",t.mode],["aspectRatio",t.aspectRatio],["model', 2500)
print('Pos:', pos)
print(text[pos-100:pos+500])
