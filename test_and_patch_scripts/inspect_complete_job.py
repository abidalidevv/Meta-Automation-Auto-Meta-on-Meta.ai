with open(r'E:\stickman-video-automation\studio\server\worker_orchestrator.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async completeJob(')
if pos == -1:
    pos = text.find('completeJob')
print("=== completeJob in worker_orchestrator.js ===")
print(text[pos:pos+1500])
