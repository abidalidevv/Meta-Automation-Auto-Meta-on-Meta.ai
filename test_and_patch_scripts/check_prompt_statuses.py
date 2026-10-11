import sqlite3

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

for r in cursor.execute("SELECT id, prompt_index, status, assigned_worker_id FROM prompts WHERE project_id = 'proj_1790887253002_ssh4' ORDER BY prompt_index ASC").fetchall():
    print(dict(r))
