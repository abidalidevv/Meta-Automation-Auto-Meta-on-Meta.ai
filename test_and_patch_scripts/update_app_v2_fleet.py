import os
import sys

app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update refreshFleetStatus, openWorkerLogin, and add toggleWorkerProvider
target_fleet_start = code.find('async function refreshFleetStatus() {')
target_fleet_end = code.find('async function loadGroqKeyPool() {')

if target_fleet_start == -1 or target_fleet_end == -1:
    print('Error: Could not find refreshFleetStatus boundaries in app_v2.js')
    sys.exit(1)

new_fleet_code = '''async function refreshFleetStatus() {
  try {
    const res = await fetch('/api/v1/workers/fleet-status');
    const data = await res.json();
    if (!data.workers) return;

    // 1. Update Step 6 Login Assistant Grid
    const assistantGrid = document.getElementById('workersLoginAssistantGrid');
    if (assistantGrid) {
      assistantGrid.innerHTML = data.workers.map(w => {
        const isAuth = w.authenticated;
        const isRunning = w.is_running;
        const isFlow = (w.provider || '').toLowerCase() === 'flow';
        const providerBadge = isFlow 
          ? '<span class="badge" style="background: rgba(0,240,255,0.15); color: var(--cyan); border: 1px solid rgba(0,240,255,0.3); font-size: 10px; font-weight: 800;">⚡ FLOW</span>'
          : '<span class="badge" style="background: rgba(139,92,246,0.15); color: var(--violet); border: 1px solid rgba(139,92,246,0.3); font-size: 10px; font-weight: 800;">🌐 META</span>';
        
        const statusBadge = isRunning
          ? `<span style="color: #60a5fa; font-size: 10px; font-weight: 700;">🔵 Running (PID ${w.pid || ''})</span>`
          : (isAuth 
            ? '<span style="color: var(--emerald); font-size: 10px; font-weight: 700;">🟢 Session Saved</span>'
            : '<span style="color: var(--amber); font-size: 10px; font-weight: 700;">🟡 Needs Login</span>');

        const otherProv = isFlow ? 'meta' : 'flow';

        return `
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-family: var(--font-mono); font-weight: 800; font-size: 13px; color: #fff;">${w.id}</span>
              ${providerBadge}
            </div>
            <div style="margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
              ${statusBadge}
              <button type="button" class="btn btn-secondary" onclick="toggleWorkerProvider('${w.id}', '${w.provider}')" title="Switch between Flow and Meta" style="font-size: 9.5px; padding: 2px 6px;">
                ⇄ ${otherProv.toUpperCase()}
              </button>
            </div>
            <button type="button" class="btn btn-secondary" onclick="openWorkerLogin('${w.id}', '${w.provider}')" style="width: 100%; justify-content: center; font-size: 11px; padding: 5px 8px; font-weight: 700;">
              🚀 Open ${isFlow ? 'Flow' : 'Meta'} Login
            </button>
          </div>
        `;
      }).join('');
    }

    // 2. Update Step 2 Fleet Status Grid if present
    const fleetGrid = document.getElementById('workersFleetStatusGrid');
    if (fleetGrid) {
      fleetGrid.innerHTML = data.workers.map(w => {
        const isAuth = w.authenticated;
        const statusBadge = isAuth 
          ? '<span class="badge badge-emerald" style="font-size: 10px;">Session Saved</span>'
          : '<span class="badge badge-amber" style="font-size: 10px;">Setup Required</span>';

        return `
          <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-family: var(--font-mono); font-weight: 700; color: #fff;">${w.id}</span>
              <span class="badge badge-cyan" style="font-size: 10px;">${w.provider.toUpperCase()}</span>
            </div>
            <div style="margin-bottom: 8px;">${statusBadge}</div>
            <button class="btn btn-secondary" onclick="openWorkerLogin('${w.id}', '${w.provider}')" style="width: 100%; padding: 4px 8px; font-size: 11px;">
              Open Login
            </button>
          </div>
        `;
      }).join('');
    }
  } catch (err) {
    console.warn('refreshFleetStatus error:', err);
  }
}

async function toggleWorkerProvider(workerId, currentProvider) {
  const newProv = (currentProvider || '').toLowerCase() === 'flow' ? 'meta' : 'flow';
  showToast(`Switching ${workerId} to ${newProv.toUpperCase()}...`, 'info');
  try {
    const res = await fetch(`/api/v1/workers/${workerId}/provider`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider: newProv })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Worker ${workerId} is now assigned to ${newProv.toUpperCase()}!`, 'success');
      refreshFleetStatus();
    } else {
      showToast(data.error || 'Failed to update provider', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}

async function openWorkerLogin(workerId, provider) {
  if (workerId === 'ALL') {
    showToast('🚀 Launching all 10 worker profiles (1 worker = 1 extension)... Please log in once in each window!', 'info');
    try {
      const res = await fetch('/api/v1/workers/login-assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ worker_id: 'ALL' })
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, 'success');
        setTimeout(refreshFleetStatus, 3000);
      } else {
        showToast(data.error || 'Failed launching worker profiles', 'error');
      }
    } catch (err) {
      showToast(`Error: ${err.message}`, 'error');
    }
    return;
  }

  showToast(`Opening dedicated browser for ${workerId} (${(provider || '').toUpperCase()})...`, 'info');
  try {
    const res = await fetch('/api/v1/workers/login-assistant', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ worker_id: workerId, provider })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      setTimeout(refreshFleetStatus, 2500);
    } else {
      showToast(data.error || 'Failed to open login window', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}

'''

code = code[:target_fleet_start] + new_fleet_code + code[target_fleet_end:]

# 2. Update loadSettings and saveAllSettings
target_save_start = code.find('async function saveAllSettings() {')
target_save_end = code.find('async function testGroqKeyConnection() {')

if target_save_start != -1 and target_save_end != -1:
    new_settings_code = '''async function loadSettings() {
  try {
    const res = await fetch('/api/v1/settings');
    const data = await res.json();
    
    // Groq settings
    if (data.groq_primary_model && document.getElementById('settingsGroqModel')) {
      document.getElementById('settingsGroqModel').value = data.groq_primary_model;
    }
    if (data.groq_fallback_model && document.getElementById('settingsGroqFallback')) {
      document.getElementById('settingsGroqFallback').value = data.groq_fallback_model;
    }
    if (data.groq_api_key && document.getElementById('settingsGroqKeySingle')) {
      document.getElementById('settingsGroqKeySingle').value = data.groq_api_key;
    }
    if (data.groq_api_keys_pool && document.getElementById('settingsGroqKeyPool')) {
      try {
        const pool = JSON.parse(data.groq_api_keys_pool);
        if (Array.isArray(pool)) {
          document.getElementById('settingsGroqKeyPool').value = pool.join('\\n');
          const poolLabel = document.getElementById('keyPoolCountLabel');
          if (poolLabel) poolLabel.textContent = `${pool.length} Key(s) Loaded`;
        }
      } catch (e) {
        document.getElementById('settingsGroqKeyPool').value = data.groq_api_keys_pool;
      }
    }

    // ElevenLabs
    if (data.elevenlabs_api_key && document.getElementById('settingsElevenLabsKey')) {
      document.getElementById('settingsElevenLabsKey').value = data.elevenlabs_api_key;
    }
    if (data.elevenlabs_voice_id && document.getElementById('settingsElevenLabsVoiceId')) {
      document.getElementById('settingsElevenLabsVoiceId').value = data.elevenlabs_voice_id;
    }

    // OpenAI
    if (data.openai_api_key && document.getElementById('settingsOpenAIKey')) {
      document.getElementById('settingsOpenAIKey').value = data.openai_api_key;
    }
    if (data.openai_model && document.getElementById('settingsOpenAIModel')) {
      document.getElementById('settingsOpenAIModel').value = data.openai_model;
    }

    // Stability & Pexels
    if (data.stability_api_key && document.getElementById('settingsStabilityKey')) {
      document.getElementById('settingsStabilityKey').value = data.stability_api_key;
    }
    if (data.pexels_api_key && document.getElementById('settingsPexelsKey')) {
      document.getElementById('settingsPexelsKey').value = data.pexels_api_key;
    }
  } catch (err) {
    console.warn('loadSettings error:', err);
  }
}

async function saveAllSettings() {
  const groqSingle = document.getElementById('settingsGroqKeySingle')?.value.trim();
  const groqPool = document.getElementById('settingsGroqKeyPool')?.value.trim();
  const primaryModel = document.getElementById('settingsGroqModel')?.value.trim();
  const fallbackModel = document.getElementById('settingsGroqFallback')?.value.trim();
  const elevenKey = document.getElementById('settingsElevenLabsKey')?.value.trim();
  const elevenVoice = document.getElementById('settingsElevenLabsVoiceId')?.value.trim();
  const openAIKey = document.getElementById('settingsOpenAIKey')?.value.trim();
  const openAIModel = document.getElementById('settingsOpenAIModel')?.value.trim();
  const stabilityKey = document.getElementById('settingsStabilityKey')?.value.trim();
  const pexelsKey = document.getElementById('settingsPexelsKey')?.value.trim();

  const payload = {};
  if (primaryModel) payload.groq_primary_model = primaryModel;
  if (fallbackModel) payload.groq_fallback_model = fallbackModel;
  if (groqSingle) payload.groq_api_key = groqSingle;
  if (elevenKey) payload.elevenlabs_api_key = elevenKey;
  if (elevenVoice) payload.elevenlabs_voice_id = elevenVoice;
  if (openAIKey) payload.openai_api_key = openAIKey;
  if (openAIModel) payload.openai_model = openAIModel;
  if (stabilityKey) payload.stability_api_key = stabilityKey;
  if (pexelsKey) payload.pexels_api_key = pexelsKey;

  if (groqPool) {
    const lines = groqPool.split('\\n').map(l => l.trim()).filter(l => l.startsWith('gsk_'));
    if (lines.length > 0) {
      payload.groq_api_keys_pool = JSON.stringify(lines);
      if (!payload.groq_api_key) payload.groq_api_key = lines[0];
    }
  }

  showToast('Saving all settings & keys to local database...', 'info');
  try {
    const res = await fetch('/api/v1/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showToast('All settings & API keys saved successfully!', 'success');
      await loadSettings();
    } else {
      showToast(data.error || 'Failed to save settings', 'error');
    }
  } catch (err) {
    showToast(`Error saving settings: ${err.message}`, 'error');
  }
}

'''
    code = code[:target_save_start] + new_settings_code + code[target_save_end:]
    print('Updated loadSettings and saveAllSettings in app_v2.js')

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('app_v2.js updated successfully!')
