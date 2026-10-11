import os
import sys

app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'

with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace triggerRender implementation
target_render_fn_start = "async function triggerRender() {"
idx_tr = code.find(target_render_fn_start)
if idx_tr == -1:
    print('Error: triggerRender not found')
    sys.exit(1)

# Find the end of triggerRender function (before the next top-level function or catch block)
idx_tr_end = code.find("async function loadRenderHistory()", idx_tr)
if idx_tr_end == -1:
    print('Error: loadRenderHistory not found')
    sys.exit(1)

new_trigger_render = """async function triggerRender() {
  if (!activeProjectId) {
    showToast('Select an active project first', 'warn');
    return;
  }

  const resolution = document.getElementById('renderResolution')?.value || '1920x1080';
  const fps = parseInt(document.getElementById('renderFps')?.value, 10) || 60;
  const speedPreset = document.getElementById('renderSpeedPreset')?.value || 'veryfast';
  const crf = document.getElementById('renderCrf')?.value || (resolution.startsWith('3840') ? '18' : '20');
  const audioBitrate = document.getElementById('renderAudioBitrate')?.value || '320k';
  const motion = document.getElementById('renderMotionToggle')?.checked !== false;
  const hwaccel = document.getElementById('renderHwaccelToggle')?.checked !== false;

  const btn = document.getElementById('btnStartRender');
  const box = document.getElementById('renderStatusCard');
  const bar = document.getElementById('renderBar');
  const statusText = document.getElementById('renderProgressText');
  const pctText = document.getElementById('renderProgressPct');
  const actionsRow = document.getElementById('renderCompletionActions');

  btn.disabled = true;
  box.style.display = 'block';
  if (actionsRow) actionsRow.style.display = 'none';

  statusText.textContent = `Encoding ${resolution} @ ${fps} FPS via FFmpeg (${speedPreset})...`;
  bar.style.width = '25%';
  if (pctText) pctText.textContent = '25%';

  try {
    const isPortrait = resolution.includes('1080x1920') || resolution.includes('2160x3840');
    const aspectRatio = isPortrait ? '9:16' : '16:9';

    const res = await fetch(`/api/v1/projects/${activeProjectId}/render`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        fps,
        resolution,
        aspect_ratio: aspectRatio,
        speed_preset: speedPreset,
        crf,
        audio_bitrate: audioBitrate,
        enable_hwaccel: hwaccel,
        motion_enabled: motion,
        include_music: true,
        include_sfx: true,
        music_volume: window.renderMusicVolume !== undefined ? window.renderMusicVolume : 0.07,
        effects_preset: window.activeAtmosphericEffect || 'normal',
        vignette_enabled: document.getElementById('fxVignetteToggle')?.checked || false,
        blur_amount: parseFloat(document.getElementById('fxBlurSlider')?.value) || 0,
        sharpen_enabled: document.getElementById('fxSharpenToggle')?.checked || false,
        grain_enabled: document.getElementById('fxGrainToggle')?.checked || false,
        transition_type: window.activeTransitionPreset || 'cross_dissolve'
      })
    });

    bar.style.width = '75%';
    if (pctText) pctText.textContent = '75%';

    const data = await res.json();
    if (data.output_path || data.success) {
      bar.style.width = '100%';
      if (pctText) pctText.textContent = '100%';
      statusText.textContent = `✓ Export Complete! (${resolution} @ ${fps}fps H.264 MP4 Saved)`;
      showToast('Render Complete! Video saved to project renders folder.', 'success');

      const videoUrl = resolveMediaUrl(data.output_path || (data.result && data.result.outputPath));
      
      // Update completion actions
      if (actionsRow) actionsRow.style.display = 'flex';
      const dlBtn = document.getElementById('btnDownloadRender');
      if (dlBtn && videoUrl) dlBtn.href = videoUrl;

      // Play video in in-page Master Player
      if (videoUrl) {
        playRenderVideo(videoUrl);
      }

      await loadRenderHistory();
    } else {
      bar.style.width = '100%';
      bar.style.background = '#ef4444';
      statusText.textContent = `Render failed: ${data.error || 'Unknown error'}`;
      showToast(data.error || 'Render failed', 'error');
    }
  } catch (err) {
    bar.style.width = '100%';
    bar.style.background = '#ef4444';
    statusText.textContent = `Error: ${err.message}`;
    showToast(`Render failed: ${err.message}`, 'error');
  } finally {
    btn.disabled = false;
  }
}

"""

code = code[:idx_tr] + new_trigger_render + code[idx_tr_end:]

# Append helper functions for Step 5 and Step 6
helpers = """

// ==========================================================================
// STEP 5 & STEP 6 ADVANCED HELPER FUNCTIONS
// ==========================================================================
function onRenderResolutionChange(val) {
  const badge = document.getElementById('resBadge');
  if (!badge) return;
  const labels = {
    '3840x2160': '🌟 4K Ultra HD',
    '2560x1440': '💎 2K Quad HD',
    '1920x1080': '🎬 1080p Full HD',
    '2160x3840': '📱 4K Vertical Shorts',
    '1080x1920': '📱 1080p Vertical Shorts'
  };
  badge.textContent = labels[val] || val;
}

function playRenderVideo(url) {
  const player = document.getElementById('step5MasterPlayer');
  const placeholder = document.getElementById('step5PlayerPlaceholder');
  if (player) {
    player.src = url;
    player.style.display = 'block';
    player.play().catch(() => {});
  }
  if (placeholder) {
    placeholder.style.display = 'none';
  }
}

async function openOutputFolder(type = 'renders') {
  try {
    const res = await fetch('/api/v1/system/open-folder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folder_type: type, project_id: activeProjectId })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`Opened folder in Windows Explorer`, 'info');
    } else {
      showToast(`Could not open folder: ${data.error}`, 'warn');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}

function togglePasswordVisibility(inputId) {
  const el = document.getElementById(inputId);
  if (!el) return;
  el.type = (el.type === 'password') ? 'text' : 'password';
}

async function testGroqKeyConnection() {
  const keyInput = document.getElementById('settingsGroqKeySingle')?.value.trim();
  showToast('Testing Groq Cloud API connection...', 'info');
  try {
    const res = await fetch('/api/v1/settings/test-groq', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: keyInput })
    });
    const data = await res.json();
    if (data.success) {
      showToast(`✓ ${data.message}`, 'success');
    } else {
      showToast(`❌ Groq Key Test Failed: ${data.error}`, 'error');
    }
  } catch (err) {
    showToast(`Connection error: ${err.message}`, 'error');
  }
}

async function saveAllSettings() {
  const groqSingle = document.getElementById('settingsGroqKeySingle')?.value.trim();
  const groqPool = document.getElementById('settingsGroqKeyPool')?.value.trim();
  const primaryModel = document.getElementById('settingsGroqModel')?.value.trim();
  const fallbackModel = document.getElementById('settingsGroqFallback')?.value.trim();
  const elevenKey = document.getElementById('settingsElevenLabsKey')?.value.trim();
  const openAIKey = document.getElementById('settingsOpenAIKey')?.value.trim();

  const payload = {};
  if (primaryModel) payload.groq_primary_model = primaryModel;
  if (fallbackModel) payload.groq_fallback_model = fallbackModel;
  if (groqSingle) payload.groq_api_key = groqSingle;
  if (elevenKey) payload.elevenlabs_api_key = elevenKey;
  if (openAIKey) payload.openai_api_key = openAIKey;

  if (groqPool) {
    const lines = groqPool.split('\\n').map(l => l.trim()).filter(l => l.startsWith('gsk_'));
    if (lines.length > 0) {
      payload.groq_api_keys_pool = JSON.stringify(lines);
      if (!payload.groq_api_key) payload.groq_api_key = lines[0];
    }
  }

  showToast('Saving settings to local database...', 'info');
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
      showToast(`Save error: ${data.error}`, 'error');
    }
  } catch (err) {
    showToast(`Error saving settings: ${err.message}`, 'error');
  }
}

async function stopAllWorkers() {
  if (!confirm('Are you sure you want to stop all active Chrome worker windows?')) return;
  showToast('Stopping all worker browser instances...', 'info');
  try {
    const res = await fetch('/api/v1/workers/stop-all', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      showToast(`Stopped ${data.count || 0} worker browser windows`, 'success');
      setTimeout(refreshFleetStatus, 2000);
    } else {
      showToast(data.error || 'Failed to stop workers', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}
"""

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code + helpers)

print('Successfully patched triggerRender and added Step 5/6 helpers in app_v2.js')
