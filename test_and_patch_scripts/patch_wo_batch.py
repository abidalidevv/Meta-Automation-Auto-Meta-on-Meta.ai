wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """  // 3. Worker-assigned prompt check
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
  }"""

replacement = """  // 3. Worker-assigned prompts check (Batch of up to 50 prompts at once)
  let batchQuery = `
    SELECT p.*, pr.name as project_name, pr.directory_path, pr.character_id
    FROM prompts p
    JOIN projects pr ON p.project_id = pr.id
    WHERE p.assigned_worker_id = ? AND p.status IN ('QUEUED', 'ASSIGNED') AND pr.status = 'ACTIVE'
  `;
  const batchParams = [id];
  if (targetProjectId) {
    batchQuery += ` AND p.project_id = ? `;
    batchParams.push(targetProjectId);
  }
  batchQuery += ` ORDER BY p.prompt_index ASC LIMIT 50 `;
  let assignedPrompts = await db.all(batchQuery, batchParams);

  // 4. Fallback: Unassigned prompts check (for Mode 2 or flexible workers)
  if (!assignedPrompts || assignedPrompts.length === 0) {
    let unassignedQuery = `
      SELECT p.*, pr.name as project_name, pr.directory_path, pr.character_id
      FROM prompts p
      JOIN projects pr ON p.project_id = pr.id
      WHERE (p.assigned_worker_id IS NULL OR p.assigned_worker_id = '') AND p.status IN ('QUEUED', 'ASSIGNED') AND pr.status = 'ACTIVE'
    `;
    const unassignedParams = [];
    if (targetProjectId) {
      unassignedQuery += ` AND p.project_id = ? `;
      unassignedParams.push(targetProjectId);
    }
    unassignedQuery += ` ORDER BY p.prompt_index ASC LIMIT 50 `;
    assignedPrompts = await db.all(unassignedQuery, unassignedParams);
  }

  if (assignedPrompts && assignedPrompts.length > 0) {
    const firstPrompt = assignedPrompts[0];

    // Reference pre-flight check on project
    if (firstPrompt.character_id && (worker.reference_status !== 'READY' || worker.active_project_id !== firstPrompt.project_id)) {
      const charRef = await db.get(`SELECT * FROM character_references WHERE id = ?`, [firstPrompt.character_id]);
      return {
        job: {
          job_id: `ref_init_${Date.now()}`,
          project_id: firstPrompt.project_id,
          character_id: firstPrompt.character_id,
          character_name: charRef ? charRef.character_name : 'Stickman',
          image_url: `/api/v1/projects/${firstPrompt.project_id}/character-reference`,
          type: 'INITIALIZE_REFERENCE'
        }
      };
    }

    const batchId = `batch_${firstPrompt.project_id}_${id}_${Date.now()}`;
    const leaseExpires = new Date(Date.now() + 1800 * 1000).toISOString(); // 30 mins safe lease for batch of 50

    // Register jobs and update prompts for the entire batch
    for (const p of assignedPrompts) {
      const pJobId = `job_${p.project_id}_${id}_${p.prompt_index}`;
      await db.run(`
        INSERT OR REPLACE INTO jobs (
          id, project_id, prompt_id, worker_id, provider,
          status, lease_owner, lease_expires_at, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, 'ASSIGNED', ?, ?, ?, ?)
      `, [pJobId, p.project_id, p.id, id, worker.provider, id, leaseExpires, now, now]);

      await db.run(`
        UPDATE prompts SET status = 'GENERATING', assigned_worker_id = ?, updated_at = ? WHERE id = ?
      `, [id, now, p.id]);
    }

    await db.run(`UPDATE workers SET active_job_id = ?, status = 'BUSY' WHERE id = ?`, [batchId, id]);

    return {
      job: {
        job_id: batchId,
        project_id: firstPrompt.project_id,
        project_name: firstPrompt.project_name,
        prompt_id: firstPrompt.id,
        prompt_index: firstPrompt.prompt_index,
        prompt_id_str: firstPrompt.prompt_id_str,
        prompt_text: firstPrompt.prompt_text,
        total_prompts: assignedPrompts.length,
        prompts: assignedPrompts.map(p => ({
          job_id: `job_${p.project_id}_${id}_${p.prompt_index}`,
          prompt_id: p.id,
          prompt_index: p.prompt_index,
          prompt_id_str: p.prompt_id_str,
          prompt_text: p.prompt_text
        })),
        type: 'PROMPT_GENERATION'
      }
    };
  }"""

assert target in text, "Target not found in worker_orchestrator.js"
new_text = text.replace(target, replacement, 1)

with open(wo_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Successfully patched worker_orchestrator.js with batch prompt dispatch")
