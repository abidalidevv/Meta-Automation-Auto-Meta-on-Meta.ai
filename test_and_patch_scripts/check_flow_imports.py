flow_ext = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\index.ts-D1zBd6hg.js'
with open(flow_ext, 'r', encoding='utf-8') as f:
    text = f.read()

print('Imports at top of file:')
print(text[:1500])
