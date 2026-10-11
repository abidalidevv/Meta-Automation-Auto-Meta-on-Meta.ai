story_engine_path = r'E:\stickman-video-automation\studio\server\ai_story_engine.js'
with open(story_engine_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'groq|apiKey|api_key', text, re.IGNORECASE)]
print('Matches in ai_story_engine:', len(matches))
for m in matches[:10]:
    print(text[m-20:m+120])
    print('-'*30)
