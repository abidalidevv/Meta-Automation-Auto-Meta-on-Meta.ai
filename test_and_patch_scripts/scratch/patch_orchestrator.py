import re

filepath = 'E:/stickman-video-automation/studio/server/worker_orchestrator.js'
with open(filepath, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Patch getNextJob to scope to active project and allow unassigned prompts
pattern_get_next = r'async function getNextJob\(workerId, requestedProjectId = null\) \{[\s\S]*?return \{ job: null, status: \'IDLE\' \};\s+\}'

replacement_get_next = '''async function getNextJob(workerId, requestedProjectId = null) {
  const id = workerId.toUpperCase();
  const worker = await db.get(`SELECT * FROM workers WHERE id = ?`, [id]);
  if (!worker) return { job: null, message: 'Worker not registered' };

  if (worker.status === 'LOGIN_REQUIRED') {
    return { job: null, message: 'Login required', status: 'LOGIN_REQUIRED' };
  }

  const now = new Date().toISOString();

  // Resolve target project: explicit or latest ACTIVE
  let targetProjectId = requestedProjectId;
  if (!targetProjectId) {
    const latestActive = await db.get(`SELECT id FROM projects WHERE status = 'ACTIVE' ORDER BY created_at DESC LIMIT 1`);
    if (latestActive) {
      targetProjectId = latestActive.id;
    }
  }

  // 1. Check for active in-flight leased job
  let activeJobQuery = `
    SELECT j.*, p.prompt_text, p.prompt_index, p.prompt_id_str, pr.name as project_name, pr.directory_path
    FROM jobs j
    JOIN prompts p ON j.prompt_id = p.id
    JOIN projects pr ON j.project_id = pr.id
    WHERE j.worker_id = ? AND j.status IN ('ASSIGNED', 'ACKNOWLEDGED', 'GENERATING', 'DOWNLOADING')
      AND j.lease_expires_at > ?
  `;
  const activeParams = [id, now];
  if (targetProjectId) {
    activeJobQuery += ` AND j.project_id = ? `;
    activeParams.push(targetProjectId);
  }
  activeJobQuery += ` ORDER BY j.created_at DESC LIMIT 1 `;
  const activeJob = await db.get(activeJobQuery, activeParams);

  if (activeJob) {
    return {
      job: {
        job_id: activeJob.id,
        project_id: activeJob.project_id,
        project_name: activeJob.project_name,
        prompt_id: activeJob.prompt_id,
        prompt_index: activeJob.prompt_index,
        prompt_id_str: activeJob.prompt_id_str,
        prompt_text: activeJob.prompt_text,
        type: 'PROMPT_GENERATION'
      }
    };
  }

  // 2. High-Priority Repair Queue check (scoped to target project)
  let repairQuery = `
    SELECT p.*, pr.name as project_name, pr.directory_path, pr.character_id
    FROM prompts p
    JOIN projects pr ON p.project_id = pr.id
    WHERE p.status = 'REPAIR_PENDING' AND pr.status = 'ACTIVE'
  `;
  const repairParams = [];
  if (targetProjectId) {
    repairQuery += ` AND p.project_id = ? `;
    repairParams.push(targetProjectId);
  }
  repairQuery += ` ORDER BY pr.created_at DESC, p.prompt_index ASC LIMIT 1 `;
  const repairPrompt = await db.get(repairQuery, repairParams);

  if (repairPrompt) {
    // PRE-FLIGHT CHECK: Ensure character reference is READY for this project
    if (repairPrompt.character_id && (worker.reference_status !== 'READY' || worker.active_project_id !== repairPrompt.project_id)) {
      const charRef = await db.get(`SELECT * FROM character_references WHERE id = ?`, [repairPrompt.character_id]);
      return {
        job: {
          job_id: `ref_init_${Date.now()}`,
          project_id: repairPrompt.project_id,
          character_id: repairPrompt.character_id,
          character_name: charRef ? charRef.character_name : 'Stickman',
          image_url: `/api/v1/projects/${repairPrompt.project_id}/character-reference`,
          type: 'INITIALIZE_REFERENCE'
        }
      };
    }

    const jobId = `job_rep_${Date.now()}_${id}`;
    const leaseExpires = new Date(Date.now() + LEASE_DURATION_SEC * 1000).toISOString();

    await db.run(`
      INSERT INTO jobs (
        id, project_id, prompt_id, worker_id, provider,
        status, lease_owner, lease_expires_at, created_at, updated_at
      ) VALUES (?, ?, ?, ?, ?, 'ASSIGNED', ?, ?, ?, ?)
    `, [jobId, repairPrompt.project_id, repairPrompt.id, id, worker.provider, id, leaseExpires, now, now]);

    await db.run(`
      UPDATE prompts SET status = 'ASSIGNED', assigned_worker_id = ?, updated_at = ? WHERE id = ?
    `, [id, now, repairPrompt.id]);

    await db.run(`UPDATE workers SET active_job_id = ? WHERE id = ?`, [jobId, id]);

    return {
      job: {
        job_id: jobId,
        project_id: repairPrompt.project_id,
        project_name: repairPrompt.project_name,
        prompt_id: repairPrompt.id,
        prompt_index: repairPrompt.prompt_index,
        prompt_id_str: repairPrompt.prompt_id_str,
        prompt_text: repairPrompt.prompt_text,
        type: 'PROMPT_GENERATION'
      }
    };
  }

  // 3. Worker-assigned prompt check
  let nextQuery = `
    SELECT p.*, pr.name as project_name, pr.directory_path, pr.character_id
    FROM prompts p
    JOIN projects pr ON p.project_id = pr.id
    WHERE p.assigned_worker_id = ? AND p.status = 'QUEUED' AND pr.status = 'ACTIVE'
  `;
  const nextParams = [id];
  if (targetProjectId) {
    nextQuery += ` AND p.project_id = ? `;
    nextParams.push(targetProjectId);
  }
  nextQuery += ` ORDER BY pr.created_at DESC, p.prompt_index ASC LIMIT 1 `;
  let nextPrompt = await db.get(nextQuery, nextParams);

  // 4. Fallback: Unassigned prompt check (for Mode 2 or flexible workers)
  if (!nextPrompt) {
    let unassignedQuery = `
      SELECT p.*, pr.name as project_name, pr.directory_path, pr.character_id
      FROM prompts p
      JOIN projects pr ON p.project_id = pr.id
      WHERE (p.assigned_worker_id IS NULL OR p.assigned_worker_id = '') AND p.status = 'QUEUED' AND pr.status = 'ACTIVE'
    `;
    const unassignedParams = [];
    if (targetProjectId) {
      unassignedQuery += ` AND p.project_id = ? `;
      unassignedParams.push(targetProjectId);
    }
    unassignedQuery += ` ORDER BY pr.created_at DESC, p.prompt_index ASC LIMIT 1 `;
    nextPrompt = await db.get(unassignedQuery, unassignedParams);
  }

  if (nextPrompt) {
    if (nextPrompt.character_id && (worker.reference_status !== 'READY' || worker.active_project_id !== nextPrompt.project_id)) {
      const charRef = await db.get(`SELECT * FROM character_references WHERE id = ?`, [nextPrompt.character_id]);
      return {
        job: {
          job_id: `ref_init_${Date.now()}`,
          project_id: nextPrompt.project_id,
          character_id: nextPrompt.character_id,
          character_name: charRef ? charRef.character_name : 'Stickman',
          image_url: `/api/v1/projects/${nextPrompt.project_id}/character-reference`,
          type: 'INITIALIZE_REFERENCE'
        }
      };
    }

    const jobId = `job_${Date.now()}_${id}_${nextPrompt.prompt_id_str}`;
    const leaseExpires = new Date(Date.now() + LEASE_DURATION_SEC * 1000).toISOString();

    await db.run(`
      INSERT INTO jobs (
        id, project_id, prompt_id, worker_id, provider,
        status, lease_owner, lease_expires_at, created_at, updated_at
      ) VALUES (?, ?, ?, ?, ?, 'ASSIGNED', ?, ?, ?, ?)
    `, [jobId, nextPrompt.project_id, nextPrompt.id, id, worker.provider, id, leaseExpires, now, now]);

    await db.run(`
      UPDATE prompts SET status = 'ASSIGNED', assigned_worker_id = ?, updated_at = ? WHERE id = ?
    `, [id, now, nextPrompt.id]);

    await db.run(`UPDATE workers SET active_job_id = ? WHERE id = ?`, [jobId, id]);

    return {
      job: {
        job_id: jobId,
        project_id: nextPrompt.project_id,
        project_name: nextPrompt.project_name,
        prompt_id: nextPrompt.id,
        prompt_index: nextPrompt.prompt_index,
        prompt_id_str: nextPrompt.prompt_id_str,
        prompt_text: nextPrompt.prompt_text,
        type: 'PROMPT_GENERATION'
      }
    };
  }

  return { job: null, status: 'IDLE' };
}'''

# 2. Patch completeJob file search
pattern_complete = r'  // 1\. Physical existence verification[\s\S]*?actualFilePath = found;\s+\}'

replacement_complete = '''  // 1. Physical existence verification across candidate directories
  if (!actualFilePath || !fs.existsSync(actualFilePath)) {
    const project = await db.get('SELECT * FROM projects WHERE id = ?', [job.project_id]);
    const candidates = [
      actualFilePath,
      project ? path.join(project.directory_path, 'central_images', actualFileName) : null,
      path.join(ingestionManager.downloadsDir, actualFileName),
      project ? path.join(ingestionManager.downloadsDir, project.name, actualFileName) : null,
      path.join(ingestionManager.downloadsDir, 'StickmanStudio', actualFileName)
    ].filter(Boolean);

    let found = candidates.find(c => fs.existsSync(c));

    if (!found) {
      // Look for any file starting with prompt_id_str in project and downloads folders
      const searchDirs = [
        project ? path.join(project.directory_path, 'central_images') : null,
        project ? path.join(ingestionManager.downloadsDir, project.name) : null,
        path.join(ingestionManager.downloadsDir, 'StickmanStudio'),
        ingestionManager.downloadsDir
      ].filter(Boolean);

      for (const dir of searchDirs) {
        if (fs.existsSync(dir)) {
          const files = fs.readdirSync(dir);
          const match = files.find(f => f.startsWith(prompt.prompt_id_str) && /\\.(png|jpg|jpeg|webp)$/i.test(f));
          if (match) {
            found = path.join(dir, match);
            actualFileName = match;
            break;
          }
        }
      }
    }

    if (!found) {
      throw new Error(`Cannot complete job ${jobId}: physical image file does not exist on disk at "${actualFilePath}" or in downloads`);
    }
    actualFilePath = found;
  }'''

code = re.sub(pattern_get_next, replacement_get_next, code)
code = re.sub(pattern_complete, replacement_complete, code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: worker_orchestrator.js patched!")
