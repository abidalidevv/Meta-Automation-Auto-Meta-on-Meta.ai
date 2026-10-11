with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Find generateM1Prompts (Step 1 Mode 2 - Groq AI)
print('=== STEP 1 Mode 2: generateM1Prompts (Groq AI) ===')
in_fn = False
count = 0
for i, l in enumerate(lines):
    if 'async function generateM1Prompts' in l or 'function generateM1Prompts' in l:
        in_fn = True
    if in_fn:
        clean = l.strip()[:90].encode('ascii', 'replace').decode('ascii')
        print(f'{i+1}: {clean}')
        count += 1
        if count > 40:
            break

# Find after submitNewProject what it does next
print('\n=== After project creation in submitNewProject ===')
in_after = False
count2 = 0
for i, l in enumerate(lines):
    if 'await fetch' in l and 'audio/upload' in l:
        in_after = True
    if in_after:
        clean = l.strip()[:90].encode('ascii', 'replace').decode('ascii')
        print(f'{i+1}: {clean}')
        count2 += 1
        if count2 > 30:
            break
