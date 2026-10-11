import os
import sys

pm_path = r'E:\stickman-video-automation\studio\server\profile_manager.js'
with open(pm_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace launchLoginAssistant with enhanced version that thoroughly cleans orphan processes and lockfiles
target_method = "  async launchLoginAssistant(workerId) {"
idx = code.find(target_method)

if idx != -1:
    end_idx = code.find("  async stopAllWorkers()", idx)
    enhanced_methods = """  /**
   * Thoroughly terminate any hanging Chrome processes associated with a worker and remove lockfiles
   */
  cleanWorkerProcessesAndLocks(workerId = null) {
    if (process.platform === 'win32') {
      const { execSync } = require('child_process');
      try {
        const filter = workerId ? `*Worker-${workerId}*` : '*Worker-W*';
        const psCmd = `Get-CimInstance Win32_Process -Filter "name = 'chrome.exe'" | Where-Object { $_.CommandLine -like "${filter}" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }`;
        execSync(`powershell -NoProfile -Command "${psCmd}"`, { stdio: 'ignore' });
      } catch (e) {}
    }
    const workers = workerId ? [workerId] : Array.from({ length: 10 }, (_, i) => `W${String(i + 1).padStart(2, '0')}`);
    for (const w of workers) {
      const pDir = this.getProfileDir(w);
      const staleLocks = ['SingletonLock', 'lockfile', 'SingletonSocket', 'SingletonCookie'];
      for (const lock of staleLocks) {
        try {
          const lPath = path.join(pDir, lock);
          if (fs.existsSync(lPath)) fs.unlinkSync(lPath);
        } catch (e) {}
      }
    }
  }

  /**
   * Launch a clean interactive Chrome instance specifically for One-Time Login
   * Opens both Meta.ai and Flow tabs, cleans lockfiles, enables persistent session saving
   */
  async launchLoginAssistant(workerId) {
    this.validateWorkerId(workerId);

    // Stop and kill any processes holding this worker's directory
    this.cleanWorkerProcessesAndLocks(workerId);
    this.activeProcesses.delete(workerId);
    await new Promise(r => setTimeout(r, 400));

    const profileDir = this.getProfileDir(workerId);
    const metaUrl = 'https://www.meta.ai/';
    const flowUrl = 'https://flow.google.com/?pli=1';

    // Interactive launch arguments: both tabs open, persistent user data dir
    const args = [
      `--user-data-dir=${profileDir}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--window-size=1280,820',
      metaUrl,
      flowUrl
    ];

    logger.info('WORKER_LOGIN', `Launching 1-time login assistant for worker ${workerId} at ${profileDir}`);

    const child = spawn(this.chromePath, args, {
      detached: true,
      stdio: 'ignore'
    });

    const info = {
      workerId,
      provider: 'dual',
      pid: child.pid,
      profileDir,
      startTime: new Date().toISOString(),
      isLoginMode: true
    };

    this.activeProcesses.set(workerId, info);

    child.on('exit', (code, signal) => {
      logger.info('WORKER_LOGIN', `Worker ${workerId} login window closed (code: ${code})`);
      this.activeProcesses.delete(workerId);
    });

    child.unref();

    return {
      success: true,
      workerId,
      pid: child.pid,
      profileDir,
      urls: [metaUrl, flowUrl]
    };
  }

"""
    code = code[:idx] + enhanced_methods + code[end_idx:]
    with open(pm_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print('Successfully updated profile_manager.js with cleanWorkerProcessesAndLocks')
else:
    print('target_method not found in profile_manager.js')
