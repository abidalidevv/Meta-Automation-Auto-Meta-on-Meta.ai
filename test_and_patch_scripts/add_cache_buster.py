index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('<script src="/app_v2.js">', '<script src="/app_v2.js?v=2.2">')
code = code.replace('<link rel="stylesheet" href="/styles_v2.css">', '<link rel="stylesheet" href="/styles_v2.css?v=2.2">')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('Added cache buster v=2.2 to index.html!')
