import subprocess

ps = "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'chrome.exe' -and $_.CommandLine -like '*Worker-W*' } | ForEach-Object { \"$($_.ProcessId): $($_.CommandLine)\" }"
res = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True)
print("Worker Chrome processes currently running:")
for line in res.stdout.splitlines():
    print(" ", line[:120])
