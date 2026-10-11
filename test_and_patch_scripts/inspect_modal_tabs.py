with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's inspect modal tab buttons and containers in index.html
idx1 = text.find('class="modal-tabs"')
idx2 = text.find('<!-- live audio pacing', idx1) if text.find('<!-- live audio pacing', idx1) != -1 else idx1 + 1000
print(text[idx1:idx1+1200].encode('ascii', 'replace').decode('ascii'))
