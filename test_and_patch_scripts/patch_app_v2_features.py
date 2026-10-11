import os

app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Patch resolveMediaUrl
old_resolve = """function resolveMediaUrl(filePath) {
  if (!filePath) return '';
  if (filePath.startsWith('http://') || filePath.startsWith('https://') || filePath.startsWith('data:')) return filePath;
  const normalized = filePath.replace(/\\\\/g, '/');
  const projIdx = normalized.indexOf('/Projects/');
  if (projIdx !== -1) {
    return '/projects-media/' + normalized.substring(projIdx + 10);
  }
  const folderName = currentProjectData?.directory_path ? currentProjectData.directory_path.replace(/\\\\/g, '/').split('/').pop() : currentProjectData?.name;
  return `/projects-media/${folderName}/${filePath.replace(/^\\/+/, '')}`;
}"""

new_resolve = """function resolveMediaUrl(filePath, context = null) {
  const pId = activeProjectId || (currentProjectData && currentProjectData.id);

  // If a scene or prompt object with index is provided, use prompt image API directly
  if (context && (context.prompt_index || context.order_index) && pId) {
    const pIdx = context.prompt_index || context.order_index;
    return `/api/v1/projects/${pId}/prompts/${pIdx}/image?v=${encodeURIComponent(context.file_name || context.updated_at || Date.now())}`;
  }

  if (!filePath) return '';
  if (filePath.startsWith('http://') || filePath.startsWith('https://') || filePath.startsWith('data:')) return filePath;

  const normalized = filePath.replace(/\\\\/g, '/');
  const baseName = normalized.split('/').pop() || '';

  // If filename starts with 001_ or similar prompt number, map directly to prompt image API
  const pMatch = baseName.match(/^(\\d{1,4})_/);
  if (pMatch && pId) {
    const pIdx = parseInt(pMatch[1], 10);
    return `/api/v1/projects/${pId}/prompts/${pIdx}/image?v=${encodeURIComponent(baseName)}`;
  }

  // Case-insensitive /projects/ extraction
  const projIdx = normalized.toLowerCase().indexOf('/projects/');
  if (projIdx !== -1) {
    return '/projects-media/' + normalized.substring(projIdx + 10);
  }

  const folderName = currentProjectData?.directory_path ? currentProjectData.directory_path.replace(/\\\\/g, '/').split('/').pop() : currentProjectData?.name;
  return `/projects-media/${folderName}/${filePath.replace(/^\\/+/, '')}`;
}"""

assert old_resolve in text, "old_resolve not found in app_v2.js"
text = text.replace(old_resolve, new_resolve, 1)

# 2. Patch renderCapCutTimeline to pass scene to resolveMediaUrl
old_scene_thumb = "const thumbUrl = resolveMediaUrl(scene.image_path || scene.file_path);"
new_scene_thumb = "const thumbUrl = resolveMediaUrl(scene.image_path || scene.file_path, scene);"
assert old_scene_thumb in text, "old_scene_thumb not found in app_v2.js"
text = text.replace(old_scene_thumb, new_scene_thumb)

# 3. Patch goToStep stepNum === 4 to default to captions tab
old_step4 = "if (stepNum === 4) loadTimeline();"
new_step4 = "if (stepNum === 4) { loadTimeline(); if (typeof switchToolsTab === 'function') switchToolsTab('captions'); }"
assert old_step4 in text, "old_step4 not found in app_v2.js"
text = text.replace(old_step4, new_step4, 1)

# 4. Add window.startMode1Generating implementation
start_generating_code = """
// =============================================
// MODE 1 & 2: 1-CLICK FLEET DISPATCH & AUTO-START
// =============================================
window.startMode1Generating = async function() {
  const pId = activeProjectId || (currentProjectData && currentProjectData.id);
  if (!pId) {
    showToast('Select or create an active project first', 'warn');
    return;
  }

  const rawInput = document.getElementById('rawPromptsInput');
  const rawText = rawInput ? rawInput.value.trim() : '';

  // 1. If prompts are pasted in the raw input box, validate and import them first
  if (rawText) {
    showToast('Validating & importing prompts...', 'info');
    try {
      const importRes = await fetch(`/api/v1/projects/${pId}/prompts/import`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_prompts: rawText })
      });
      const importData = await importRes.json();
      if (!importData.success) {
        const errMsg = (importData.errors && importData.errors.length) ? importData.errors.join(', ') : (importData.error || 'Failed to import prompts');
        showToast(`Validation error: ${errMsg}`, 'error');
        return;
      }
      showToast(`Imported ${importData.count} prompts!`, 'success');
      rawInput.value = '';
    } catch (err) {
      showToast(`Import error: ${err.message}`, 'error');
      return;
    }
  }

  // 2. Verify project has prompts in queue
  try {
    const promptsRes = await fetch(`/api/v1/projects/${pId}/prompts`);
    const promptsData = await promptsRes.json();
    const promptList = Array.isArray(promptsData) ? promptsData : (promptsData.prompts || []);
    const promptsCount = promptList.length;

    if (promptsCount === 0) {
      showToast('No prompts in project. Please paste or generate prompts first.', 'warn');
      return;
    }

    const startBtn = document.getElementById('btnM1StartGenerating');
    if (startBtn) {
      startBtn.disabled = true;
      startBtn.innerHTML = '<span>⏳</span> Spawning Fleet & Launching Browsers...';
    }

    showToast(`🚀 Auto-dispatching fleet for ${promptsCount} prompts...`, 'info');

    // 3. Dispatch fleet with auto_launch = true (Auto spawns Chrome profiles with isolated extensions)
    const dispatchRes = await fetch(`/api/v1/projects/${pId}/workers/dispatch-fleet`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        quota_per_worker: 50,
        max_concurrent: 10,
        auto_launch: true
      })
    });
    const dispatchData = await dispatchRes.json();

    if (dispatchData.success) {
      const activeCount = dispatchData.active_batch_1?.length || 1;
      showToast(`🚀 Fleet Launched! ${activeCount} Worker Browser(s) Active & Generating.`, 'success');
      
      // Auto-navigate to Step 3 (Workers Farm) to monitor live progress
      if (typeof goToStep === 'function') {
        goToStep(3);
      }
      if (typeof refreshWorkers === 'function') {
        refreshWorkers();
      }
      if (typeof refreshFleetStatus === 'function') {
        refreshFleetStatus();
      }
    } else {
      showToast(`Fleet dispatch error: ${dispatchData.error || 'Unknown error'}`, 'error');
    }
  } catch (err) {
    showToast(`Fleet launch error: ${err.message}`, 'error');
  } finally {
    const startBtn = document.getElementById('btnM1StartGenerating');
    if (startBtn) {
      startBtn.disabled = false;
      startBtn.innerHTML = '<span>🚀</span> Start Generating (1-Click Fleet Launch)';
    }
  }
};
"""

text += start_generating_code

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated app_v2.js with all three feature enhancements!")
