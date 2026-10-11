import os
import sys

routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    code = f.read()

fleet_target = "router.get('/workers/fleet-status', async (req, res) => {"
stop_all_target = "router.post('/workers/stop-all', async (req, res) => {"

idx1 = code.find(fleet_target)
idx2 = code.find(stop_all_target)

if idx1 == -1 or idx2 == -1:
    print(f'Error: Could not find targets: idx1={idx1}, idx2={idx2}')
    sys.exit(1)

new_routes = """router.get('/workers/fleet-status', async (req, res) => {
  try {
    const list = [];
    const workersDir = path.resolve('E:/stickman-video-automation/Workers');
    const dbWorkers = await db.all('SELECT id, provider, status, profile_name FROM workers ORDER BY id ASC');
    const dbMap = {};
    dbWorkers.forEach(w => { dbMap[w.id] = w; });

    for (let i = 1; i <= 10; i++) {
      const id = `W${String(i).padStart(2, '0')}`;
      const dbEntry = dbMap[id];
      const provider = (dbEntry && dbEntry.provider) ? dbEntry.provider.toLowerCase() : ((i % 2 === 1) ? 'flow' : 'meta');
      const profDir = path.join(workersDir, `Worker-${id}`);
      const exists = fs.existsSync(profDir);
      let hasCookies = false;

      if (exists) {
        const cookieFile1 = path.join(profDir, 'Default', 'Network', 'Cookies');
        const cookieFile2 = path.join(profDir, 'Default', 'Cookies');
        hasCookies = fs.existsSync(cookieFile1) || fs.existsSync(cookieFile2);
      }

      const isRunning = profileManager.activeProcesses.has(id);
      const activeInfo = isRunning ? profileManager.activeProcesses.get(id) : null;

      list.push({
        id,
        provider,
        profile_path: profDir,
        directory_exists: exists,
        authenticated: hasCookies,
        is_running: isRunning,
        pid: activeInfo ? activeInfo.pid : null,
        status: isRunning ? 'RUNNING' : (hasCookies ? 'SESSION_SAVED' : 'READY_FOR_SETUP')
      });
    }

    res.json({ success: true, workers: list });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Update a worker's provider (Flow <-> Meta)
router.post('/workers/:id/provider', async (req, res) => {
  try {
    const workerId = req.params.id.toUpperCase();
    const { provider } = req.body;
    const prov = (provider || '').toLowerCase();
    if (!['meta', 'flow'].includes(prov)) {
      return res.status(400).json({ error: "Provider must be 'meta' or 'flow'" });
    }

    const now = new Date().toISOString();
    await db.run('UPDATE workers SET provider = ?, updated_at = ? WHERE id = ?', [
      prov, now, workerId
    ]);

    // Re-provision isolated extension if needed
    try {
      profileManager.prepareWorkerExtension(workerId, prov);
    } catch (e) {
      logger.warn('WORKER_CONFIG', `Warning preparing extension for ${workerId}: ${e.message}`);
    }

    logger.info('WORKER_ORCHESTRATOR', `Updated worker ${workerId} provider to ${prov.toUpperCase()}`);
    res.json({ success: true, workerId, provider: prov });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Launch One-Time Login Assistant (1 Worker = 1 Dedicated Extension & Single URL)
router.post('/workers/login-assistant', async (req, res) => {
  try {
    const { worker_id = 'W01', provider = null } = req.body;
    const workerId = (worker_id || 'W01').toUpperCase();

    if (workerId === 'ALL') {
      logger.info('WORKER_LOGIN', 'Launching all 10 worker profiles (W01–W10) with single dedicated extension & single service...');
      const launched = [];
      const dbWorkers = await db.all('SELECT id, provider FROM workers ORDER BY id ASC');
      const provMap = {};
      dbWorkers.forEach(w => { provMap[w.id] = w.provider; });

      for (let i = 1; i <= 10; i++) {
        const wId = `W${String(i).padStart(2, '0')}`;
        const wProv = provMap[wId] || ((i % 2 === 1) ? 'flow' : 'meta');
        try {
          const result = await profileManager.launchLoginAssistant(wId, wProv);
          launched.push({ workerId: wId, provider: wProv, success: true, details: result });
          // Stagger launches by 1.2s so Windows opens each window smoothly
          await new Promise(r => setTimeout(r, 1200));
        } catch (lErr) {
          logger.warn('WORKER_LOGIN', `Failed launching login window for ${wId}: ${lErr.message}`);
          launched.push({ workerId: wId, provider: wProv, success: false, error: lErr.message });
        }
      }
      return res.json({
        success: true,
        message: 'Launched all 10 worker profiles! Each worker opened with its own dedicated single extension and page (Flow or Meta).',
        workers: launched
      });
    }

    logger.info('WORKER_LOGIN', `Opening dedicated login browser for ${workerId}...`);
    const launchResult = await profileManager.launchLoginAssistant(workerId, provider);
    res.json({
      success: true,
      message: `Opened browser profile for worker ${workerId} (${launchResult.provider.toUpperCase()}) with single dedicated extension.`,
      details: launchResult
    });
  } catch (err) {
    logger.error('WORKER_LOGIN', `Failed to launch login assistant: ${err.message}`);
    res.status(500).json({ error: err.message });
  }
});

"""

code = code[:idx1] + new_routes + code[idx2:]

with open(routes_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('routes.js updated successfully!')
