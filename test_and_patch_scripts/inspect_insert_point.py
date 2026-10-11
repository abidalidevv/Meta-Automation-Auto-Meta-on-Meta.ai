with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx1 = text.find('id="m2ForecastCard"')
idx2 = text.find('id="rawPromptsInput"')
print(text[idx1:idx2].encode('ascii', 'replace').decode('ascii'))
