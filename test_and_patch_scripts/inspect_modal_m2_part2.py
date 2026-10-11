with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

modal_start = text.find('newProjScriptFileM2')
print(text[modal_start:modal_start+2500].encode('ascii', 'replace').decode('ascii'))
