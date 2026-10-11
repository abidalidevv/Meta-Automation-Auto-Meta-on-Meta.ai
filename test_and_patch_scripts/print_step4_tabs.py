with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos1 = html.find('id="step-4-panel"')
pos2 = html.find('id="tabContent-media"')
print("=== Step 4 Tools Tabs in index.html ===")
print(html[pos1:pos2].encode('ascii', 'replace').decode('ascii'))
