import sqlite3

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cur = conn.cursor()

tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables in studio.sqlite:', [t[0] for t in tables])

cols = cur.execute("PRAGMA table_info(projects)").fetchall()
print('Projects columns:', [c[1] for c in cols])

pids = ['proj_1790606377967_16ls', 'proj_1790683228262_vpmv', 'proj_1790887253002_ssh4']
for pid in pids:
    proj = cur.execute('SELECT * FROM projects WHERE id = ?', (pid,)).fetchone()
    prompts_cnt = cur.execute('SELECT count(*) FROM prompts WHERE project_id = ?', (pid,)).fetchone()[0]
    completed_cnt = cur.execute("SELECT count(*) FROM prompts WHERE project_id = ? AND status = 'COMPLETED'", (pid,)).fetchone()[0]
    print('='*50)
    print('PID:', pid)
    print('Name:', proj[1] if proj else None)
    print('Dir:', proj[2] if proj else None)
    print(f'Prompts: {prompts_cnt} (Completed: {completed_cnt})')
    print('Full Row:', proj)
