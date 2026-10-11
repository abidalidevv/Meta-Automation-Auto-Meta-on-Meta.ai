import subprocess
import os

try:
    cmd = 'powershell -Command "Get-CimInstance Win32_Process -Filter \\"name = \'chrome.exe\'\\" | Select-Object ProcessId, CommandLine"'
    out = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
    worker_pids = []
    for line in out.splitlines():
        if 'Worker-' in line:
            parts = line.strip().split()
            print('Worker process:', line[:120])
            if parts:
                worker_pids.append(parts[0])
    print(f'Total worker chrome processes: {len(worker_pids)}')
except Exception as e:
    print('Error:', e)
