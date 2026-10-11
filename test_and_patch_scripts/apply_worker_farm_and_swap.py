import re
import os

print("Starting Worker Farm & Step 1 Swap Update...")

# ==============================================================================
# 1. UPDATE routes.js: Add prompt clearing & retry endpoints + ensure 10 workers
# ==============================================================================
routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    routes_code = f.read()

# Add prompt queue actions right after GET /projects/:id/prompts
prompts_routes_to_add = """router.get('/projects/:id/prompts', async (req, res) => {
  try {
    const prompts = await db.all(`
      SELECT * FROM prompts WHERE project_id = ? ORDER BY prompt_index ASC
    `, [req.params.id]);
    res.json(prompts);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Clear failed prompts from project
router.delete('/projects/:id/prompts/failed', async (req, res) => {
  try {
    const delPrompts = await db.run("DELETE FROM prompts WHERE project_id = ? AND status = 'FAILED'", [req.params.id]);
    await db.run("DELETE FROM jobs WHERE project_id = ? AND status = 'FAILED'", [req.params.id]);
    res.json({ success: true, message: 'Cleared all failed prompts from queue' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Retry failed prompts (reset to PENDING)
router.post('/projects/:id/prompts/retry-failed', async (req, res) => {
  try {
    const now = new Date().toISOString();
    await db.run("UPDATE prompts SET status = 'PENDING', worker_id = NULL, error = NULL, updated_at = ? WHERE project_id = ? AND status = 'FAILED'", [now, req.params.id]);
    await db.run("UPDATE jobs SET status = 'PENDING', error = NULL, updated_at = ? WHERE project_id = ? AND status = 'FAILED'", [now, req.params.id]);
    res.json({ success: true, message: 'Reset all failed prompts to PENDING for retry' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Clear all prompts from project queue
router.delete('/projects/:id/prompts/all', async (req, res) => {
  try {
    await db.run("DELETE FROM prompts WHERE project_id = ?", [req.params.id]);
    await db.run("DELETE FROM jobs WHERE project_id = ?", [req.params.id]);
    res.json({ success: true, message: 'All prompts cleared from queue' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

old_prompts_get = """router.get('/projects/:id/prompts', async (req, res) => {
  try {
    const prompts = await db.all(`
      SELECT * FROM prompts WHERE project_id = ? ORDER BY prompt_index ASC
    `, [req.params.id]);
    res.json(prompts);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

if old_prompts_get in routes_code and "router.delete('/projects/:id/prompts/failed'" not in routes_code:
    routes_code = routes_code.replace(old_prompts_get, prompts_routes_to_add)

# Ensure 10 workers in GET /workers
workers_get_replacement = """router.get('/workers', async (req, res) => {
  try {
    const existing = await db.all(`SELECT id FROM workers`);
    const existingSet = new Set(existing.map(w => w.id));
    const now = new Date().toISOString();
    for (let i = 1; i <= 10; i++) {
      const wId = `W${String(i).padStart(2, '0')}`;
      if (!existingSet.has(wId)) {
        const provider = (i % 2 === 1) ? 'flow' : 'meta';
        const profile = `Worker-${String(i).padStart(2, '0')}`;
        await db.run(`
          INSERT INTO workers (id, provider, status, profile_name, profile_path, reference_status, active_character_version, last_heartbeat, registered_at, updated_at)
          VALUES (?, ?, 'OFFLINE', ?, ?, 'NOT_READY', 0, ?, ?, ?)
        `, [wId, provider, profile, `Workers/${profile}`, now, now, now]);
      }
    }
    const workers = await db.all(`SELECT * FROM workers ORDER BY id ASC`);
    res.json(workers);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

routes_code = re.sub(
    r"router\.get\('/workers',\s*async\s*\(req,\s*res\)\s*=>\s*\{[\s\S]*?res\.json\(workers\);\s*\}\s*catch[\s\S]*?\}\s*\}\);",
    lambda m: workers_get_replacement,
    routes_code
)

with open(routes_path, 'w', encoding='utf-8') as f:
    f.write(routes_code)
print("Updated routes.js!")

# ==============================================================================
# 2. UPDATE app_v2.js: loadFleetCalculation, goToStep, queue handlers
# ==============================================================================
app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    app_code = f.read()

# Fix loadFleetCalculation to target exact IDs
new_fleet_calc = """async function loadFleetCalculation() {
  const elP = document.getElementById('fleetTotalPrompts');
  const elW = document.getElementById('fleetTotalWorkers');
  const elM = document.getElementById('fleetMetaWorkers');
  const elF = document.getElementById('fleetFlowWorkers');
  const elA = document.getElementById('fleetActiveQueued');
  const elExp = document.getElementById('fleetFormulaExplanation');

  if (!activeProjectId) {
    if (elP) elP.textContent = '0';
    if (elW) elW.textContent = '0';
    if (elM) elM.textContent = '0';
    if (elF) elF.textContent = '0';
    if (elA) elA.textContent = '0 / 0';
    if (elExp) elExp.textContent = 'Select or create a project first.';
    return;
  }

  try {
    const res = await fetch(`/api/v1/projects/${activeProjectId}/workers/calculate-fleet`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quota_per_worker: 50, max_concurrent: 10 })
    });
    const data = await res.json();
    if (!data.success) return;

    if (elP) elP.textContent = data.total_prompts;
    if (elW) elW.textContent = data.total_workers_needed;
    if (elM) elM.textContent = data.meta_workers;
    if (elF) elF.textContent = data.flow_workers;
    if (elA) elA.textContent = `${data.active_now_batch_1} Active / ${data.queued_for_recycle} Queued`;
    if (elExp) {
      if (data.total_prompts === 0) {
        elExp.textContent = 'Project prompt queue is currently empty. Go to Step 1 to import or generate prompts.';
      } else {
        elExp.textContent = `${data.total_prompts} Prompts → ${data.total_workers_needed} Workers (${data.meta_workers} Meta + ${data.flow_workers} Flow). ${data.total_batches > 1 ? data.total_batches + ' Batches' : '1 Batch (Max 10 concurrent)'}.`;
      }
    }
  } catch (err) {
    console.warn('loadFleetCalculation error:', err);
  }
}"""

app_code = re.sub(
    r"async function loadFleetCalculation\(\)\s*\{[\s\S]*?console\.warn\('loadFleetCalculation error:', err\);\s*\}\s*\}",
    lambda m: new_fleet_calc,
    app_code
)

# Update goToStep to call loadFleetCalculation on step 2
app_code = re.sub(
    r"if \(stepNum === 2\) refreshWorkers\(\);",
    "if (stepNum === 2) { refreshWorkers(); loadFleetCalculation(); }",
    app_code
)

# Also ensure loadFleetCalculation is called inside loadProjectPrompts
if "loadFleetCalculation();" not in app_code[app_code.find('async function loadProjectPrompts'):app_code.find('async function loadProjectPrompts')+1200]:
    app_code = app_code.replace(
        "document.getElementById('promptsCountBadge').textContent = `${prompts.length} Prompts`;",
        "document.getElementById('promptsCountBadge').textContent = `${prompts.length} Prompts`;\n    loadFleetCalculation();"
    )

# Add queue clear & retry helpers to app_v2.js
queue_helpers = """
// --- PROMPT QUEUE ACTION HELPERS ---
async function retryFailedPrompts() {
  if (!activeProjectId) {
    showToast('Select an active project first', 'warn');
    return;
  }
  try {
    const res = await fetch(`/api/v1/projects/${activeProjectId}/prompts/retry-failed`, { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message || 'Failed prompts reset to PENDING!', 'success');
      await loadProjectPrompts();
      await loadFleetCalculation();
    } else {
      showToast(data.error || 'Failed to retry prompts', 'error');
    }
  } catch (err) {
    showToast(`Retry error: ${err.message}`, 'error');
  }
}

async function clearFailedPrompts() {
  if (!activeProjectId) {
    showToast('Select an active project first', 'warn');
    return;
  }
  if (!confirm('Are you sure you want to delete all failed prompts from this project?')) return;
  try {
    const res = await fetch(`/api/v1/projects/${activeProjectId}/prompts/failed`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast(data.message || 'Failed prompts cleared!', 'success');
      await loadProjectPrompts();
      await loadFleetCalculation();
    } else {
      showToast(data.error || 'Failed to clear prompts', 'error');
    }
  } catch (err) {
    showToast(`Clear error: ${err.message}`, 'error');
  }
}

async function clearAllPromptsQueue() {
  if (!activeProjectId) {
    showToast('Select an active project first', 'warn');
    return;
  }
  if (!confirm('Are you sure you want to clear ALL prompts from this project queue?')) return;
  try {
    const res = await fetch(`/api/v1/projects/${activeProjectId}/prompts/all`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast('All prompts cleared from queue', 'success');
      await loadProjectPrompts();
      await loadFleetCalculation();
    } else {
      showToast(data.error || 'Failed to clear prompts', 'error');
    }
  } catch (err) {
    showToast(`Clear error: ${err.message}`, 'error');
  }
}
"""

if "function retryFailedPrompts" not in app_code:
    app_code += "\n" + queue_helpers

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_code)
print("Updated app_v2.js!")

# ==============================================================================
# 3. UPDATE index.html: Swap Mode 1 & Mode 2, and add Prompt Queue buttons
# ==============================================================================
index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the entire Step 1 Panel with the cleanly swapped structure
# Mode 1 = Clean Prompt List Importer (active)
# Mode 2 = Groq AI Story Engine (hidden by default)
# Prompts Queue = With Clear Failed / Retry Failed / Clear All buttons

step1_start_marker = '<!-- ==================== STEP 1: STORY & PROMPTS ==================== -->'
step2_start_marker = '<section id="step-2-panel"'

p1 = html.find(step1_start_marker)
p2 = html.find(step2_start_marker)

if p1 == -1 or p2 == -1:
    print(f"Error finding markers: p1={p1}, p2={p2}")
else:
    new_step1_html = """<!-- ==================== STEP 1: STORY & PROMPTS ==================== -->
        <section id="step-1-panel" class="view-panel active">
          
          <!-- Sub Tabs to switch between Mode 1 (Importer), Mode 2 (Groq AI), and Prompts Queue -->
          <div class="sub-tabs-bar">
            <button id="subTabMode1" class="sub-tab-btn active" onclick="switchStep1SubTab('mode1')">
              <span>📋</span> Mode 1: Clean Prompt List Importer
            </button>
            <button id="subTabMode2" class="sub-tab-btn" onclick="switchStep1SubTab('mode2')">
              <span>⚡</span> Mode 2: Groq AI Story Engine
            </button>
            <button id="subTabPromptsQueue" class="sub-tab-btn" onclick="switchStep1SubTab('queue')">
              <span>📑</span> Project Prompts Queue (<span id="promptsSubTabCount">0</span>)
            </button>
          </div>

          <!-- SUB VIEW A: MODE 1 CLEAN PROMPT LIST IMPORTER (NOW DEFAULT / 1ST) -->
          <div id="subViewMode1" class="sub-view-content" style="display: block;">
            <div class="card">
              <div class="card-header">
                <div class="card-title-group">
                  <div class="card-icon">📋</div>
                  <div>
                    <div class="card-title">Mode 1: Clean Prompt List Importer</div>
                    <div class="card-subtitle">Import sequential 001_... formatted prompt lists directly into the production database</div>
                  </div>
                </div>
                <div style="display: flex; gap: 8px;">
                  <input type="file" id="m2FileInput" accept=".txt,.md,.json" style="display: none;" onchange="handleM2FileUpload(this)" />
                  <button class="btn btn-secondary" onclick="document.getElementById('m2FileInput').click()" style="font-size: 12px; padding: 6px 12px;" title="Upload a text or markdown file containing your pre-written prompt list">
                    📁 Import Prompts from File (.txt / .md)
                  </button>
                </div>
              </div>

              <!-- Mode 1 Audio & Matching Voiceover Sync -->
              <div style="background: rgba(10, 14, 24, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 18px;">
                <div style="font-size: 12px; font-weight: 800; color: var(--cyan); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">
                  🎙️ Matching Voiceover Audio & BGM
                </div>
                <div class="grid-2">
                  <div class="form-group">
                    <label class="form-label">Voiceover Audio File / Path</label>
                    <div style="display: flex; gap: 8px;">
                      <input type="file" id="m2VoiceoverFile" accept="audio/*" class="form-input" style="flex: 1;" onchange="handleM2VoiceoverFile(this)" />
                      <input type="hidden" id="m2VoiceoverPath" /><div id="m2VoiceoverStatus" class="file-picked-chip" style="display: none;"></div>
                    </div>
                  </div>

                  <div class="form-group">
                    <label class="form-label">Duration & Auto-Detection</label>
                    <div style="display: flex; gap: 8px; align-items: center;">
                      <button type="button" class="btn btn-secondary" onclick="autoDetectM2Voiceover()" style="white-space: nowrap; font-size: 12px; padding: 8px 12px;">
                        ⚡ Auto-Detect
                      </button>
                      <input type="number" id="m2Duration" class="form-input" value="72" step="0.5" style="width: 100px;" />
                      <span id="m2DurationBadge" class="brand-badge" style="white-space: nowrap;">72.0s</span>
                    </div>
                  </div>
                </div>

                <div class="grid-2" style="margin-top: 10px;">
                  <div class="form-group">
                    <label class="form-label">Pacing Preset</label>
                    <select id="m2Pacing" class="form-select">
                      <option value="Random" selected>🎲 Random / Dynamic (Anti-Template YouTube Pacing)</option>
                      <option value="3/4s">3 images / 4 sec (0.75x - Dynamic Story Recommended)</option>
                      <option value="2/4s">2 images / 4 sec (0.50x - YouTube Standard)</option>
                      <option value="1/4s">1 image / 4 sec (0.25x - Cinematic)</option>
                      <option value="4/4s">4 images / 4 sec (1.00x - Fast-Paced)</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label class="form-label">
                      BGM Volume: <span id="m2MusicVolLabel" style="color: var(--cyan); font-weight: 700;">7%</span>
                    </label>
                    <div style="display: flex; gap: 8px; align-items: center;">
                      <input type="hidden" id="m2MusicPath" />
                      <input type="range" id="m2MusicVol" min="0" max="100" value="7" style="width: 90px;" oninput="document.getElementById('m2MusicVolLabel').textContent = this.value + '%'" />
                    </div>
                  </div>
                </div>

                <!-- Live Audio Forecast Card Mode 1 -->
                <div class="audio-forecast-card" id="m2ForecastCard">
                  <div class="forecast-item">
                    <span class="forecast-title">Audio Duration</span>
                    <span class="forecast-value text-emerald" id="m2ForecastDur">72.0s</span>
                  </div>
                  <div class="forecast-arrow">→</div>
                  <div class="forecast-item">
                    <span class="forecast-title">Pacing Rule</span>
                    <span class="forecast-value" id="m2ForecastPacing">🎲 Dynamic Anti-Template (~2.00s/img)</span>
                  </div>
                  <div class="forecast-arrow">→</div>
                  <div class="forecast-item highlight">
                    <span class="forecast-title">Expected Prompts</span>
                    <span class="forecast-value" id="m2ForecastCount">36 Prompts Expected</span>
                  </div>
                </div>
              </div>

              <!-- Prompts Input Textarea -->
              <div class="form-group">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <label class="form-label" style="margin-bottom: 0;">Paste Raw Prompts (1 per line with 001_ prefix)</label>
                  <span id="m2PromptCountBadge" class="brand-badge">0 prompts</span>
                </div>
                <textarea id="rawPromptsInput" class="form-textarea" placeholder="001_A simple stickman standing in a dark room&#10;002_The stickman looks up at a glowing neon star&#10;003_The stickman begins to run towards the light..." style="min-height: 220px;" oninput="updateM2PromptCount()"></textarea>
              </div>

              <div style="display: flex; gap: 12px;">
                <button class="btn btn-primary" onclick="importRawPrompts()" style="padding: 12px 24px; font-size: 14px; font-weight: 800;">
                  📋 Validate & Import Prompts
                </button>
              </div>
            </div>
          </div>

          <!-- SUB VIEW B: MODE 2 GROQ AI STORY ENGINE (NOW 2ND SUB-TAB) -->
          <div id="subViewMode2" class="sub-view-content" style="display: none;">
            <div class="card">
              <div class="card-header">
                <div class="card-title-group">
                  <div class="card-icon">⚡</div>
                  <div>
                    <div class="card-title">Mode 2: Groq AI Story Engine</div>
                    <div class="card-subtitle">Generate complete sequential stickman prompts from story script with character consistency</div>
                  </div>
                </div>
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                  <span class="brand-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--emerald); border-color: rgba(16, 185, 129, 0.3);">⚡ Groq: llama-3.3-70b (Auto Fallbacks)</span>
                  <span id="m1PromptEstimateBadge" class="brand-badge">~683 stickman prompts</span>
                  <select id="m1ModelSelect" style="display: none;"></select>
                </div>
              </div>

              <!-- Row 1: Video Title (Left) + Voiceover Audio File & Auto Duration (Right) -->
              <div class="grid-2" style="margin-bottom: 14px;">
                <div class="form-group" style="margin-bottom: 0;">
                  <label class="form-label">Video Title</label>
                  <input type="text" id="m1VideoTitle" class="form-input" placeholder="e.g. The Untold Story of the Stickman Kingdom" />
                </div>

                <div class="form-group" style="margin-bottom: 0;">
                  <label class="form-label" style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Voiceover Audio File / Path</span>
                    <span id="m1DurationBadge" class="brand-badge" style="white-space: nowrap; font-size: 11px; padding: 2px 8px; color: var(--emerald); border-color: rgba(16, 185, 129, 0.3);">Auto Duration Ready</span>
                  </label>
                  <div style="display: flex; gap: 8px; align-items: center;">
                    <input type="file" id="m1VoiceoverFile" accept="audio/*" class="form-input" style="flex: 1;" onchange="handleM1VoiceoverFile(this)" />
                    <input type="hidden" id="m1VoiceoverPath" />
                    <input type="number" id="m1Duration" class="form-input" value="72" step="0.5" oninput="updateM1PromptEstimate()" style="width: 85px; text-align: center;" title="Voiceover Duration (Seconds)" />
                    <span style="font-size: 12px; color: var(--text-muted); font-weight: 600;">sec</span>
                  </div>
                  <div id="m1VoiceoverStatus" class="file-picked-chip" style="display: none; margin-top: 6px;"></div>
                </div>
              </div>

              <!-- Row 2: Pacing (Left) + Background Music (Middle) + BGM Volume (Right) -->
              <div class="grid-3" style="margin-bottom: 16px;">
                <div class="form-group" style="margin-bottom: 0;">
                  <label class="form-label">Pacing Rhythm</label>
                  <select id="m1Pacing" class="form-select" onchange="updateM1PromptEstimate()">
                    <option value="Random" selected>🎲 Random / Dynamic (Anti-Template YouTube Pacing)</option>
                    <option value="3/4s">3 images / 4 sec (0.75x - Dynamic Story)</option>
                    <option value="2/4s">2 images / 4 sec (0.50x - YouTube Standard)</option>
                    <option value="1/4s">1 image / 4 sec (0.25x - Relaxed / Cinematic)</option>
                    <option value="4/4s">4 images / 4 sec (1.00x - Fast-Paced Action)</option>
                    <option value="5/4s">5 images / 4 sec (1.25x - Hyper Energetic)</option>
                  </select>
                </div>

                <div class="form-group" style="margin-bottom: 0;">
                  <label class="form-label">Background Music (Optional)</label>
                  <div style="display: flex; gap: 8px;">
                    <input type="file" id="m1MusicFile" accept="audio/*" class="form-input" style="flex: 1; padding: 6px 10px;" onchange="handleM1MusicFile(this)" />
                    <input type="hidden" id="m1MusicPath" />
                  </div>
                  <div id="m1MusicStatus" class="file-picked-chip" style="display: none; margin-top: 4px;"></div>
                </div>

                <div class="form-group" style="margin-bottom: 0;">
                  <label class="form-label" style="display: flex; justify-content: space-between;">
                    <span>BGM Volume</span>
                    <span id="m1MusicVolLabel" style="color: var(--cyan); font-weight: 700;">7% (Auto-Ducked)</span>
                  </label>
                  <input type="range" id="m1MusicVol" min="0" max="100" value="7" class="form-input" style="padding: 4px 0; height: 38px;" oninput="updateM1MusicVolume(this.value)" />
                </div>
              </div>

              <!-- Live Audio Pacing & Generation Forecast Banner -->
              <div class="audio-forecast-card" id="m1ForecastCard" style="margin-bottom: 18px;">
                <div class="forecast-item">
                  <span class="forecast-title">Audio Duration</span>
                  <span class="forecast-value text-emerald" id="m1ForecastDur">72.0s</span>
                </div>
                <div class="forecast-arrow">→</div>
                <div class="forecast-item">
                  <span class="forecast-title">Pacing Rule</span>
                  <span class="forecast-value" id="m1ForecastPacing">🎲 Dynamic Anti-Template (~2.00s/img)</span>
                </div>
                <div class="forecast-arrow">→</div>
                <div class="forecast-item highlight">
                  <span class="forecast-title">Target Generation</span>
                  <span class="forecast-value" id="m1ForecastCount">36 Scenes (36 Prompts &amp; 36 Images)</span>
                </div>
              </div>

              <!-- Character Reference Consistency Box -->
              <div style="background: rgba(10, 14, 24, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 14px; margin-bottom: 18px;">
                <div style="font-size: 12px; font-weight: 800; color: var(--violet); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                  <span>🎭 Character Reference &amp; Visual Consistency</span>
                  <span id="m1CharBadge" class="brand-badge" style="background: rgba(139, 92, 246, 0.15); color: #c4b5fd;">Consistency Active</span>
                </div>

                <div class="char-ref-picker-card" style="margin-bottom: 8px;">
                  <div class="char-ref-thumb-box" id="m1CharThumbBox">
                    <span class="char-ref-thumb-placeholder" id="m1CharPlaceholder">🎭</span>
                    <img id="m1CharThumb" class="char-ref-thumb-img" alt="Character Reference" />
                  </div>
                  <div class="char-ref-meta">
                    <div class="char-ref-name">Stickman Protagonist Reference Image</div>
                    <div class="char-ref-status" id="m1CharStatusText">Upload or pick reference image to lock character appearance and linework across all scenes</div>
                    <div style="display: flex; gap: 8px; margin-top: 6px;">
                      <input type="file" id="m1CharFile" accept="image/*" style="display: none;" onchange="handleM1CharFile(this)" />
                      <button type="button" class="btn btn-secondary" onclick="document.getElementById('m1CharFile').click()" style="font-size: 11.5px; padding: 6px 14px; cursor: pointer;">
                        🖼️ Pick Reference Image
                      </button>
                      <button type="button" class="btn btn-secondary" id="m1CharRemoveBtn" onclick="removeM1CharImage()" style="font-size: 11.5px; padding: 6px 12px; display: none; color: var(--rose); cursor: pointer;">
                        ✕ Remove
                      </button>
                    </div>
                  </div>
                </div>

                <details style="margin-top: 8px; background: rgba(0,0,0,0.25); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); padding: 10px 14px;">
                  <summary style="font-size: 11.5px; font-weight: 700; color: var(--text-muted); cursor: pointer;">
                    ⚙️ Advanced Character Details (Optional - Pre-filled Stickman Defaults)
                  </summary>
                  <div style="margin-top: 10px;">
                    <div class="grid-2">
                      <div class="form-group">
                        <label class="form-label">Character Name</label>
                        <input type="text" id="m1CharacterName" class="form-input" value="Main Stickman" />
                      </div>
                      <div class="form-group">
                        <label class="form-label">Character Visual Consistency Prompt Anchor</label>
                        <input type="text" id="m1CharacterRef" class="form-input" value="Minimalist 2D hand-drawn stickman hero, clean black ink outlines, solid pure white background" />
                      </div>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                      <label class="form-label">Recurring Visual Elements &amp; Atmosphere</label>
                      <input type="text" id="m1VisualElements" class="form-input" placeholder="e.g. Glowing neon sword, blackboard sketch style, chalk arrows..." />
                    </div>
                  </div>
                </details>
              </div>

              <!-- Voiceover Script Input -->
              <div class="form-group" style="margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <label class="form-label" style="margin-bottom: 0;">Story / Voiceover Script</label>
                  <div style="display: flex; align-items: center; gap: 10px;">
                    <input type="file" id="m1ScriptFile" accept=".txt,.text,.md" style="display: none;" onchange="handleScriptFile(this, 'm1')" />
                    <button type="button" class="btn btn-secondary" onclick="document.getElementById('m1ScriptFile').click()" style="font-size: 11px; padding: 4px 12px; cursor: pointer;">
                      📁 Pick .txt Script File
                    </button>
                    <span id="m1WordCountLabel" style="color: var(--cyan); font-weight: 700; font-size: 12px;">0 words</span>
                  </div>
                </div>
                <textarea id="m1ScriptInput" class="form-textarea" placeholder="Paste your complete story or voiceover script here, or click 'Pick .txt Script File'..." oninput="updateM1ScriptWordCount()" style="min-height: 150px;"></textarea>
              </div>

              <!-- Master Directive Info Bar (story to prompts.md default) -->
              <div style="background: rgba(10, 14, 24, 0.6); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 10px 14px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span style="font-size: 13px;">📄</span>
                  <span style="font-size: 12px; font-weight: 700; color: #fff;">Master Directive:</span>
                  <span id="m1DirectiveStatusBadge" class="brand-badge" style="background: rgba(0, 240, 255, 0.1); color: var(--cyan); border-color: rgba(0, 240, 255, 0.25); font-size: 11px;">
                    story to prompts.md (Canonical V7 Locked)
                  </span>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <input type="file" id="m1MasterPromptFile" accept=".md,.txt" style="display: none;" onchange="handleMasterPromptFile(this)" />
                  <button type="button" class="btn btn-secondary" onclick="document.getElementById('m1MasterPromptFile').click()" style="font-size: 11px; padding: 4px 10px; cursor: pointer;">
                    📂 Pick Custom .md Directive
                  </button>
                  <button type="button" class="btn btn-secondary" onclick="toggleDirectivePreview()" style="font-size: 11px; padding: 4px 10px; cursor: pointer;">
                    👁️ View / Edit Directive
                  </button>
                </div>
              </div>

              <div id="m1DirectiveBox" style="display: none; margin-bottom: 18px;">
                <textarea id="m1MasterPrompt" class="form-textarea" style="font-family: var(--font-mono); font-size: 11.5px; min-height: 130px;"></textarea>
              </div>

              <button id="btnM1Generate" class="btn btn-primary" onclick="triggerMode1Generate()" style="width: 100%; justify-content: center; padding: 14px; font-size: 15px; font-weight: 800;">
                <span>✨</span> Generate Sequential Story Prompts
              </button>

              <!-- Animated Progress Indicator -->
              <div id="m1ProgressBox" style="display: none; margin-top: 18px;">
                <div style="height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden;">
                  <div id="m1ProgressBar" style="width: 0%; height: 100%; background: var(--grad-brand); transition: width 0.4s ease;"></div>
                </div>
                <div id="m1ProgressStatus" style="font-size: 12px; color: var(--cyan); margin-top: 8px; font-family: var(--font-mono);">Generating...</div>
              </div>

              <!-- Output Prompts Canvas (Shown after generation) -->
              <div id="m1OutputCanvasBox" style="display: none; margin-top: 22px; background: rgba(10, 14, 24, 0.85); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: var(--radius-sm); padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                  <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-weight: 800; color: #fff; font-size: 14px;">✨ Generated Prompts Canvas</span>
                    <span id="m1CanvasCountBadge" class="brand-badge text-emerald" style="border-color: rgba(16, 185, 129, 0.3);">0 Scenes</span>
                  </div>
                  <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button type="button" class="btn btn-secondary" onclick="copyM1PromptsCanvas()" style="font-size: 12px; padding: 6px 14px; cursor: pointer;">
                      📋 Copy All Prompts
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="downloadM1PromptsFile()" style="font-size: 12px; padding: 6px 14px; cursor: pointer;">
                      💾 Download .txt
                    </button>
                    <button type="button" class="btn btn-primary" onclick="proceedFromM1ToWorkerFarm()" style="font-size: 12px; padding: 6px 16px; cursor: pointer;">
                      🚀 Proceed to Worker Farm →
                    </button>
                  </div>
                </div>
                <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 8px;">
                  Generated prompts ready for Worker Farm execution or export. Edit any line if needed:
                </div>
                <textarea id="m1OutputCanvasText" class="form-textarea" style="font-family: var(--font-mono); font-size: 12px; line-height: 1.5; min-height: 240px; background: rgba(5, 7, 13, 0.95);"></textarea>
              </div>

              <!-- Story Bible Card -->
              <div id="m1BibleBox" style="display: none; margin-top: 18px; background: rgba(139, 92, 246, 0.12); border: 1px solid rgba(139, 92, 246, 0.35); border-radius: var(--radius-sm); padding: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <div style="font-weight: 800; color: #c4b5fd; font-size: 14px;">📖 Story Bible Generated:</div>
                  <button class="btn btn-emerald" onclick="proceedFromM1ToWorkerFarm()" style="font-size: 11.5px; padding: 5px 12px;">🚀 Open Worker Farm</button>
                </div>
                <div style="font-size: 13px; color: var(--text-muted);"><strong style="color: #fff;">Protagonist:</strong> <span id="m1BibleProtagonist"></span></div>
                <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;"><strong style="color: #fff;">Setting:</strong> <span id="m1BibleSetting"></span></div>
              </div>
            </div>
          </div>

          <!-- SUB VIEW C: PROJECT PROMPTS QUEUE (NOW WITH CLEAR & RETRY BUTTONS) -->
          <div id="subViewQueue" class="sub-view-content" style="display: none;">
            <div class="card">
              <div class="card-header">
                <div class="card-title-group">
                  <div class="card-icon">📑</div>
                  <div>
                    <div class="card-title">Active Project Prompts Queue</div>
                    <div class="card-subtitle">Sequential Stickman Generation Queue and Worker Allocation</div>
                  </div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                  <span id="promptsCountBadge" class="brand-badge">0 Prompts</span>
                  <button type="button" class="btn btn-secondary" onclick="retryFailedPrompts()" style="font-size: 11.5px; padding: 5px 12px; color: var(--amber); cursor: pointer;" title="Reset all failed prompts back to PENDING status">
                    ↻ Retry Failed Prompts
                  </button>
                  <button type="button" class="btn btn-secondary" onclick="clearFailedPrompts()" style="font-size: 11.5px; padding: 5px 12px; color: var(--rose); cursor: pointer;" title="Remove failed prompts from this project">
                    ✕ Clear Failed Prompts
                  </button>
                  <button type="button" class="btn btn-secondary" onclick="clearAllPromptsQueue()" style="font-size: 11.5px; padding: 5px 12px; color: var(--rose); cursor: pointer;" title="Clear all prompts from this project queue">
                    🗑️ Clear All Prompts
                  </button>
                </div>
              </div>

              <div id="promptListContainer" class="prompt-list-wrap">
                <div style="color: var(--text-dim); padding: 24px; text-align: center;">Select or create a project to inspect prompts.</div>
              </div>
            </div>
          </div>
        </section>
        \n        """

    html = html[:p1] + new_step1_html + html[p2:]
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html Step 1 panel!")

print("All updates applied successfully!")
