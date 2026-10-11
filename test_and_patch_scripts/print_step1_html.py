with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos1 = html.find('id="step-1-panel"')
pos2 = html.find('id="step-2-panel"')
print("=== Step 1 Panel ===")
print(html[pos1:pos2].encode('ascii', 'replace').decode('ascii'))
