with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx_btn = text.find('id="btnM1StartGenerating"')
idx_modal = text.find('id="newProjectModal"')
idx_lightbox = text.find('id="lightboxModal"')

print(f"btnM1StartGenerating at: {idx_btn}")
print(f"newProjectModal at: {idx_modal}")
print(f"lightboxModal at: {idx_lightbox}")

print("\nAround btnM1StartGenerating (2000 chars):")
print(text[idx_btn-200:idx_btn+1500].encode('ascii', 'replace').decode('ascii'))
