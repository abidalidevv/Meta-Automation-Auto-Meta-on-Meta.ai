index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('id="step5DownloadBtn"', 'id="btnDownloadRender"')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated step5DownloadBtn -> btnDownloadRender in index.html')
