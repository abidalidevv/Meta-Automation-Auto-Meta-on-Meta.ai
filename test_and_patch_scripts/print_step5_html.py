with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos1 = html.find('id="step-5-panel"')
pos2 = html.find('id="step-6-panel"')
print("=== Step 5 Panel in index.html ===")
print(html[pos1:pos2].encode('ascii', 'replace').decode('ascii'))
