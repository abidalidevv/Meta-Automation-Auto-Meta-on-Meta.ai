import os
import sys

pm_path = r'E:\stickman-video-automation\studio\server\profile_manager.js'
with open(pm_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Require db at top if not present
if "const db = require('./db');" not in code:
    code = code.replace("const logger = require('./logger');", "const logger = require('./logger');\nconst db = require('./db');")

# 2. Update prepareWorkerExtension to be strictly isolated per worker
old_prep_start = code.find('prepareWorkerExtension(workerId, provider) {')
old_prep_end = code.find('getTargetUrl(provider) {')

new_prep = '''prepareWorkerExtension(workerId, provider) {
    const prov = (provider || '').toLowerCase();
    const baseExtDir = this.getBaseExtensionPath(prov);
    if (!baseExtDir || !fs.existsSync(baseExtDir)) {
      throw new Error(`Base extension not found for provider '${provider}' at ${baseExtDir}`);
    }

    const profileDir = this.getProfileDir(workerId);
    const workerExtDir = path.join(profileDir, 'extension');

    // Check if worker extension already exists and matches target provider
    let needsProvisioning = !fs.existsSync(workerExtDir);
    const configPath = path.join(workerExtDir, 'worker-config.js');
    if (!needsProvisioning && fs.existsSync(configPath)) {
      try {
        const existingConfig = fs.readFileSync(configPath, 'utf8');
        if (!existingConfig.includes(`WORKER_ID = "${workerId}"`) || !existingConfig.includes(`PROVIDER = "${prov}"`)) {
          needsProvisioning = true;
          fs.rmSync(workerExtDir, { recursive: true, force: true });
        }
      } catch (e) {
        needsProvisioning = true;
      }
    }

    if (needsProvisioning) {
      logger.info('PROFILE_MANAGER', `Provisioning isolated extension for worker ${workerId} (${prov}) into ${workerExtDir}`);
      this.copyDirRecursive(baseExtDir, workerExtDir);
    }

    // Always ensure worker-config.js contains exact WORKER_ID and PROVIDER
    const configContent = `export const WORKER_ID = "${workerId}";\\nexport const PROVIDER = "${prov}";\\n`;
    fs.writeFileSync(configPath, configContent, 'utf8');

    return workerExtDir;
  }

  '''

if old_prep_start != -1 and old_prep_end != -1:
    code = code[:old_prep_start] + new_prep + code[old_prep_end:]
    print('Replaced prepareWorkerExtension successfully')
else:
    print('Error: Could not find prepareWorkerExtension boundaries')
    sys.exit(1)

# 3. Clean up and replace launchLoginAssistant and cleanWorkerProcessesAndLocks
# Find cleanWorkerProcessesAndLocks start to module.exports
clean_start = code.find('cleanWorkerProcessesAndLocks(workerId = null) {')
mod_export_idx = code.find('module.exports = new BrowserProfileManager();')

if clean_start != -1 and mod_export_idx != -1:
    new_end_methods = '''cleanWorkerProcessesAndLocks(workerId = null) {
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
   * Launch a clean interactive Chrome instance for One-Time Login
   * Strictly 1 worker = 1 service = 1 extension (Meta.ai OR Google Flow)
   * Never dual tabs, never dual extensions
   */
  async launchLoginAssistant(workerId, requestedProvider = null) {
    this.validateWorkerId(workerId);

    // Stop and kill any processes holding this worker's directory & delete lockfiles
    this.cleanWorkerProcessesAndLocks(workerId);
    this.activeProcesses.delete(workerId);
    await new Promise(r => setTimeout(r, 400));

    // Resolve provider from argument, DB, or fallback
    let provider = (requestedProvider || '').toLowerCase();
    if (!provider || !['meta', 'flow'].includes(provider)) {
      try {
        const row = await db.get('SELECT provider FROM workers WHERE id = ?', [workerId]);
        if (row && row.provider) {
          provider = row.provider.toLowerCase();
        }
      } catch (e) {}
    }
    if (!provider || !['meta', 'flow'].includes(provider)) {
      const num = parseInt(workerId.replace(/\\D/g, ''), 10);
      provider = (num % 2 === 1) ? 'flow' : 'meta';
    }

    const profileDir = this.getProfileDir(workerId);
    const extensionPath = this.prepareWorkerExtension(workerId, provider);
    const targetUrl = this.getTargetUrl(provider);

    // Strictly ONE isolated extension and strictly ONE target URL
    const args = [
      `--user-data-dir=${profileDir}`,
      `--load-extension=${extensionPath}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--window-size=1280,820',
      targetUrl
    ];

    logger.info('WORKER_LOGIN', `Launching 1-time login assistant for worker ${workerId} (${provider.toUpperCase()}) -> ${targetUrl} [Profile: ${profileDir}]`);

    const child = spawn(this.chromePath, args, {
      detached: true,
      stdio: 'ignore'
    });

    const info = {
      workerId,
      provider,
      pid: child.pid,
      profileDir,
      extensionPath,
      targetUrl,
      startTime: new Date().toISOString(),
      isLoginMode: true
    };

    this.activeProcesses.set(workerId, info);

    child.on('exit', (code, signal) => {
      logger.info('WORKER_LOGIN', `Worker ${workerId} (${provider}) login window closed (code: ${code}, signal: ${signal})`);
      this.activeProcesses.delete(workerId);
    });

    child.unref();

    return {
      success: true,
      workerId,
      provider,
      pid: child.pid,
      profileDir,
      targetUrl,
      extensionPath
    };
  }

  /**
   * Stop all active worker processes
   */
  async stopAllWorkers() {
    logger.info('PROFILE_MANAGER', `Stopping all ${this.activeProcesses.size} active worker processes...`);
    const results = [];
    for (const [wId, info] of Array.from(this.activeProcesses.entries())) {
      try {
        const res = await this.stopWorker(wId);
        results.push(res);
      } catch (e) {
        results.push({ success: false, workerId: wId, error: e.message });
      }
    }
    return { success: true, count: results.length, results };
  }
}

'''
    code = code[:clean_start] + new_end_methods + code[mod_export_idx:]
    print('Replaced cleanWorkerProcessesAndLocks and launchLoginAssistant successfully')
else:
    print('Error: Could not find cleanWorkerProcessesAndLocks or module.exports')
    sys.exit(1)

with open(pm_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('profile_manager.js updated successfully!')
