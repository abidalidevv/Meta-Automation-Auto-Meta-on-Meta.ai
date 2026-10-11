import sqlite3

db = sqlite3.connect('E:/stickman-video-automation/studio/data/studio.sqlite')
c = db.cursor()

# 1. Cancel in-flight jobs belonging to old projects
c.execute("""
    UPDATE jobs 
    SET status = 'CANCELLED', last_error = 'Pruned stale ghost job'
    WHERE status IN ('ASSIGNED', 'ACKNOWLEDGED', 'GENERATING', 'DOWNLOADING', 'RETRYING')
      AND project_id != 'proj_1790683228262_vpmv'
""")
print(f"Cancelled {c.rowcount} stale ghost jobs")

# 2. Mark old REPAIR_PENDING prompts as FAILED so they don't loop
c.execute("""
    UPDATE prompts 
    SET status = 'FAILED'
    WHERE status = 'REPAIR_PENDING'
      AND project_id != 'proj_1790683228262_vpmv'
""")
print(f"Cleaned up {c.rowcount} old repair prompts")

# 3. Clear active_job_id on workers
c.execute("UPDATE workers SET active_job_id = NULL")
print(f"Reset active_job_id on {c.rowcount} workers")

db.commit()
print("Database cleanup completed successfully.")
