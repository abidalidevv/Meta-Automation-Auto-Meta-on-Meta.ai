pm_path = r'E:\stickman-video-automation\studio\server\profile_manager.js'
with open(pm_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """    const args = [
      `--user-data-dir=${profileDir}`,
      `--load-extension=${extensionPath}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-background-networking',
      '--disable-default-apps',
      '--disable-sync',
      targetUrl
    ];"""

replacement = """    // Clean stray processes, locks, and stale session restore files
    this.cleanWorkerProcessesAndLocks(workerId);
    const sessionsDir = path.join(profileDir, 'Default', 'Sessions');
    if (fs.existsSync(sessionsDir)) {
      try { fs.rmSync(sessionsDir, { recursive: true, force: true }); } catch (e) {}
    }

    const args = [
      `--user-data-dir=${profileDir}`,
      `--load-extension=${extensionPath}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--no-restore-session-state',
      '--disable-session-crashed-bubble',
      '--restore-last-session=0',
      '--hide-crash-restore-bubble',
      '--disable-background-networking',
      '--disable-default-apps',
      '--disable-sync',
      targetUrl
    ];"""

assert target in text, "Target string not found in profile_manager.js"
new_text = text.replace(target, replacement, 1)

with open(pm_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Successfully patched launchWorker in profile_manager.js")
