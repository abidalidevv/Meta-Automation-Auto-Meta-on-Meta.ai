import subprocess
import os

ps_cmd = 'Get-CimInstance Win32_Process -Filter "name = \'chrome.exe\'" | Where-Object { $_.CommandLine -like "*Worker-W*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
subprocess.run(['powershell', '-NoProfile', '-Command', ps_cmd])
print('Killed all orphan worker chrome processes.')

# Now try removing lockfile in Worker-W01
lock = r'E:\stickman-video-automation\Workers\Worker-W01\lockfile'
if os.path.exists(lock):
    try:
        os.remove(lock)
        print('Successfully removed Worker-W01 lockfile!')
    except Exception as e:
        print('Still locked:', e)
else:
    print('No lockfile in Worker-W01')
