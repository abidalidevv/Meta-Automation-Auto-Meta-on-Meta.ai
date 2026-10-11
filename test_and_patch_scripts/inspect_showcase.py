import sqlite3

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cur = conn.cursor()

p1 = cur.execute('SELECT * FROM projects WHERE id = "proj_1790606377967_16ls"').fetchone()
prompts = cur.execute('SELECT count(*), sum(case when status="COMPLETED" then 1 else 0 end) FROM prompts WHERE project_id = "proj_1790606377967_16ls"').fetchone()
print('proj_1790606377967_16ls:', p1)
print('Prompts:', prompts)
