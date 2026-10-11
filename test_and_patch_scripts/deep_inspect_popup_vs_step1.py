with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Find submitNewProject and what step 1 subTabMode1/2 functions do
print('=== POPUP: submitNewProject scope ===')
in_submit = False
count = 0
for i, l in enumerate(lines):
    if 'async function submitNewProject' in l:
        in_submit = True
    if in_submit:
        clean = l.strip()[:90].encode('ascii', 'replace').decode('ascii')
        print(f'{i+1}: {clean}')
        count += 1
        if count > 70:
            break

print('\n=== STEP 1: importRawPrompts (Mode 1 tab) ===')
in_fn = False
count2 = 0
for i, l in enumerate(lines):
    if 'async function importRawPrompts' in l or 'function importRawPrompts' in l:
        in_fn = True
    if in_fn:
        clean = l.strip()[:90].encode('ascii', 'replace').decode('ascii')
        print(f'{i+1}: {clean}')
        count2 += 1
        if count2 > 30:
            break
