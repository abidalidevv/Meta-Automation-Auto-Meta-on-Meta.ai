with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()[:158865]

idx1 = text.find('id="subViewMode1"')
idx2 = text.find('id="subViewMode2"')
print("=== SUBVIEW MODE 1 ===")
print(text[idx1:idx2].encode('ascii', 'replace').decode('ascii'))
