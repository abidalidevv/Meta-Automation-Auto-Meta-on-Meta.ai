import subprocess

try:
    cmd = 'powershell -Command "Get-Process | Where-Object { $_.Path -like \'*chrome*\' } | Select-Object Id, Path, CommandLine"'
    out = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
    for line in out.splitlines():
        if 'Worker-W01' in line:
            print('Holding process:', line)
except Exception as e:
    print('Error:', e)
