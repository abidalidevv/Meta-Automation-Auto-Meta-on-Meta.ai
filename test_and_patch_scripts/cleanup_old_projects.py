import sqlite3
import os
import shutil

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'

conn = sqlite3.connect(db_path)
cur = conn.cursor()

demo_proj_id = 'proj_1790887253002_ssh4'
demo_proj = cur.execute('SELECT * FROM projects WHERE id = ?', (demo_proj_id,)).fetchone()

# Update demo project name to "Demo Stickman Showcase"
cur.execute('UPDATE projects SET name = "Demo Stickman Showcase" WHERE id = ?', (demo_proj_id,))

# Check columns for all tables
tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
for tbl in tables:
    cols = [c[1] for c in cur.execute(f"PRAGMA table_info({tbl})").fetchall()]
    if 'project_id' in cols:
        cur.execute(f"DELETE FROM {tbl} WHERE project_id != ? AND project_id IS NOT NULL", (demo_proj_id,))
        print(f"Cleaned {tbl} table where project_id != {demo_proj_id}")

cur.execute("DELETE FROM projects WHERE id != ?", (demo_proj_id,))
conn.commit()

remaining_projects = cur.execute('SELECT id, name FROM projects').fetchall()
print("Remaining projects in DB:", remaining_projects)
remaining_prompts = cur.execute('SELECT count(*) FROM prompts WHERE project_id = ?', (demo_proj_id,)).fetchone()[0]
print(f"Remaining prompts for {demo_proj_id}: {remaining_prompts}")

# 2. Archive disk folders in E:\stickman-video-automation\Projects
projects_dir = r'E:\stickman-video-automation\Projects'
archive_dir = os.path.join(projects_dir, '_archive')
os.makedirs(archive_dir, exist_ok=True)

active_dir_name = os.path.basename(demo_proj[2]) if demo_proj else ''

moved_count = 0
for item in os.listdir(projects_dir):
    if item == '_archive' or item == active_dir_name:
        continue
    item_path = os.path.join(projects_dir, item)
    if os.path.isdir(item_path):
        dest_path = os.path.join(archive_dir, item)
        try:
            shutil.move(item_path, dest_path)
            moved_count += 1
        except Exception as e:
            pass

print(f"Moved {moved_count} test project folders to {archive_dir}")
conn.close()
