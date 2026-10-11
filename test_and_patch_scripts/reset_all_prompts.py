import sqlite3

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DELETE FROM jobs")
cursor.execute("UPDATE prompts SET status = 'QUEUED'")
cursor.execute("UPDATE workers SET active_job_id = NULL")
conn.commit()
print("All 19 prompts reset to QUEUED, no jobs.")
