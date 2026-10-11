import sqlite3
conn = sqlite3.connect(r'E:\stickman-video-automation\studio\data\studio.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='prompts'")
print(cursor.fetchone()[0])
conn.close()
