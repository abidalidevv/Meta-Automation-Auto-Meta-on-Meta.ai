import sys
sys.stdout.reconfigure(encoding='utf-8')

app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('async function refreshFleetStatus() {')
print(code[idx:idx+1500])
