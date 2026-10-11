import subprocess, os, re

# Query and kill all chrome.exe processes whose CommandLine includes 'stickman-video-automation\Workers'
ps_script = """
Get-CimInstance Win32_Process | Where-Object { 
    $_.Name -eq 'chrome.exe' -and $_.CommandLine -like '*stickman-video-automation\\Workers*' 
} | ForEach-Object { 
    Write-Output "Killing PID: $($_.ProcessId)"
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue 
}
"""

with open(r'c:\Users\Ali\Desktop\meta automation\test_and_patch_scripts\kill_worker_chromes.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', r'c:\Users\Ali\Desktop\meta automation\test_and_patch_scripts\kill_worker_chromes.ps1'], capture_output=True, text=True)
print("Kill output:")
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

# Also clean lockfiles
workers_base = r'E:\stickman-video-automation\Workers'
if os.path.exists(workers_base):
    for root, dirs, files in os.walk(workers_base):
        for f in files:
            if f in ('lockfile', 'SingletonLock', 'SingletonCookie', 'SingletonSocket'):
                lpath = os.path.join(root, f)
                try:
                    os.unlink(lpath)
                    print(f"Removed lockfile: {lpath}")
                except Exception as e:
                    print(f"Could not remove {lpath}: {e}")
