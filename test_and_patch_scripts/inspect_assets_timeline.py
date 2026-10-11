import sqlite3

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- ASSETS ---")
assets = cursor.execute("SELECT * FROM assets LIMIT 10").fetchall()
for a in assets:
    print(dict(a))

print("\n--- TIMELINE ITEMS ---")
timeline = cursor.execute("SELECT * FROM timeline LIMIT 10").fetchall()
for t in timeline:
    print(dict(t))
