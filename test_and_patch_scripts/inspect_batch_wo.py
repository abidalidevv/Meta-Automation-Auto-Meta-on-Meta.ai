wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('batchQuery')
print('pos of batchQuery:', pos)
if pos != -1:
    print(text[pos-100:pos+1500])
else:
    pos2 = text.find('// 3. Worker-assigned prompt check')
    print('pos2:', pos2)
    print(text[pos2-100:pos2+1500])
