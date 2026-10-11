import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('class="stepper-tab"')
idx2 = code.find('</nav>', idx)
print(code[idx:idx2])
