wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('// 4. Fallback: Unassigned prompt check')
print(text[pos:pos+2500])
