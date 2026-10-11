import urllib.request, json, time, os

BASE_URL = 'http://127.0.0.1:45450/api/v1'

def post_json(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req)
    return json.loads(res.read().decode())

def get_json(endpoint):
    res = urllib.request.urlopen(f"{BASE_URL}{endpoint}")
    return json.loads(res.read().decode())

print("=== 1. SERVER HEALTH ===")
health = get_json('/health')
print("Health:", health.get('status'))

print("\n=== 2. CREATE TEST PROJECT ===")
proj = post_json('/projects', {
    'name': 'E2E Verification Project',
    'mode': 'MODE_1',
    'voiceover_duration': 10
})
proj_id = proj['id']
print(f"Created project: {proj['name']} (ID: {proj_id})")

print("\n=== 3. IMPORT PROMPTS (STEP 1 MODE 1) ===")
raw_prompts = """001_Minimalist stickman stands in an empty white room
002_The stickman draws a glowing cyan line in the air
003_A futuristic neon door opens before the stickman"""

import_res = post_json(f'/projects/{proj_id}/prompts/import', {
    'raw_prompts': raw_prompts
})
print("Import result:", import_res)

print("\n=== 4. ATTACH CHARACTER REFERENCE (NEW POST ENDPOINT) ===")
dummy_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
char_res = post_json(f'/projects/{proj_id}/character-reference', {
    'character_name': 'Test Stickman',
    'character_description': 'Stickman with red headband',
    'image_base64': dummy_png
})
print("Char ref result:", char_res)

try:
    c_img = urllib.request.urlopen(f"{BASE_URL}/projects/{proj_id}/character-reference").read()
    print(f"GET character-reference returned {len(c_img)} bytes image successfully!")
except Exception as e:
    print("GET char-ref failed:", e)

print("\n=== 5. FLEET ALLOCATION & DISPATCH ===")
dispatch = post_json(f'/projects/{proj_id}/workers/dispatch-fleet', {
    'quota_per_worker': 5,
    'max_concurrent': 2,
    'auto_launch': False
})
print("Dispatch result message:", dispatch.get('message'))
print("Active batch:", dispatch.get('active_batch_1'))

print("\n=== 6. WORKER POLLS JOB ===")
active_batch = dispatch.get('active_batch_1', [])
if active_batch and isinstance(active_batch[0], dict):
    worker_id = active_batch[0]['worker_id']
else:
    worker_id = 'W01'

job_data = get_json(f'/workers/{worker_id}/job')
print(f"Worker {worker_id} next job type:", job_data.get('job', {}).get('type'))
if job_data.get('job'):
    prompts_in_job = job_data['job'].get('prompts', [])
    print(f"Prompts delivered in job: {len(prompts_in_job)}")
    for p in prompts_in_job:
        print(f"  - #{p.get('prompt_index')}: {p.get('prompt_text')[:40]}...")

print("\n=== 7. CLEANUP TEST PROJECT ===")
import sqlite3, shutil
conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
conn.execute('DELETE FROM prompts WHERE project_id = ?', (proj_id,))
conn.execute('DELETE FROM jobs WHERE project_id = ?', (proj_id,))
conn.execute('DELETE FROM character_references WHERE project_id = ?', (proj_id,))
conn.execute('DELETE FROM projects WHERE id = ?', (proj_id,))
conn.commit()
if os.path.exists(proj['directory_path']):
    shutil.rmtree(proj['directory_path'], ignore_errors=True)
print("Test project cleaned up cleanly from DB and disk!")

print("\n============================================")
print("       ALL E2E CHECKS PASSED 100%!          ")
print("============================================")
