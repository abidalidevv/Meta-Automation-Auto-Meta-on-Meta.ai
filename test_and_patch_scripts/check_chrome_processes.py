import subprocess

cmd = """powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \\"name = 'chrome.exe'\\" | Select-Object ProcessId, CommandLine | ForEach-Object { \\"$($_.ProcessId): $($_.CommandLine)\\" }" """
res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
for line in res.stdout.splitlines():
    if line.strip():
        print(line[:120])
