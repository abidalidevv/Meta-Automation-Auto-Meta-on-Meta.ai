wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[220:330], start=221):
    print(f"{i}: {line}", end='')
