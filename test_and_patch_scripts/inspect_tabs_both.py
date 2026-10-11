import re

with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Let's inspect the New Project Modal tabs
modal_idx = text.find('id="newProjectModal"')
if modal_idx != -1:
    modal_snippet = text[modal_idx:modal_idx+2000]
    print("=== NEW PROJECT MODAL HEADER & TABS ===")
    for line in modal_snippet.splitlines()[:40]:
        print(line[:120].encode('ascii', 'replace').decode('ascii'))

# Let's find Step 1 in index.html
step1_idx = text.find('id="step1View"')
if step1_idx != -1:
    step1_snippet = text[step1_idx:step1_idx+2000]
    print("\n=== STEP 1 VIEW HEADER & TABS ===")
    for line in step1_snippet.splitlines()[:40]:
        print(line[:120].encode('ascii', 'replace').decode('ascii'))
