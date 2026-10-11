import sqlite3

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- PROJECTS ---")
for p in cursor.execute("SELECT id, name, status, created_at FROM projects ORDER BY created_at DESC LIMIT 5").fetchall():
    print(dict(p))

latest_project = cursor.execute("SELECT id FROM projects ORDER BY created_at DESC LIMIT 1").fetchone()
if latest_project:
    pid = latest_project['id']
    print(f"\n--- PROMPTS for project {pid} ---")
    prompts = cursor.execute("SELECT id, prompt_index, assigned_worker_id, status FROM prompts WHERE project_id = ? ORDER BY prompt_index ASC", (pid,)).fetchall()
    print(f"Total prompts: {len(prompts)}")
    for pr in prompts[:10]:
        print(dict(pr))

    print(f"\n--- JOBS for project {pid} ---")
    jobs = cursor.execute("SELECT id, worker_id, status, created_at FROM jobs WHERE project_id = ? LIMIT 10", (pid,)).fetchall()
    print(f"Total jobs: {len(jobs)}")
    for j in jobs:
        print(dict(j))

print("\n--- WORKERS ---")
for w in cursor.execute("SELECT id, provider, status, active_job_id, reference_status FROM workers").fetchall():
    print(dict(w))
