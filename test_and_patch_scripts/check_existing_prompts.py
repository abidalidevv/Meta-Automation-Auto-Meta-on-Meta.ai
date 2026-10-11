import sqlite3

db = sqlite3.connect('studio/data/studio.sqlite')
cursor = db.cursor()

cursor.execute("SELECT id, project_id, prompt_index, prompt_id_str, status FROM prompts WHERE project_id = 'proj_1790606377967_16ls'")
rows = cursor.fetchall()
print(f"Total prompts in proj_1790606377967_16ls: {len(rows)}")
for r in rows[:10]:
    print(r)
