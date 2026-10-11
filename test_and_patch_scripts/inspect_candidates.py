with open(r'E:\stickman-video-automation\studio\server\worker_orchestrator.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('// 1. Physical existence verification across candidate directories')
print(text[pos:pos+2000])
