pm_path = r'E:\stickman-video-automation\studio\server\profile_manager.js'
with open(pm_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('launchWorker(workerId, provider)')
print(text[pos:pos+1500])
