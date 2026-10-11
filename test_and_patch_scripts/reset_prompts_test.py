import sqlite3

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check prompt 2
cursor.execute("UPDATE prompts SET status = 'COMPLETED' WHERE status = 'REPAIR_PENDING'")
# Reset prompts 3-19 to QUEUED and assigned to W01
cursor.execute("UPDATE prompts SET status = 'QUEUED', assigned_worker_id = 'W01' WHERE prompt_index > 2")
conn.commit()
print("Updated prompts in SQLite")
