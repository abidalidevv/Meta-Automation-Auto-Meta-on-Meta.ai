with open(r'E:\stickman-video-automation\studio\server\worker_orchestrator.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('// 3. Physical binary sign')
if pos == -1:
    pos = text.find('actualFilePath = found')
print(text[pos:pos+1500])
