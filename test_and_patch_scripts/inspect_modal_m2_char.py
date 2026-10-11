with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Check what's in modal Mode 2 around the char section
idx = text.find('newProjCharNameM2')
print(text[idx-200:idx+600].encode('ascii', 'replace').decode('ascii'))
