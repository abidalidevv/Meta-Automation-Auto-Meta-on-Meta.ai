import os, sys, re, sqlite3, json, urllib.request

print("==================================================")
print("   STICKMAN STUDIO & META AUTOMATION DEEP AUDIT   ")
print("==================================================")

# 1. HTML Integrity Check
with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html_text = f.read()

print(f"\n[1] HTML Check (Length: {len(html_text):,} chars):")
panels = re.findall(r'id=[\'"](step-\d-panel)[\'"]', html_text)
print(f"  Step panels found in HTML: {panels}")

# Check if there are duplicate sections or broken tags
for step_num in range(1, 7):
    p_id = f"step-{step_num}-panel"
    count = html_text.count(f'id="{p_id}"')
    print(f"  Panel {p_id}: {count} instance(s)")

# 2. Check JS file
with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8', errors='ignore') as f:
    js_text = f.read()

print(f"\n[2] JS Check (Length: {len(js_text):,} chars):")
# Check media loading in app_v2.js
media_matches = [line for line in js_text.splitlines() if 'function loadMedia' in line or 'function renderMedia' in line or 'function switchStep' in line or 'goToStep' in line]
print(f"  Navigation / Media functions found:")
for m in media_matches[:10]:
    print(f"    - {m.strip()[:90]}")

# 3. Check Media Gallery image rendering in app_v2.js
print("\n[3] Media Gallery Thumbnail Rendering:")
idx = js_text.find('loadMediaAssets')
if idx != -1:
    print(js_text[idx:idx+800].encode('ascii', 'replace').decode('ascii'))
else:
    # find where prompts are mapped to images in media gallery
    for line in js_text.splitlines():
        if 'api/v1/projects/' in line and 'prompts' in line:
            print(f"    {line.strip()[:100]}")

# 4. Check Database Consistency
print("\n[4] Database Consistency:")
db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
proj = cur.execute("SELECT id, name, directory_path FROM projects WHERE status = 'ACTIVE' LIMIT 1").fetchone()
if proj:
    p_id, p_name, p_dir = proj
    print(f"  Active Project: {p_name} ({p_id})")
    print(f"  Directory: {p_dir} (Exists: {os.path.exists(p_dir)})")
    
    # Check physical folders
    if os.path.exists(p_dir):
        subdirs = os.listdir(p_dir)
        print(f"  Subdirectories in project: {subdirs}")
        c_images = os.path.join(p_dir, 'central_images')
        if os.path.exists(c_images):
            imgs = os.listdir(c_images)
            print(f"  central_images count: {len(imgs)} files: {imgs[:5]}")
            
    # Check prompts in DB
    prompts = cur.execute("SELECT prompt_index, status, file_name, file_path FROM prompts WHERE project_id = ?", (p_id,)).fetchall()
    print(f"  Total prompts in DB: {len(prompts)}")
    completed = [p for p in prompts if p[1] == 'COMPLETED']
    assigned = [p for p in prompts if p[1] == 'ASSIGNED']
    pending = [p for p in prompts if p[1] in ('PENDING', 'QUEUED')]
    print(f"  Status breakdown: Completed={len(completed)}, Assigned={len(assigned)}, Pending={len(pending)}")
    for c in completed:
        file_exists = os.path.exists(c[3]) if c[3] else False
        print(f"    Completed prompt #{c[0]}: file={c[2]} exists_on_disk={file_exists}")
else:
    print("  No active project found in DB!")

print("\n==================================================")
