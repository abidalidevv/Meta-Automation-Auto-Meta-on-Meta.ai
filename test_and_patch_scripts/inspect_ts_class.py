ts_path = r'E:\stickman-video-automation\studio\server\transcription_service.js'
with open(ts_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect where getApiKey and transcribeAudio are
pos = text.find('class TranscriptionService {')
print(text[pos:pos+1500])
