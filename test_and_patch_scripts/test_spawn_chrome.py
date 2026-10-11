import subprocess
import os
import time

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
profile_dir = r'E:\stickman-video-automation\Workers\Worker-W01'

# Delete lockfile if present
lock = os.path.join(profile_dir, 'lockfile')
if os.path.exists(lock):
    try:
        os.remove(lock)
        print('Removed stale lockfile')
    except Exception as e:
        print('Failed to remove lockfile:', e)

args = [
    chrome_path,
    f'--user-data-dir={profile_dir}',
    '--no-first-run',
    '--no-default-browser-check',
    'https://www.meta.ai/',
    'https://flow.google.com/?pli=1'
]

print('Launching:', args)
proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)
poll = proc.poll()
print('Poll result after 2s:', poll)
if poll is not None:
    stdout, stderr = proc.communicate()
    print('stdout:', stdout.decode(errors='ignore'))
    print('stderr:', stderr.decode(errors='ignore'))
else:
    print('Chrome is running smoothly! Terminating test process...')
    proc.terminate()
