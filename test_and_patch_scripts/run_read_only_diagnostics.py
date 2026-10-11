import sqlite3, os, subprocess, json, urllib.request

print("=== 1. SERVER HEALTH CHECK ===")
try:
    res = urllib.request.urlopen('http://127.0.0.1:45450/api/v1/health', timeout=3)
    print("Studio Server Health:", res.read().decode())
except Exception as e:
    print("Studio Server Health check failed:", e)

print("\n=== 2. EXTERNAL TOOLS (FFMPEG, PYTHON) ===")
try:
    ff = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    print("FFmpeg:", ff.stdout.splitlines()[0] if ff.stdout else "Not found")
except Exception as e:
    print("FFmpeg not in PATH:", e)

try:
    ffp = subprocess.run(['ffprobe', '-version'], capture_output=True, text=True)
    print("FFprobe:", ffp.stdout.splitlines()[0] if ffp.stdout else "Not found")
except Exception as e:
    print("FFprobe not in PATH:", e)

print("\n=== 3. SQLITE DATABASE SCHEMA & COUNTS ===")
db_path = r'E:\stickman-video-automation\studio\data\studio.sqlite'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    for t in tables:
        tname = t[0]
        cnt = cur.execute(f"SELECT count(*) FROM {tname}").fetchone()[0]
        print(f"Table: {tname:<25} Rows: {cnt}")
else:
    print("DB not found at", db_path)

print("\n=== 4. CURRENT ACTIVE PROJECTS ===")
if os.path.exists(db_path):
    projs = cur.execute("SELECT id, name, mode, status, voiceover_path, directory_path FROM projects").fetchall()
    for p in projs:
        print(f"Project ID: {p[0]} | Name: {p[1]} | Mode: {p[2]} | Status: {p[3]}")
        print(f"  Dir: {p[5]}")
        print(f"  Voiceover: {p[4]}")
