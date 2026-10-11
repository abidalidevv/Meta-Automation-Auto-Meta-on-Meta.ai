ts_path = r'E:\stickman-video-automation\studio\server\transcription_service.js'
with open(ts_path, 'r', encoding='utf-8') as f:
    text = f.read()

print(text[:2000])
print("="*50)
print(text[-2000:])
