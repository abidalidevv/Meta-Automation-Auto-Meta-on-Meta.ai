import sqlite3, requests

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()
cursor.execute("DELETE FROM jobs")
cursor.execute("UPDATE workers SET active_job_id = NULL")
cursor.execute("UPDATE prompts SET status = 'QUEUED', assigned_worker_id = 'W01'")
conn.commit()

BASE = 'http://127.0.0.1:45450/api/v1'
res = requests.get(f'{BASE}/workers/W01/job')
data = res.json()
print('HTTP Response Status:', res.status_code)
if data and data.get('job'):
    j = data['job']
    print('Batch Job ID:', j.get('job_id'))
    print('Type:', j.get('type'))
    print('Total Prompts:', j.get('total_prompts'))
    prompts = j.get('prompts', [])
    print('Prompts Array Length:', len(prompts))
    if len(prompts) > 0:
        print('First Prompt ID:', prompts[0]['prompt_id_str'])
        print('Last Prompt ID:', prompts[-1]['prompt_id_str'])
else:
    print('Response:', data)
