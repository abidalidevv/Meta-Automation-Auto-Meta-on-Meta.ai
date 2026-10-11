wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('// 2. High-Priority Repair Queue check')
print(text[pos:pos+600])
