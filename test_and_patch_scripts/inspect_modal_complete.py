with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="newProjectModal"')
idx2 = text.find('</div>\n    </div>\n  </div>', idx1)
if idx2 == -1:
    idx2 = text.find('<!-- ==================== LIGHTBOX', idx1)
if idx2 == -1:
    idx2 = idx1 + 8000

print(text[idx1:idx2].encode('ascii', 'replace').decode('ascii'))
