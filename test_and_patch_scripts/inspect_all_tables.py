import sqlite3

conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables in SQLite:', [t[0] for t in tables])

for t in [t[0] for t in tables]:
    print(f"\n--- Table: {t} ---")
    cols = cursor.execute(f"PRAGMA table_info({t})").fetchall()
    print([c[1] for c in cols])
    rows = cursor.execute(f"SELECT * FROM {t} LIMIT 2").fetchall()
    print("Sample rows:", len(rows))
