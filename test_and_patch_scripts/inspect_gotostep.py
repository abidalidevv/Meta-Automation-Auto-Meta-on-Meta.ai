import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('function goToStep(stepNum)')
print(code[idx:idx+1200])
