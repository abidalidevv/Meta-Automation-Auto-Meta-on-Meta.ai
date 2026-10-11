import sqlite3

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()
jobs = cursor.execute("SELECT id, prompt_id, worker_id, status FROM jobs").fetchall()
print('Jobs count:', len(jobs))
for j in jobs:
    print(' ', j)
