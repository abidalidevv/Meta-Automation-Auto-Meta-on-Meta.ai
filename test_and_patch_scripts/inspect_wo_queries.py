wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('// 3. Worker-assigned prompt check')
print(text[pos-200:pos+1200])
