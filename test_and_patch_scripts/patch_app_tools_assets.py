import os
import sys

app_js_path = r'E:\stickman-video-automation\studio\public\app_v2.js'

with open(app_js_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update updatePlaybackScene to call applyAtmosphericEffectToCanvas and updateMediaInspector
target_playback = """  badgeEl.textContent = `SCENE ${scene.prompt_id_str || (idx + 1)}`;
  captionEl.textContent = scene.prompt_text || scene.label || `Stickman scene ${idx + 1}`;"""

replacement_playback = """  badgeEl.textContent = `SCENE ${scene.prompt_id_str || (idx + 1)}`;
  captionEl.textContent = scene.prompt_text || scene.label || `Stickman scene ${idx + 1}`;

  // Apply Atmospheric look & Media Inspector sync
  if (typeof applyAtmosphericEffectToCanvas === 'function') {
    applyAtmosphericEffectToCanvas();
  }
  if (typeof updateMediaInspector === 'function') {
    updateMediaInspector();
  }
  if (scene.sfx && isPlaying && typeof playSfx === 'function') {
    playSfx(scene.sfx);
  }"""

if target_playback in code:
    code = code.replace(target_playback, replacement_playback)
    print('Updated updatePlaybackScene hook')
else:
    print('Warning: target_playback not found directly')

# 2. Update triggerRender payload
target_render_body = """        fps: parseInt(fps, 10) || 30,
        resolution,
        aspect_ratio: aspectRatio,
        motion_enabled: motion,
        include_music: true,
        include_sfx: true,
        music_volume: 0.07"""

replacement_render_body = """        fps: parseInt(fps, 10) || 30,
        resolution,
        aspect_ratio: aspectRatio,
        motion_enabled: motion,
        include_music: true,
        include_sfx: true,
        music_volume: window.renderMusicVolume !== undefined ? window.renderMusicVolume : 0.07,
        effects_preset: window.activeAtmosphericEffect || 'normal',
        vignette_enabled: document.getElementById('fxVignetteToggle')?.checked || false,
        blur_amount: parseFloat(document.getElementById('fxBlurSlider')?.value) || 0,
        sharpen_enabled: document.getElementById('fxSharpenToggle')?.checked || false,
        grain_enabled: document.getElementById('fxGrainToggle')?.checked || false,
        transition_type: window.activeTransitionPreset || 'cross_dissolve'"""

if target_render_body in code:
    code = code.replace(target_render_body, replacement_render_body)
    print('Updated triggerRender payload')
else:
    print('Warning: target_render_body not found directly, checking alternate...')
    idx = code.find('async function triggerRender')
    if idx != -1:
        sub = code[idx:idx+1200]
        if 'music_volume: 0.07' in sub:
            code = code.replace('music_volume: 0.07', 'music_volume: window.renderMusicVolume !== undefined ? window.renderMusicVolume : 0.07,\n        effects_preset: window.activeAtmosphericEffect || "normal",\n        vignette_enabled: document.getElementById("fxVignetteToggle")?.checked || false,\n        blur_amount: parseFloat(document.getElementById("fxBlurSlider")?.value) || 0,\n        sharpen_enabled: document.getElementById("fxSharpenToggle")?.checked || false,\n        grain_enabled: document.getElementById("fxGrainToggle")?.checked || false,\n        transition_type: window.activeTransitionPreset || "cross_dissolve"')
            print('Replaced render body fields by alternate search')

# 3. Append the Tools & Assets post-production engine
tools_assets_logic = """

// ==========================================================================
// TOOLS & ASSETS POST-PRODUCTION ENGINE (PORTED & EXPANDED)
// ==========================================================================
window.activeToolsTab = 'effects';
window.activeAtmosphericEffect = 'normal';
window.activeTransitionPreset = 'cross_dissolve';
window.activeMotionPreset = 'motion-zoom-in';
window.renderMusicVolume = 0.07;

const ATMOSPHERIC_FILTERS = {
  normal: '',
  bright: 'brightness(1.18) contrast(1.08) saturate(1.05)',
  moody_dark: 'brightness(0.82) contrast(1.35) saturate(0.85)',
  warm: 'sepia(0.25) saturate(1.4) hue-rotate(-10deg) contrast(1.1)',
  cool: 'hue-rotate(185deg) saturate(1.15) contrast(1.1)',
  vintage: 'sepia(0.4) contrast(1.1) brightness(0.95) saturate(1.2)',
  b_w: 'grayscale(1) contrast(1.3) brightness(1.05)',
  vivid: 'saturate(1.8) contrast(1.2)',
  dreamy: 'brightness(1.1) contrast(1.05) saturate(1.2)',
  neon: 'contrast(1.4) saturate(1.7) hue-rotate(290deg)',
  golden_hour: 'sepia(0.35) saturate(1.6) brightness(1.08) contrast(1.12)',
  cyberpunk: 'contrast(1.35) saturate(1.7) hue-rotate(20deg)',
  noir: 'grayscale(1) contrast(1.7) brightness(0.9)',
  sepia: 'sepia(0.85) contrast(1.15) brightness(0.95)',
  invert: 'invert(1) hue-rotate(180deg)',
  pastel: 'saturate(0.8) brightness(1.12) contrast(0.95)',
  frost: 'hue-rotate(180deg) saturate(0.7) brightness(1.15) contrast(1.1)',
  sunset: 'saturate(1.6) contrast(1.2) hue-rotate(-20deg)',
  ocean: 'hue-rotate(160deg) saturate(1.35) contrast(1.15)',
  chromatic: 'contrast(1.3) saturate(1.5) drop-shadow(2px 0px 0px rgba(255,0,80,0.5)) drop-shadow(-2px 0px 0px rgba(0,240,255,0.5))'
};

function switchToolsTab(tabName) {
  window.activeToolsTab = tabName;
  const tabs = ['effects', 'captions', 'motion', 'audio', 'media'];
  
  tabs.forEach(t => {
    const btn = document.getElementById(`toolTab-${t}`);
    const content = document.getElementById(`tabContent-${t}`);
    if (btn) btn.classList.toggle('active', t === tabName);
    if (content) content.style.display = (t === tabName) ? 'flex' : 'none';
  });

  const badge = document.getElementById('toolsActiveModeBadge');
  if (badge) {
    const labels = {
      effects: '✨ Effects Active',
      captions: '💬 Captions Active',
      motion: '⚡ Motion Active',
      audio: '🔊 Audio / SFX',
      media: '📁 Media Inspector'
    };
    badge.textContent = labels[tabName] || 'Active';
  }

  if (tabName === 'media') {
    updateMediaInspector();
  }
}

function applyAtmosphericEffectToCanvas() {
  const imgEl = document.getElementById('playerCanvasImage');
  const viewport = document.getElementById('playerCanvasViewport');
  if (!imgEl) return;

  const blurVal = parseFloat(document.getElementById('fxBlurSlider')?.value) || 0;
  const expVal = parseFloat(document.getElementById('fxExposureSlider')?.value) || 0;
  const contrastVal = parseFloat(document.getElementById('fxContrastSlider')?.value) || 100;
  const satVal = parseFloat(document.getElementById('fxSaturationSlider')?.value) || 100;
  const vignetteOn = document.getElementById('fxVignetteToggle')?.checked;
  const grainOn = document.getElementById('fxGrainToggle')?.checked;
  const sharpenOn = document.getElementById('fxSharpenToggle')?.checked;
  const glowOn = document.getElementById('fxGlowToggle')?.checked;

  let filterParts = [];
  const basePreset = ATMOSPHERIC_FILTERS[window.activeAtmosphericEffect] || '';
  if (basePreset) filterParts.push(basePreset);

  if (blurVal > 0) filterParts.push(`blur(${blurVal}px)`);
  if (expVal !== 0) filterParts.push(`brightness(${1 + (expVal / 100)})`);
  if (contrastVal !== 100) filterParts.push(`contrast(${contrastVal / 100})`);
  if (satVal !== 100) filterParts.push(`saturate(${satVal / 100})`);
  if (glowOn) filterParts.push('drop-shadow(0 0 10px rgba(0,240,255,0.5))');
  if (sharpenOn) filterParts.push('contrast(1.15)');

  imgEl.style.filter = filterParts.join(' ');

  if (viewport) {
    const forceVig = (window.activeAtmosphericEffect === 'moody_dark' || window.activeAtmosphericEffect === 'noir');
    viewport.classList.toggle('has-vignette', !!vignetteOn || forceVig);
    viewport.classList.toggle('has-grain', !!grainOn || window.activeAtmosphericEffect === 'vintage');
  }
}

function selectAtmosphericEffect(presetKey) {
  window.activeAtmosphericEffect = presetKey;
  document.querySelectorAll('.atmos-card').forEach(card => {
    card.classList.toggle('active', card.getAttribute('data-preset') === presetKey);
  });
  applyAtmosphericEffectToCanvas();
  showToast(`Atmospheric look: ${presetKey.replace('_', ' ').toUpperCase()}`, 'info');
}

function resetAtmosphericEffects() {
  window.activeAtmosphericEffect = 'normal';
  document.querySelectorAll('.atmos-card').forEach(card => {
    card.classList.toggle('active', card.getAttribute('data-preset') === 'normal');
  });

  const blurEl = document.getElementById('fxBlurSlider');
  const expEl = document.getElementById('fxExposureSlider');
  const contrastEl = document.getElementById('fxContrastSlider');
  const satEl = document.getElementById('fxSaturationSlider');
  const vigEl = document.getElementById('fxVignetteToggle');
  const grainEl = document.getElementById('fxGrainToggle');
  const sharpEl = document.getElementById('fxSharpenToggle');
  const glowEl = document.getElementById('fxGlowToggle');

  if (blurEl) blurEl.value = 0;
  if (expEl) expEl.value = 0;
  if (contrastEl) contrastEl.value = 100;
  if (satEl) satEl.value = 100;
  if (vigEl) vigEl.checked = false;
  if (grainEl) grainEl.checked = false;
  if (sharpEl) sharpEl.checked = false;
  if (glowEl) glowEl.checked = false;

  updateCustomEffectSliders();
  showToast('Reset atmospheric effects to Normal', 'info');
}

function updateCustomEffectSliders() {
  const blurVal = document.getElementById('fxBlurSlider')?.value || 0;
  const expVal = document.getElementById('fxExposureSlider')?.value || 0;
  const contrastVal = document.getElementById('fxContrastSlider')?.value || 100;
  const satVal = document.getElementById('fxSaturationSlider')?.value || 100;

  const lblBlur = document.getElementById('fxBlurVal');
  const lblExp = document.getElementById('fxExposureVal');
  const lblContrast = document.getElementById('fxContrastVal');
  const lblSat = document.getElementById('fxSaturationVal');

  if (lblBlur) lblBlur.textContent = `${blurVal}px`;
  if (lblExp) lblExp.textContent = `${expVal > 0 ? '+' : ''}${expVal}%`;
  if (lblContrast) lblContrast.textContent = `${contrastVal}%`;
  if (lblSat) lblSat.textContent = `${satVal}%`;

  applyAtmosphericEffectToCanvas();
}

function selectMotionPreset(motionClass, el) {
  window.activeMotionPreset = motionClass;
  document.querySelectorAll('[data-motion]').forEach(c => c.classList.remove('active'));
  if (el) el.classList.add('active');

  const badge = document.getElementById('activeMotionBadge');
  if (badge && el) {
    const title = el.querySelector('.motion-card-title');
    if (title) badge.textContent = title.textContent;
  }

  const imgEl = document.getElementById('playerCanvasImage');
  if (imgEl) {
    imgEl.className = 'canvas-image-stage';
    void imgEl.offsetWidth; // trigger reflow
    imgEl.className = `canvas-image-stage ${motionClass}`;
  }
}

function selectTransitionPreset(transKey, el) {
  window.activeTransitionPreset = transKey;
  document.querySelectorAll('[data-transition]').forEach(c => c.classList.remove('active'));
  if (el) el.classList.add('active');

  const badge = document.getElementById('activeTransitionBadge');
  if (badge && el) {
    const title = el.querySelector('.motion-card-title');
    if (title) badge.textContent = title.textContent;
  }
  showToast(`Transition set: ${transKey.replace('_', ' ').toUpperCase()}`, 'info');
}

// ==========================================================================
// WEB AUDIO API SFX SYNTHESIZER ENGINE (ZERO-DEPENDENCY AUDITION)
// ==========================================================================
let studioAudioCtx = null;
function getStudioAudioContext() {
  if (!studioAudioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (AudioContextClass) studioAudioCtx = new AudioContextClass();
  }
  if (studioAudioCtx && studioAudioCtx.state === 'suspended') {
    studioAudioCtx.resume();
  }
  return studioAudioCtx;
}

function playSfx(type) {
  const ctx = getStudioAudioContext();
  if (!ctx) return;

  const now = ctx.currentTime;
  const masterGain = ctx.createGain();
  masterGain.connect(ctx.destination);

  if (type === 'whoosh') {
    const a = new Audio('/sfx/whoosh.wav');
    a.play().catch(() => synthWhoosh(ctx, now, masterGain, 0.45));
    return;
  }
  if (type === 'pop') {
    const a = new Audio('/sfx/pop.wav');
    a.play().catch(() => synthPop(ctx, now, masterGain));
    return;
  }

  if (type.includes('whoosh') || type.includes('swish')) {
    const dur = (type.includes('fast') || type.includes('short')) ? 0.22 : 0.48;
    synthWhoosh(ctx, now, masterGain, dur, type.includes('reverse'));
  } else if (type.includes('impact') || type.includes('hit') || type.includes('boom')) {
    synthImpact(ctx, now, masterGain, type);
  } else if (type.includes('riser')) {
    synthRiser(ctx, now, masterGain, type.includes('tension'));
  } else if (type.includes('ambience') || type.includes('tone')) {
    synthAmbience(ctx, now, masterGain, type);
  } else if (type === 'camera_shutter') {
    synthShutter(ctx, now, masterGain);
  } else if (type === 'click' || type === 'tick' || type === 'digital_click') {
    synthClick(ctx, now, masterGain, type);
  } else if (type === 'glitch_hit') {
    synthGlitch(ctx, now, masterGain);
  } else {
    synthWhoosh(ctx, now, masterGain, 0.35);
  }
}

function synthWhoosh(ctx, now, masterGain, duration = 0.45, isReverse = false) {
  const bufferSize = ctx.sampleRate * duration;
  const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = Math.random() * 2 - 1;
  }

  const noise = ctx.createBufferSource();
  noise.buffer = buffer;

  const filter = ctx.createBiquadFilter();
  filter.type = 'bandpass';
  filter.Q.setValueAtTime(3.5, now);

  const gain = ctx.createGain();
  if (isReverse) {
    filter.frequency.setValueAtTime(150, now);
    filter.frequency.exponentialRampToValueAtTime(3000, now + duration);
    gain.gain.setValueAtTime(0.01, now);
    gain.gain.exponentialRampToValueAtTime(0.7, now + duration * 0.85);
    gain.gain.linearRampToValueAtTime(0.01, now + duration);
  } else {
    filter.frequency.setValueAtTime(200, now);
    filter.frequency.exponentialRampToValueAtTime(2800, now + duration * 0.4);
    filter.frequency.exponentialRampToValueAtTime(180, now + duration);
    gain.gain.setValueAtTime(0.01, now);
    gain.gain.linearRampToValueAtTime(0.8, now + duration * 0.3);
    gain.gain.exponentialRampToValueAtTime(0.01, now + duration);
  }

  noise.connect(filter);
  filter.connect(gain);
  gain.connect(masterGain);

  noise.start(now);
  noise.stop(now + duration);
}

function synthImpact(ctx, now, masterGain, type) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  const isDeep = type.includes('deep') || type.includes('sub') || type.includes('bass');
  const startFreq = isDeep ? 90 : 160;
  const endFreq = isDeep ? 28 : 45;
  const dur = isDeep ? 1.6 : 1.1;

  osc.type = 'sine';
  osc.frequency.setValueAtTime(startFreq, now);
  osc.frequency.exponentialRampToValueAtTime(endFreq, now + dur);

  gain.gain.setValueAtTime(0.9, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + dur);

  osc.connect(gain);
  gain.connect(masterGain);

  osc.start(now);
  osc.stop(now + dur);
}

function synthRiser(ctx, now, masterGain, isTension = false) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  const dur = 2.4;

  osc.type = isTension ? 'sawtooth' : 'triangle';
  osc.frequency.setValueAtTime(100, now);
  osc.frequency.exponentialRampToValueAtTime(1200, now + dur);

  gain.gain.setValueAtTime(0.05, now);
  gain.gain.linearRampToValueAtTime(0.65, now + dur * 0.9);
  gain.gain.linearRampToValueAtTime(0.001, now + dur);

  osc.connect(gain);
  gain.connect(masterGain);

  osc.start(now);
  osc.stop(now + dur);
}

function synthAmbience(ctx, now, masterGain, type) {
  const dur = 2.5;
  const osc1 = ctx.createOscillator();
  const osc2 = ctx.createOscillator();
  const gain = ctx.createGain();

  osc1.type = 'sine';
  osc1.frequency.setValueAtTime(65, now);
  osc2.type = 'sine';
  osc2.frequency.setValueAtTime(97.5, now); // perfect fifth

  gain.gain.setValueAtTime(0.01, now);
  gain.gain.linearRampToValueAtTime(0.4, now + 0.6);
  gain.gain.linearRampToValueAtTime(0.01, now + dur);

  osc1.connect(gain);
  osc2.connect(gain);
  gain.connect(masterGain);

  osc1.start(now);
  osc2.start(now);
  osc1.stop(now + dur);
  osc2.stop(now + dur);
}

function synthClick(ctx, now, masterGain, type) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  const freq = type === 'tick' ? 2400 : 1200;

  osc.type = 'sine';
  osc.frequency.setValueAtTime(freq, now);
  gain.gain.setValueAtTime(0.5, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

  osc.connect(gain);
  gain.connect(masterGain);

  osc.start(now);
  osc.stop(now + 0.05);
}

function synthPop(ctx, now, masterGain) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.type = 'sine';
  osc.frequency.setValueAtTime(600, now);
  osc.frequency.exponentialRampToValueAtTime(140, now + 0.09);

  gain.gain.setValueAtTime(0.7, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);

  osc.connect(gain);
  gain.connect(masterGain);

  osc.start(now);
  osc.stop(now + 0.11);
}

function synthShutter(ctx, now, masterGain) {
  synthClick(ctx, now, masterGain, 'tick');
  synthClick(ctx, now + 0.065, masterGain, 'click');
}

function synthGlitch(ctx, now, masterGain) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.type = 'square';
  osc.frequency.setValueAtTime(450, now);
  osc.frequency.setValueAtTime(920, now + 0.03);
  osc.frequency.setValueAtTime(210, now + 0.06);

  gain.gain.setValueAtTime(0.4, now);
  gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

  osc.connect(gain);
  gain.connect(masterGain);

  osc.start(now);
  osc.stop(now + 0.13);
}

function attachSfxToCurrentScene(sfxName) {
  if (!timelineItems || timelineItems.length === 0) {
    showToast('No scenes on timeline to attach sound', 'warn');
    return;
  }
  const idx = currentSceneIndex;
  timelineItems[idx].sfx = sfxName;
  showToast(`🔊 Attached "${sfxName}" to Scene #${idx + 1}`, 'success');
  renderCapCutTimeline();
}

function updateMediaInspector() {
  if (!timelineItems || timelineItems.length === 0) return;
  const idx = currentSceneIndex;
  const item = timelineItems[idx];
  if (!item) return;

  const titleEl = document.getElementById('mediaInspectorTitle');
  const badgeEl = document.getElementById('mediaInspectorBadge');
  const thumbEl = document.getElementById('mediaInspectorThumb');
  const durEl = document.getElementById('mediaInspectorDuration');
  const textEl = document.getElementById('mediaInspectorPromptText');

  if (titleEl) titleEl.textContent = `🎬 Active Scene #${idx + 1}`;
  if (badgeEl) badgeEl.textContent = `Prompt ${item.prompt_id_str || String(idx + 1).padStart(3, '0')}`;
  if (durEl) durEl.textContent = `${(parseFloat(item.duration) || 1.33).toFixed(2)}s`;
  if (textEl) textEl.textContent = item.prompt_text || `Prompt description for scene #${idx + 1}`;

  const rawImg = item.image_path || item.file_path;
  if (thumbEl && rawImg) {
    thumbEl.src = resolveMediaUrl(rawImg);
  }
}

function onReplaceSceneImage(inputEl) {
  if (!inputEl.files || !inputEl.files[0]) return;
  const file = inputEl.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    const dataUrl = e.target.result;
    if (timelineItems[currentSceneIndex]) {
      timelineItems[currentSceneIndex].image_path = dataUrl;
      const imgEl = document.getElementById('playerCanvasImage');
      if (imgEl) imgEl.src = dataUrl;
      renderCapCutTimeline();
      updateMediaInspector();
      showToast(`Updated image for Scene #${currentSceneIndex + 1}`, 'success');
    }
  };
  reader.readAsDataURL(file);
}
"""

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(code + tools_assets_logic)

print('Successfully appended Tools & Assets logic to app_v2.js')
