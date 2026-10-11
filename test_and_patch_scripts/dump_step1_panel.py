with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's inspect step-1-panel completely
p_start = text.find('id="step-1-panel"')
p_end = text.find('id="step-2-panel"')
print("=== STEP 1 PANEL HTML (total len:", p_end - p_start, ") ===")
step1_html = text[p_start:p_end]
for line in step1_html.splitlines():
    print(line[:110].encode('ascii', 'replace').decode('ascii'))
