import sqlite3
conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='workers'")
print("Schema:")
print(cursor.fetchone()[0])
cursor.execute("SELECT * FROM workers")
rows = cursor.fetchall()
print(f"\nTotal rows in workers table: {len(rows)}")
for r in rows:
    print(r)
