import re

with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Look for Step 1 / Mode 1 container
m1 = re.search(r'id=[\'"]mode1Container[\'"]|class=[\'"][^\'"]*mode1[^\'"]*[\'"]', html)
if m1:
    idx = m1.start()
    print("=== Mode 1 Container (first 1500 chars) ===")
    print(html[idx:idx+1500].encode('ascii', 'replace').decode('ascii'))

# 2. Look for Step 4 Media Grid container
m2 = re.search(r'id=[\'"]mediaGrid[\'"]|id=[\'"]assetsGrid[\'"]', html)
if m2:
    idx = m2.start()
    print("\n=== Media Grid Container ===")
    print(html[idx-100:idx+600].encode('ascii', 'replace').decode('ascii'))

# 3. Look for Step 5 Video Preview tabs
m3 = re.search(r'id=[\'"]previewContainer[\'"]|step-5|data-step=[\'"]5[\'"]', html)
if m3:
    idx = m3.start()
    print("\n=== Step 5 Container ===")
    print(html[idx:idx+1200].encode('ascii', 'replace').decode('ascii'))
