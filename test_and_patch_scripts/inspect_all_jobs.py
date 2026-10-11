import sqlite3

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- ALL JOBS ---")
for j in cursor.execute("SELECT * FROM jobs").fetchall():
    print(dict(j))
