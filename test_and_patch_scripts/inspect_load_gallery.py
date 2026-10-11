with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('async function loadProjectGallery()')
if idx == -1:
    idx = text.find('loadProjectGallery')
print(text[idx:idx+2500].encode('ascii', 'replace').decode('ascii'))
