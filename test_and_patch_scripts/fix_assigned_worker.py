with open(r'E:\stickman-video-automation\studio\server\routes.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = "UPDATE prompts SET status = 'PENDING', worker_id = NULL, error = NULL"
replacement = "UPDATE prompts SET status = 'QUEUED', assigned_worker_id = NULL"

if target in code:
    code = code.replace(target, replacement)
    with open(r'E:\stickman-video-automation\studio\server\routes.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed assigned_worker_id column!")
else:
    print("Target not found directly, checking...")
