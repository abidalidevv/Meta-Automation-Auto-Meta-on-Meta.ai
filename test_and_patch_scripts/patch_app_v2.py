import re
import os

print("Starting app_v2.js patcher...")

app_file = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_file, 'r', encoding='utf-8') as f:
    js_code = f.read()

# 1. Update handleM1VoiceoverFile to format duration cleanly and not add voiceover.mp3 badge
old_audio_probe_block = """  audioObj.onloadedmetadata = () => {
    const dur = audioObj.duration;
    URL.revokeObjectURL(objectUrl);
    if (dur && dur > 0) {
      const formattedDur = dur.toFixed(1);
      const durInput = document.getElementById('m1Duration');
      if (durInput) durInput.value = formattedDur;
      const badge = document.getElementById('m1DurationBadge');
      if (badge) {
        badge.textContent = `${formattedDur}s (Auto-Detected)`;
        badge.style.color = 'var(--emerald)';
        badge.style.borderColor = 'var(--emerald)';
      }
      updateM1PromptEstimate();
      showToast(`⚡ Audio auto-scanned: ${formattedDur}s. Pacing forecast updated!`, 'success');
    }
  };"""

new_audio_probe_block = """  audioObj.onloadedmetadata = () => {
    const dur = audioObj.duration;
    URL.revokeObjectURL(objectUrl);
    if (dur && dur > 0) {
      const formattedDur = dur.toFixed(1);
      const mins = Math.floor(dur / 60);
      const secs = Math.round(dur % 60);
      const durInput = document.getElementById('m1Duration');
      if (durInput) durInput.value = formattedDur;
      const badge = document.getElementById('m1DurationBadge');
      if (badge) {
        badge.textContent = mins > 0 ? `${formattedDur}s (${mins}m ${secs}s)` : `${formattedDur}s`;
        badge.style.color = 'var(--emerald)';
        badge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      }
      updateM1PromptEstimate();
      showToast(`🎵 Audio scanned: ${formattedDur}s (${mins}m ${secs}s). Forecast updated!`, 'success');
    }
  };"""

if old_audio_probe_block in js_code:
    js_code = js_code.replace(old_audio_probe_block, new_audio_probe_block)
else:
    print("Warning: old_audio_probe_block not found directly, checking regex")
    js_code = re.sub(
        r"audioObj\.onloadedmetadata\s*=\s*\(\)\s*=>\s*\{[\s\S]*?showToast\([^\)]+\);\s*\}\s*\};",
        new_audio_probe_block.strip(),
        js_code
    )

# 2. Update updateM1PromptEstimate
old_update_est_pat = r"function updateM1PromptEstimate\(\)\s*\{[\s\S]*?if \(fCount\) fCount\.textContent = `\$\{targetPrompts\} Scenes \(\$\{targetPrompts\} Prompts & \$\{targetPrompts\} Images\)`\;\s*\}"

new_update_est = """function updateM1PromptEstimate() {
  const durEl = document.getElementById('m1Duration');
  const pacingEl = document.getElementById('m1Pacing');
  const customEl = document.getElementById('m1CustomCount');
  const badge = document.getElementById('m1PromptEstimateBadge');
  if (!durEl || !pacingEl) return;

  const duration = parseFloat(durEl.value) || 60;
  const pacing = pacingEl.value || 'Random';
  const custom = customEl ? parseInt(customEl.value) : null;
  const rates = { 'Random': 0.50, '1/4s': 0.25, '2/4s': 0.50, '3/4s': 0.75, '4/4s': 1.00, '5/4s': 1.25 };
  const rate = rates[pacing] || 0.50;
  const targetPrompts = (custom && custom > 0) ? custom : Math.max(1, Math.round(duration * rate));

  let pacingRuleText = `${pacing} (${(1 / rate).toFixed(2)}s/image)`;
  if (pacing === 'Random') {
    pacingRuleText = '🎲 Dynamic Anti-Template (~2.00s/img)';
  }

  if (badge) {
    badge.textContent = (custom && custom > 0) ? `${custom} prompts (override)` : `~${targetPrompts} stickman prompts`;
  }

  // Update Live Audio Forecast Card
  const fDur = document.getElementById('m1ForecastDur');
  const fPacing = document.getElementById('m1ForecastPacing');
  const fCount = document.getElementById('m1ForecastCount');
  const mins = Math.floor(duration / 60);
  const secs = Math.round(duration % 60);
  const durTimeStr = mins > 0 ? `${duration.toFixed(1)}s (${mins}m ${secs}s)` : `${duration.toFixed(1)}s`;
  if (fDur) fDur.textContent = durTimeStr;
  if (fPacing) fPacing.textContent = pacingRuleText;
  if (fCount) fCount.textContent = `${targetPrompts} Scenes (${targetPrompts} Prompts & ${targetPrompts} Images)`;
}"""

js_code = re.sub(old_update_est_pat, lambda m: new_update_est, js_code)

# 3. Update triggerMode1Generate to render into #m1OutputCanvasBox
old_m1gen_end = """    if (result.story_bible) {
      document.getElementById('m1BibleBox').style.display = 'block';
      document.getElementById('m1BibleProtagonist').textContent = result.story_bible.protagonist || 'Stickman Hero';
      document.getElementById('m1BibleSetting').textContent = result.story_bible.setting || 'Obsidian void / minimalist background';
    }

    await loadProjectPrompts();
    onSelectProject(activeProjectId);"""

new_m1gen_end = """    if (result.story_bible) {
      document.getElementById('m1BibleBox').style.display = 'block';
      document.getElementById('m1BibleProtagonist').textContent = result.story_bible.protagonist || 'Stickman Hero';
      document.getElementById('m1BibleSetting').textContent = result.story_bible.setting || 'Obsidian void / minimalist background';
    }

    // Render into Output Canvas
    const canvasBox = document.getElementById('m1OutputCanvasBox');
    const canvasText = document.getElementById('m1OutputCanvasText');
    const canvasCountBadge = document.getElementById('m1CanvasCountBadge');
    
    let rawText = result.raw_prompts_text || '';
    if (!rawText && result.prompts && Array.isArray(result.prompts)) {
      rawText = result.prompts.map(p => {
        let t = p.prompt_text || p.prompt || '';
        const numStr = String(p.index || p.id_str).padStart(3, '0');
        return t.startsWith(`${numStr}_`) ? t : `${numStr}_${t}`;
      }).join('\\n');
    }

    if (canvasBox && canvasText) {
      canvasText.value = rawText;
      if (canvasCountBadge) canvasCountBadge.textContent = `${result.generated_count || result.prompts?.length || 0} Scenes`;
      canvasBox.style.display = 'block';
      canvasBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    await loadProjectPrompts();
    onSelectProject(activeProjectId);"""

if old_m1gen_end in js_code:
    js_code = js_code.replace(old_m1gen_end, new_m1gen_end)
else:
    print("Warning: old_m1gen_end not found directly, checking regex")
    js_code = re.sub(
        r"if \(result\.story_bible\) \{[\s\S]*?onSelectProject\(activeProjectId\);",
        lambda m: new_m1gen_end,
        js_code
    )

# 4. Append new helper functions if not present
new_helpers = """
// --- MODE 1 ENHANCED HELPERS ---
function copyM1PromptsCanvas() {
  const el = document.getElementById('m1OutputCanvasText');
  if (!el || !el.value.trim()) {
    showToast('No prompts to copy', 'warn');
    return;
  }
  navigator.clipboard.writeText(el.value.trim())
    .then(() => showToast(`📋 Copied ${el.value.trim().split('\\n').length} prompts to clipboard!`, 'success'))
    .catch(() => {
      el.select();
      document.execCommand('copy');
      showToast('📋 Copied prompts to clipboard!', 'success');
    });
}

function downloadM1PromptsFile() {
  const el = document.getElementById('m1OutputCanvasText');
  if (!el || !el.value.trim()) {
    showToast('No prompts to download', 'warn');
    return;
  }
  const title = (document.getElementById('m1VideoTitle')?.value || 'stickman_prompts').replace(/[^a-zA-Z0-9_\\-]/g, '_');
  const blob = new Blob([el.value], { type: 'text/plain;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `${title}.txt`;
  a.click();
  URL.revokeObjectURL(a.href);
  showToast(`💾 Saved ${title}.txt`, 'success');
}

function proceedFromM1ToWorkerFarm() {
  switchStepTab(2);
}

function toggleDirectivePreview() {
  const box = document.getElementById('m1DirectiveBox');
  if (box) {
    box.style.display = box.style.display === 'none' ? 'block' : 'none';
  }
}

function handleMasterPromptFile(input) {
  if (!input.files || !input.files[0]) return;
  const file = input.files[0];
  const reader = new FileReader();
  reader.onload = (e) => {
    const text = e.target.result;
    const promptInput = document.getElementById('m1MasterPrompt');
    if (promptInput) promptInput.value = text;
    const badge = document.getElementById('m1DirectiveStatusBadge');
    if (badge) {
      badge.textContent = `${file.name} (Custom Loaded)`;
      badge.style.color = 'var(--emerald)';
    }
    showToast(`Loaded directive from ${file.name}`, 'success');
  };
  reader.readAsText(file);
}
"""

if "function copyM1PromptsCanvas" not in js_code:
    js_code += "\n" + new_helpers

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Updated app_v2.js successfully!")
