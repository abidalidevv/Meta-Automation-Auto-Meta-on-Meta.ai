story_engine_path = r'E:\stickman-video-automation\studio\server\ai_story_engine.js'
with open(story_engine_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async getApiKeyPool()')
print(text[pos:pos+1200])
