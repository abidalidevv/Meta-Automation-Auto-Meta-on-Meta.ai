with open(r'E:\stickman-video-automation\studio\server\profile_manager.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'const psCmd = `Get-CimInstance Win32_Process -Filter "name = \'chrome.exe\'" | Where-Object { $_.CommandLine -like "${filter}" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }`;\n        execSync(`powershell -NoProfile -Command "${psCmd}"`, { stdio: \'ignore\' });\n      } catch (e) {}'

replacement = 'const psCmd = `Get-CimInstance Win32_Process | Where-Object { $_.Name -eq \'chrome.exe\' -and $_.CommandLine -like \'${filter}\' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }`;\n        execSync(`powershell -NoProfile -NonInteractive -Command "${psCmd}"`, { stdio: \'ignore\' });\n      } catch (e) { logger.warn(\'PROFILE_MANAGER\', `Process cleanup error: ${e.message}`); }'

if target in text:
    text = text.replace(target, replacement)
    with open(r'E:\stickman-video-automation\studio\server\profile_manager.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: profile_manager.js patched!")
else:
    print("TARGET NOT FOUND! Let's check exact substring:")
    idx = text.find('Get-CimInstance')
    print(repr(text[idx-20:idx+250]))
