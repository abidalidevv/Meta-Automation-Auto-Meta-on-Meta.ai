import sqlite3
from datetime import datetime

db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

now = datetime.utcnow().isoformat() + 'Z'

workers_data = [
    ('W01', 'flow', 'OFFLINE', 'Worker-01', 'Workers/Worker-01'),
    ('W02', 'meta', 'OFFLINE', 'Worker-02', 'Workers/Worker-02'),
    ('W03', 'flow', 'OFFLINE', 'Worker-03', 'Workers/Worker-03'),
    ('W04', 'meta', 'OFFLINE', 'Worker-04', 'Workers/Worker-04'),
    ('W05', 'flow', 'OFFLINE', 'Worker-05', 'Workers/Worker-05'),
    ('W06', 'meta', 'OFFLINE', 'Worker-06', 'Workers/Worker-06'),
    ('W07', 'flow', 'OFFLINE', 'Worker-07', 'Workers/Worker-07'),
    ('W08', 'meta', 'OFFLINE', 'Worker-08', 'Workers/Worker-08'),
    ('W09', 'flow', 'OFFLINE', 'Worker-09', 'Workers/Worker-09'),
    ('W10', 'meta', 'OFFLINE', 'Worker-10', 'Workers/Worker-10'),
]

for w in workers_data:
    cursor.execute('''
        INSERT INTO workers (id, provider, status, profile_name, profile_path, reference_status, active_character_version, last_heartbeat, registered_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'NOT_READY', 0, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            provider = excluded.provider,
            profile_name = excluded.profile_name,
            profile_path = excluded.profile_path,
            updated_at = excluded.updated_at
    ''', (w[0], w[1], w[2], w[3], w[4], now, now, now))

conn.commit()

cursor.execute('SELECT id, provider, profile_name, status FROM workers ORDER BY id ASC')
rows = cursor.fetchall()
print(f"Total workers in database now: {len(rows)}")
for r in rows:
    print(r)

conn.close()
