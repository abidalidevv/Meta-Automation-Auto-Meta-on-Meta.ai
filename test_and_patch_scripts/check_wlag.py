with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('workersLoginAssistantGrid')
print('workersLoginAssistantGrid at index:', idx)
if idx != -1:
    print(code[idx-50:idx+200])
