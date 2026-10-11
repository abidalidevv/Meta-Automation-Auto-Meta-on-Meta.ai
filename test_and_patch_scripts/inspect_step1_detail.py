with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

step1_idx = text.find('id="step1View"')
if step1_idx != -1:
    step1_snippet = text[step1_idx:step1_idx+5000]
    for line in step1_snippet.splitlines()[:120]:
        print(line[:120].encode('ascii', 'replace').decode('ascii'))
