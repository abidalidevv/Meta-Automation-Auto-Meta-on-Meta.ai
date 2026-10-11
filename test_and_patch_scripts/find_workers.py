import subprocess

script = """
Get-CimInstance Win32_Process -Filter "name = 'chrome.exe'" | ForEach-Object {
    if ($_.CommandLine -match "Worker-W") {
        Write-Output "$($_.ProcessId) : $($_.CommandLine)"
    }
}
"""

with open('find_workers.ps1', 'w', encoding='utf-8') as f:
    f.write(script)

out = subprocess.check_output(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'find_workers.ps1']).decode('utf-8', errors='ignore')
print('Worker processes found:\n', out)
