with open(r'E:\stickman-video-automation\studio\server\ingestion_manager.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async ingestFileForPrompt')
print(text[pos:pos+1500])
