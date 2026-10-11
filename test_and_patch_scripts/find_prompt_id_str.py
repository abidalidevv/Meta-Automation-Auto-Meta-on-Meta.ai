import os, re

server_dir = r'E:\stickman-video-automation\studio\server'
for f in os.listdir(server_dir):
    if f.endswith('.js'):
        p = os.path.join(server_dir, f)
        with open(p, 'r', encoding='utf-8') as fp:
            c = fp.read()
            if 'prompt_id_str' in c:
                for m in re.finditer(r'job_[^\'\`"]*prompt_id_str', c):
                    print(f"{f}: found {m.group(0)}")
