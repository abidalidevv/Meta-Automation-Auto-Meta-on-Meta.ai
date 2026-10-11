with open(r'E:\stickman-video-automation\studio\server\profile_manager.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_chunk = """  cleanWorkerProcessesAndLocks(workerId = null) {
    if (process.platform === 'win32') {
      const { execSync } = require('child_process');
      try {
        const filter = workerId ? `*Worker-${workerId}*` : '*Worker-W*';
        const psCmd = `Get-CimInstance Win32_Process -Filter "name = 'chrome.exe'" | Where-Object { $_.CommandLine -like "${filter}" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }`;
        execSync(`powershell -NoProfile -Command "${psCmd}"`, { stdio: 'ignore', timeout: 5000 });
      } catch (e) {}"""

new_chunk = """  cleanWorkerProcessesAndLocks(workerId = null) {
    if (process.platform === 'win32') {
      const { execSync } = require('child_process');
      try {
        const filter = workerId ? `*Worker-${workerId}*` : '*Worker-W*';
        const psCmd = `Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'chrome.exe' -and $_.CommandLine -like '${filter}' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }`;
        execSync(`powershell -NoProfile -NonInteractive -Command "${psCmd}"`, { stdio: 'ignore', timeout: 6000 });
      } catch (e) {
        logger.warn('PROFILE_MANAGER', `Process cleanup error: ${e.message}`);
      }"""

if old_chunk in text:
    text = text.replace(old_chunk, new_chunk)
    with open(r'E:\stickman-video-automation\studio\server\profile_manager.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully patched cleanWorkerProcessesAndLocks in profile_manager.js!")
else:
    print("Could not find exact old_chunk in profile_manager.js")
