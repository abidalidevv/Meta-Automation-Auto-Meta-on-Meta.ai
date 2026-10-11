ts_path = r'E:\stickman-video-automation\studio\server\transcription_service.js'
with open(ts_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async transcribeAudio')
print(text[pos:pos+2000])
