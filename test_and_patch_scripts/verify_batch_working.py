import sqlite3, requests

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM jobs")
cursor.execute("UPDATE workers SET active_job_id = NULL")
cursor.execute("UPDATE prompts SET status = 'QUEUED', assigned_worker_id = 'W01'")
conn.commit()

BASE_URL = 'http://127.0.0.1:45450/api/v1'
job_res = requests.get(f"{BASE_URL}/workers/W01/job")
data = job_res.json()
if data and data.get('job'):
    j = data['job']
    print("SUCCESS! Batch Job ID:", j.get('job_id'))
    print("Total prompts in batch:", j.get('total_prompts'))
    print("Prompts count in array:", len(j.get('prompts', [])))
    print("Sample prompt 1:", j.get('prompts', [])[0]['prompt_id_str'])
    print("Sample prompt last:", j.get('prompts', [])[-1]['prompt_id_str'])
else:
    print("No job returned:", data)
