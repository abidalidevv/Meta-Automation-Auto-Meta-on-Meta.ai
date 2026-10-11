ts_path = r'E:\stickman-video-automation\studio\server\transcription_service.js'
with open(ts_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the entire file to see how it's structured
print("Length of file:", len(text))
