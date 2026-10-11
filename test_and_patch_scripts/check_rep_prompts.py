import sqlite3

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()
rep = cursor.execute("SELECT id, prompt_index, status, assigned_worker_id, project_id FROM prompts WHERE status = 'REPAIR_PENDING'").fetchall()
print('Repair prompts count:', len(rep))
for r in rep:
    print(' ', r)
