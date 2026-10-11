with open(r'E:\stickman-video-automation\studio\server\ingestion_manager.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('downloadsDir')
print(text[pos-50:pos+500])
