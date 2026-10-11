import os

flow_ext = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\index.ts-D1zBd6hg.js'
with open(flow_ext, 'r', encoding='utf-8') as f:
    text = f.read()

pos = 0
while True:
    pos = text.find('aspectRatio', pos)
    if pos == -1:
        break
    print(f"--- Found aspectRatio at {pos} ---")
    print(text[max(0, pos-150):min(len(text), pos+300)])
    pos += 1
    if pos > 300000:
        break
