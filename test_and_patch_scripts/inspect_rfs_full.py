import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('async function refreshFleetStatus() {')
idx2 = code.find('async function toggleWorkerProvider', idx)
print(code[idx:idx2])
