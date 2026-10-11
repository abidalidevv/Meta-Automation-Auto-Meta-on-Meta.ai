import os, re

for folder in [r'E:\stickman-video-automation\studio\server', r'c:\Users\Ali\Desktop\meta automation']:
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith('.js'):
                p = os.path.join(root, f)
                try:
                    with open(p, 'r', encoding='utf-8') as fp:
                        c = fp.read()
                        if 'job_${Date.now()}' in c or 'job_${Date.now()}_' in c or '_${nextPrompt' in c or '_${repairPrompt' in c:
                            print(f"MATCH: {p}")
                except:
                    pass
