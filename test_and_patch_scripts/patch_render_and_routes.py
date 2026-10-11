import os
import sys

# 1. Patch routes.js
routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    routes_code = f.read()

target_route = """router.post('/projects/:id/render', async (req, res) => {
  try {
    const { output_file_name, include_music, include_sfx, music_volume, transition_type, aspect_ratio } = req.body;
    const result = await renderEngine.renderProjectVideo(req.params.id, {
      outputFileName: output_file_name,
      includeMusic: include_music,
      includeSfx: include_sfx,
      musicVolume: music_volume !== undefined ? music_volume : 0.07, // 7% default
      transitionType: transition_type,
      aspectRatio: aspect_ratio || '16:9'
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

if target_route in routes_code:
    routes_code = routes_code.replace(target_route, replacement_route)
    with open(routes_path, 'w', encoding='utf-8') as f:
        f.write(routes_code)
    print('Successfully patched routes.js')
else:
    print('Warning: target_route not found in routes.js, checking alternate match...')
    idx = routes_code.find("router.post('/projects/:id/render'")
    if idx != -1:
        end_idx = routes_code.find('});', idx) + 3
        routes_code = routes_code[:idx] + replacement_route + routes_code[end_idx:]
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(routes_code)
        print('Successfully replaced render route by index in routes.js')

# 2. Patch render_engine.js
render_path = r'E:\stickman-video-automation\studio\server\render_engine.js'
with open(render_path, 'r', encoding='utf-8') as f:
    render_code = f.read()

target_render_fn_head = """  async renderProjectVideo(projectId, {
    outputFileName = null,
    includeMusic = true,
    includeSfx = true,
    musicVolume = 0.07, // STRICT REQUIREMENT: DEFAULT MUSIC VOLUME = 7%
    transitionType = 'cut',
    aspectRatio = '16:9'
  } = {}) {"""

replacement_render_fn_head = """  async renderProjectVideo(projectId, {
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
  } = {}) {"""

if target_render_fn_head in render_code:
    render_code = render_code.replace(target_render_fn_head, replacement_render_fn_head)

target_video_filter = """    // Video filter: Scale and letterbox to exact 1920x1080
    const videoFilter = `scale=${targetW}:${targetH}:force_original_aspect_ratio=decrease,pad=${targetW}:${targetH}:(ow-iw)/2:(oh-ih)/2:color=black,fps=30`;"""

replacement_video_filter = """    // Video filter: Scale and letterbox to exact target resolution with broadcast FPS
    let videoFilter = `scale=${targetW}:${targetH}:force_original_aspect_ratio=decrease,pad=${targetW}:${targetH}:(ow-iw)/2:(oh-ih)/2:color=black,fps=${fps || 30}`;

    // Apply Atmospheric & Post-Production Effects
    if (effectsPreset === 'cyberpunk') {
      videoFilter += `,hue=s=1.6:h=25,eq=contrast=1.3:brightness=0.03`;
    } else if (effectsPreset === 'noir' || effectsPreset === 'b_w') {
      videoFilter += `,hue=s=0,eq=contrast=1.45:brightness=-0.04`;
    } else if (effectsPreset === 'warm') {
      videoFilter += `,colorchannelmixer=rr=1.15:rg=0.05:bb=0.85,eq=saturation=1.2`;
    } else if (effectsPreset === 'cool') {
      videoFilter += `,colorchannelmixer=rr=0.85:bb=1.25,eq=saturation=1.15`;
    } else if (effectsPreset === 'vintage') {
      videoFilter += `,colorchannelmixer=rr=1.1:rg=0.05:bb=0.8,eq=contrast=1.1:saturation=0.85`;
    } else if (effectsPreset === 'vivid') {
      videoFilter += `,eq=contrast=1.25:saturation=1.6`;
    } else if (effectsPreset === 'moody_dark') {
      videoFilter += `,eq=contrast=1.35:brightness=-0.1:saturation=0.9`;
    } else if (effectsPreset === 'golden_hour') {
      videoFilter += `,colorchannelmixer=rr=1.2:gg=1.05:bb=0.7,eq=contrast=1.15:saturation=1.3`;
    } else if (effectsPreset === 'dreamy') {
      videoFilter += `,gblur=sigma=1.2,eq=contrast=1.08:brightness=0.05:saturation=1.2`;
    } else if (effectsPreset === 'neon') {
      videoFilter += `,hue=s=1.6:h=-20,eq=contrast=1.35`;
    } else if (effectsPreset === 'sepia') {
      videoFilter += `,colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131,eq=contrast=1.1`;
    } else if (effectsPreset === 'invert') {
      videoFilter += `,negate`;
    } else if (effectsPreset === 'pastel') {
      videoFilter += `,eq=contrast=0.95:brightness=0.06:saturation=0.85`;
    } else if (effectsPreset === 'frost') {
      videoFilter += `,colorchannelmixer=rr=0.85:bb=1.3,eq=contrast=1.15:saturation=0.9`;
    } else if (effectsPreset === 'sunset') {
      videoFilter += `,colorchannelmixer=rr=1.25:gg=0.85:bb=0.95,eq=contrast=1.2:saturation=1.35`;
    } else if (effectsPreset === 'ocean') {
      videoFilter += `,colorchannelmixer=rr=0.75:gg=1.1:bb=1.35,eq=contrast=1.2:saturation=1.25`;
    } else if (effectsPreset === 'bright') {
      videoFilter += `,eq=contrast=1.1:brightness=0.08:saturation=1.1`;
    }

    if (vignetteEnabled) {
      videoFilter += `,vignette=PI/4`;
    }
    if (sharpenEnabled) {
      videoFilter += `,unsharp=5:5:1.0:5:5:0.0`;
    }
    if (blurAmount > 0) {
      videoFilter += `,gblur=sigma=${Math.min(blurAmount, 10)}`;
    }
    if (grainEnabled) {
      videoFilter += `,noise=c1s=8:c1f=t+u`;
    }"""

if target_video_filter in render_code:
    render_code = render_code.replace(target_video_filter, replacement_video_filter)
    with open(render_path, 'w', encoding='utf-8') as f:
        f.write(render_code)
    print('Successfully patched render_engine.js')
else:
    print('Warning: target_video_filter not found directly in render_engine.js')

print('Patch script finished.')
