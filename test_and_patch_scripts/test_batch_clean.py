import sqlite3, requests

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM jobs WHERE worker_id = 'W01'")
cursor.execute("UPDATE workers SET active_job_id = NULL WHERE id = 'W01'")
conn.commit()

BASE_URL = 'http://127.0.0.1:45450/api/v1'
job_res = requests.get(f"{BASE_URL}/workers/W01/job")
print("Status:", job_res.status_code)
data = job_res.json()
if data and data.get('job'):
    j = data['job']
    print("Batch Job ID:", j.get('job_id'))
    print("Total prompts in batch:", j.get('total_prompts'))
    print("Prompts count in array:", len(j.get('prompts', [])))
    for p in j.get('prompts', [])[:3]:
        print(" ", p)
else:
    print("No job:", data)
