import sqlite3

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()

print("--- Prompts for proj_1790887253002_ssh4 ---")
for p in cursor.execute("SELECT id, prompt_index, status, file_path, file_name FROM prompts WHERE project_id = 'proj_1790887253002_ssh4' LIMIT 10").fetchall():
    print(p)

print("\n--- Timeline for proj_1790887253002_ssh4 ---")
for t in cursor.execute("SELECT id, prompt_id, image_path FROM timeline_items WHERE project_id = 'proj_1790887253002_ssh4' LIMIT 10").fetchall():
    print(t)
