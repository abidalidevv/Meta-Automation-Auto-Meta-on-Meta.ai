import sqlite3

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()

print("--- Prompts file_path samples ---")
for p in cursor.execute("SELECT id, prompt_index, status, file_path, file_name FROM prompts WHERE file_path IS NOT NULL LIMIT 10").fetchall():
    print(p)

print("\n--- Timeline items image_path samples ---")
for t in cursor.execute("SELECT id, prompt_id, image_path FROM timeline_items WHERE image_path IS NOT NULL LIMIT 10").fetchall():
    print(t)
