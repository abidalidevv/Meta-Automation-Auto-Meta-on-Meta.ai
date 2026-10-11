import os, shutil

workers_dir = r'E:\stickman-video-automation\Workers'
for w in os.listdir(workers_dir):
    w_path = os.path.join(workers_dir, w)
    if os.path.isdir(w_path):
        sessions_dir = os.path.join(w_path, 'Default', 'Sessions')
        if os.path.exists(sessions_dir):
            try:
                shutil.rmtree(sessions_dir)
                print(f"Cleaned Sessions for {w}")
            except Exception as e:
                print(f"Error cleaning {w}: {e}")

print("Stale worker sessions cleaned.")
