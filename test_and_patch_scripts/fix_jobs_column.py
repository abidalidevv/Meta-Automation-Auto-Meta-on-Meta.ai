with open(r'E:\stickman-video-automation\studio\server\routes.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = "UPDATE jobs SET status = 'PENDING', error = NULL"
replacement = "UPDATE jobs SET status = 'PENDING', last_error = NULL"

if target in code:
    code = code.replace(target, replacement)
    with open(r'E:\stickman-video-automation\studio\server\routes.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed last_error in jobs table update!")
else:
    print("target not found")
