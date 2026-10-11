import os
import sys

# 1. Update render_engine.js
render_path = r'E:\stickman-video-automation\studio\server\render_engine.js'
with open(render_path, 'r', encoding='utf-8') as f:
    code = f.read()

old_head = """  async renderProjectVideo(projectId, {
    outputFileName = null,
    includeMusic = true,
    includeSfx = true,
    musicVolume = 0.07, // STRICT REQUIREMENT: DEFAULT MUSIC VOLUME = 7%
    transitionType = 'cross_dissolve',
    aspectRatio = '16:9',
    effectsPreset = 'normal',
    vignetteEnabled = false,
    blurAmount = 0,
    sharpenEnabled = false,
    grainEnabled = false,
    fps = 30
  } = {}) {
    const isPortrait = (aspectRatio === '9:16');
    const targetW = isPortrait ? 1080 : 1920;
    const targetH = isPortrait ? 1920 : 1080;
    const resolutionStr = `${targetW}x${targetH}`;"""

new_head = """  async renderProjectVideo(projectId, {
    outputFileName = null,
    includeMusic = true,
    includeSfx = true,
    musicVolume = 0.07, // STRICT REQUIREMENT: DEFAULT MUSIC VOLUME = 7%
    transitionType = 'cross_dissolve',
    aspectRatio = '16:9',
    resolution = '1920x1080',
    effectsPreset = 'normal',
    vignetteEnabled = false,
    blurAmount = 0,
    sharpenEnabled = false,
    grainEnabled = false,
    fps = 60,
    speedPreset = 'veryfast',
    crf = null,
    audioBitrate = '320k',
    enableHwaccel = true
  } = {}) {
    let targetW = 1920;
    let targetH = 1080;
    if (resolution && resolution.includes('x')) {
      const parts = resolution.split('x').map(Number);
      if (parts.length === 2 && parts[0] > 0 && parts[1] > 0) {
        targetW = parts[0];
        targetH = parts[1];
      }
    } else if (aspectRatio === '9:16') {
      targetW = 1080;
      targetH = 1920;
    }
    const renderFps = parseInt(fps, 10) || 60;
    const crfVal = crf !== null && crf !== undefined ? String(crf) : (targetW >= 3840 ? '18' : '20');
    const resolutionStr = `${targetW}x${targetH}`;"""

if old_head in code:
    code = code.replace(old_head, new_head)
    print('Updated renderProjectVideo head with 4K/60FPS/Fast params')
else:
    print('Warning: old_head not found in render_engine.js')

old_args_block = """      '-c:v', 'libx264',
      '-pix_fmt', 'yuv420p',
      '-preset', 'fast',
      '-crf', '20',
      '-r', '30',
      '-c:a', 'aac',
      '-b:a', '192k',"""

new_args_block = """      '-c:v', 'libx264',
      '-pix_fmt', 'yuv420p',
      '-preset', speedPreset || 'veryfast',
      '-crf', crfVal,
      '-r', String(renderFps),
      '-threads', '0',
      '-c:a', 'aac',
      '-b:a', audioBitrate || '320k',"""

if old_args_block in code:
    code = code.replace(old_args_block, new_args_block)
    print('Updated FFmpeg args with multi-threading, dynamic CRF, 320k audio, and 60 FPS')
else:
    print('Warning: old_args_block not found in render_engine.js')

with open(render_path, 'w', encoding='utf-8') as f:
    f.write(code)

# 2. Update routes.js /projects/:id/render
routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    r_code = f.read()

target_route = """router.post('/projects/:id/render', async (req, res) => {
  try {
    const {
      output_file_name,
      include_music,
      include_sfx,
      music_volume,
      transition_type,
      aspect_ratio,
      effects_preset,
      vignette_enabled,
      blur_amount,
      sharpen_enabled,
      grain_enabled,
      fps
    } = req.body;
    const result = await renderEngine.renderProjectVideo(req.params.id, {
      outputFileName: output_file_name,
      includeMusic: include_music !== undefined ? include_music : true,
      includeSfx: include_sfx !== undefined ? include_sfx : true,
      musicVolume: music_volume !== undefined ? music_volume : 0.07, // 7% default
      transitionType: transition_type || 'cross_dissolve',
      aspectRatio: aspect_ratio || '16:9',
      effectsPreset: effects_preset || 'normal',
      vignetteEnabled: !!vignette_enabled,
      blurAmount: parseFloat(blur_amount) || 0,
      sharpenEnabled: !!sharpen_enabled,
      grainEnabled: !!grain_enabled,
      fps: parseInt(fps, 10) || 30
    });
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

replacement_route = """router.post('/projects/:id/render', async (req, res) => {
  try {
    const {
      output_file_name,
      include_music,
      include_sfx,
      music_volume,
      transition_type,
      aspect_ratio,
      resolution,
      effects_preset,
      vignette_enabled,
      blur_amount,
      sharpen_enabled,
      grain_enabled,
      fps,
      speed_preset,
      crf,
      audio_bitrate,
      enable_hwaccel
    } = req.body;
    const result = await renderEngine.renderProjectVideo(req.params.id, {
      outputFileName: output_file_name,
      includeMusic: include_music !== undefined ? include_music : true,
      includeSfx: include_sfx !== undefined ? include_sfx : true,
      musicVolume: music_volume !== undefined ? music_volume : 0.07, // 7% default
      transitionType: transition_type || 'cross_dissolve',
      aspectRatio: aspect_ratio || '16:9',
      resolution: resolution || (aspect_ratio === '9:16' ? '1080x1920' : '1920x1080'),
      effectsPreset: effects_preset || 'normal',
      vignetteEnabled: !!vignette_enabled,
      blurAmount: parseFloat(blur_amount) || 0,
      sharpenEnabled: !!sharpen_enabled,
      grainEnabled: !!grain_enabled,
      fps: parseInt(fps, 10) || 60,
      speedPreset: speed_preset || 'veryfast',
      crf: crf !== undefined ? crf : null,
      audioBitrate: audio_bitrate || '320k',
      enableHwaccel: enable_hwaccel !== false
    });
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

if target_route in r_code:
    r_code = r_code.replace(target_route, replacement_route)
    with open(routes_path, 'w', encoding='utf-8') as f:
        f.write(r_code)
    print('Updated render endpoint in routes.js with 4K/60FPS/Fast options')
else:
    print('Warning: target_route not found in routes.js')

print('Render engine 4K patch complete.')
