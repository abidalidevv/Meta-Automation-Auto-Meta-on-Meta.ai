import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('subTabMode1')
print(code[idx-100:idx+800])
