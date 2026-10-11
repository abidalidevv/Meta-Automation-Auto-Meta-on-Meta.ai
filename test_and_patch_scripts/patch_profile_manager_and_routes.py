import os
import sys

# 1. Patch profile_manager.js
pm_path = r'E:\stickman-video-automation\studio\server\profile_manager.js'
with open(pm_path, 'r', encoding='utf-8') as f:
    pm_code = f.read()

# Add launchLoginAssistant and stopAllWorkers to BrowserProfileManager class
target_class_end = "module.exports = new BrowserProfileManager();"

new_pm_methods = """  /**
   * Launch a clean interactive Chrome instance specifically for One-Time Login
   * Opens both Meta.ai and Flow tabs, cleans lockfiles, enables persistent session saving
   */
  async launchLoginAssistant(workerId) {
    this.validateWorkerId(workerId);

    // Stop any existing process for this worker to ensure a fresh, clean window
    if (this.activeProcesses.has(workerId)) {
      await this.stopWorker(workerId);
      await new Promise(r => setTimeout(r, 500));
    }

    const profileDir = this.getProfileDir(workerId);

    // Clean up stale lockfiles that can cause Chrome to fail spawning
    const staleLocks = ['SingletonLock', 'lockfile', 'SingletonSocket', 'SingletonCookie'];
    for (const lock of staleLocks) {
      const lockPath = path.join(profileDir, lock);
      try {
        if (fs.existsSync(lockPath)) {
          fs.unlinkSync(lockPath);
        }
      } catch (e) {}
    }

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
"""

if "launchLoginAssistant" not in pm_code:
    idx = pm_code.rfind("module.exports = new BrowserProfileManager();")
    if idx != -1:
        pm_code = pm_code[:idx] + new_pm_methods + "\n" + pm_code[idx:]
        with open(pm_path, 'w', encoding='utf-8') as f:
            f.write(pm_code)
        print('Successfully added launchLoginAssistant and stopAllWorkers to profile_manager.js')
    else:
        print('Error: Could not locate class end in profile_manager.js')
else:
    print('launchLoginAssistant already exists in profile_manager.js')

# 2. Patch logger.js to also write readable plain text logs to studio/logs/studio.log
logger_path = r'E:\stickman-video-automation\studio\server\logger.js'
with open(logger_path, 'r', encoding='utf-8') as f:
    log_code = f.read()

target_append = "  fs.appendFile(logFile, line, () => {});"
replacement_append = """  fs.appendFile(logFile, line, () => {});

  // Write plain text readable log file for user inspection
  const textLogDir = path.join(__dirname, '..', 'logs');
  if (!fs.existsSync(textLogDir)) {
    try { fs.mkdirSync(textLogDir, { recursive: true }); } catch (e) {}
  }
  const textLogFile = path.join(textLogDir, 'studio.log');
  const readableLine = `[${ts}] [${level.toUpperCase().padEnd(5)}] [${source.padEnd(16)}] ${sanitizedMsg}${sanitizedContext ? ' | ' + JSON.stringify(sanitizedContext) : ''}\\n`;
  fs.appendFile(textLogFile, readableLine, () => {});

  if (level === 'error') {
    const errorLogFile = path.join(textLogDir, 'studio_errors.log');
    fs.appendFile(errorLogFile, readableLine, () => {});
  }"""

if target_append in log_code and "studio.log" not in log_code:
    log_code = log_code.replace(target_append, replacement_append)
    with open(logger_path, 'w', encoding='utf-8') as f:
        f.write(log_code)
    print('Successfully patched logger.js for plain-text file logging')
else:
    print('logger.js already has readable plain-text logging or target not found')

# 3. Patch routes.js for login-assistant, stop-all, test-groq, and open-folder
routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    routes_code = f.read()

# Replace login-assistant handler
old_login_handler = """router.post('/workers/login-assistant', async (req, res) => {
  try {
    const { worker_id = 'W01', provider } = req.body;
    const workerId = (worker_id || 'W01').toUpperCase();

    if (workerId === 'ALL') {
      logger.info('WORKER_LOGIN', 'Launching all 10 worker profiles (W01–W10) for one-time login...');
      const launched = [];
      for (let i = 1; i <= 10; i++) {
        const wId = `W${String(i).padStart(2, '0')}`;
        const prov = (i % 2 === 1) ? 'meta' : 'flow';
        try {
          const result = await profileManager.launchWorker(wId, prov);
          launched.push({ workerId: wId, provider: prov, success: true, details: result });
          // stagger launches slightly to prevent process spikes
          await new Promise(r => setTimeout(r, 400));
        } catch (lErr) {
          logger.warn('WORKER_LOGIN', `Failed launching ${wId}: ${lErr.message}`);
          launched.push({ workerId: wId, provider: prov, success: false, error: lErr.message });
        }
      }
      return res.json({
        success: true,
        message: 'Launched workers W01 through W10 for 1-time login. Please complete login in the opened browser windows.',
        workers: launched
      });
    }

    const prov = provider || ((parseInt(workerId.replace('W', ''), 10) % 2 === 1) ? 'meta' : 'flow');
    logger.info('WORKER_LOGIN', `Opening interactive login window for ${workerId} (${prov})...`);
    const launchResult = await profileManager.launchWorker(workerId, prov);
    res.json({
      success: true,
      message: `Interactive login browser opened for worker ${workerId} (${prov}). Complete 1-time login in the opened browser window.`,
      details: launchResult
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

new_login_handler = """router.post('/workers/login-assistant', async (req, res) => {
  try {
    const { worker_id = 'W01' } = req.body;
    const workerId = (worker_id || 'W01').toUpperCase();

    if (workerId === 'ALL') {
      logger.info('WORKER_LOGIN', 'Launching all 10 worker profiles (W01–W10) for one-time login with Meta.ai & Flow tabs...');
      const launched = [];
      for (let i = 1; i <= 10; i++) {
        const wId = `W${String(i).padStart(2, '0')}`;
        try {
          const result = await profileManager.launchLoginAssistant(wId);
          launched.push({ workerId: wId, success: true, details: result });
          // Stagger launches by 1.2s so Windows handles the windows smoothly
          await new Promise(r => setTimeout(r, 1200));
        } catch (lErr) {
          logger.warn('WORKER_LOGIN', `Failed launching login window for ${wId}: ${lErr.message}`);
          launched.push({ workerId: wId, success: false, error: lErr.message });
        }
      }
      return res.json({
        success: true,
        message: 'Launched all 10 worker profiles with Meta.ai and Flow tabs open! Please complete login in the opened windows.',
        workers: launched
      });
    }

    logger.info('WORKER_LOGIN', `Opening dedicated login browser for ${workerId} with Meta.ai & Flow tabs...`);
    const launchResult = await profileManager.launchLoginAssistant(workerId);
    res.json({
      success: true,
      message: `Opened browser profile for worker ${workerId} with Meta.ai & Flow tabs open. Log in once to save permanent session.`,
      details: launchResult
    });
  } catch (err) {
    logger.error('WORKER_LOGIN', `Error launching login assistant: ${err.message}`);
    res.status(500).json({ error: err.message });
  }
});

// Stop all running worker browser windows
router.post('/workers/stop-all', async (req, res) => {
  try {
    const result = await profileManager.stopAllWorkers();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Open folder in Windows File Explorer
router.post('/system/open-folder', async (req, res) => {
  try {
    const { folder_type = 'logs', project_id } = req.body;
    const { exec } = require('child_process');
    let targetPath = '';

    if (folder_type === 'logs') {
      targetPath = path.resolve('E:/stickman-video-automation/studio/logs');
    } else if (folder_type === 'renders' && project_id) {
      const proj = await db.get('SELECT directory_path FROM projects WHERE id = ?', [project_id]);
      targetPath = proj ? path.join(proj.directory_path, 'renders') : path.resolve('E:/stickman-video-automation/renders');
    } else if (folder_type === 'workers') {
      targetPath = path.resolve('E:/stickman-video-automation/Workers');
    } else {
      targetPath = path.resolve('E:/stickman-video-automation');
    }

    if (!fs.existsSync(targetPath)) {
      fs.mkdirSync(targetPath, { recursive: true });
    }

    exec(`explorer.exe "${targetPath}"`);
    res.json({ success: true, opened: targetPath });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Test Groq API Key connectivity
router.post('/settings/test-groq', async (req, res) => {
  try {
    const { api_key } = req.body;
    const keyToTest = api_key || (await db.get("SELECT value FROM settings WHERE key = 'groq_api_key'"))?.value;
    if (!keyToTest) return res.status(400).json({ success: false, error: 'No Groq API Key provided or configured' });

    const startTime = Date.now();
    const fetch = global.fetch || require('node-fetch');
    const resp = await fetch('https://api.groq.com/openai/v1/models', {
      headers: { 'Authorization': `Bearer ${keyToTest}` }
    });
    const latency = Date.now() - startTime;

    if (resp.ok) {
      const data = await resp.json();
      const modelCount = data.data ? data.data.length : 0;
      res.json({ success: true, latency_ms: latency, models_available: modelCount, message: `Groq API Key is valid! (${modelCount} models available, Latency: ${latency}ms)` });
    } else {
      const errData = await resp.json().catch(() => ({}));
      res.status(400).json({ success: false, error: errData.error?.message || `Groq API returned HTTP ${resp.status}` });
    }
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Download / Read raw log file
router.get('/logs/raw', (req, res) => {
  const logPath = path.resolve('E:/stickman-video-automation/studio/logs/studio.log');
  if (!fs.existsSync(logPath)) {
    return res.type('text/plain').send('No logs recorded yet.');
  }
  res.sendFile(logPath);
});"""

idx_login = routes_code.find("router.post('/workers/login-assistant'")
if idx_login != -1:
    idx_end = routes_code.find("router.get('/workers'", idx_login)
    if idx_end != -1:
        routes_code = routes_code[:idx_login] + new_login_handler + "\n\n" + routes_code[idx_end:]
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(routes_code)
        print('Successfully replaced login-assistant and added system routes to routes.js')
    else:
        print('Error finding boundary after login-assistant in routes.js')
else:
    print('Error finding login-assistant in routes.js')

print('Profile manager and routes patching complete.')
