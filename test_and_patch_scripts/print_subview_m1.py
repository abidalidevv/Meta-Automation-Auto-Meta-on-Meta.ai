with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos1 = html.find('id="subViewMode1"')
pos2 = html.find('id="subViewMode2"')
print("=== Sub-View Mode 1 ===")
print(html[pos1:pos2].encode('ascii', 'replace').decode('ascii'))
