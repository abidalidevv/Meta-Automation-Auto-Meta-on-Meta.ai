import os
import sys

index_html_path = r'E:\stickman-video-automation\studio\public\index.html'

with open(index_html_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- RIGHT COLUMN: CAPCUT CAPTION CUSTOMIZER'
start_idx = html.find(start_marker)
if start_idx == -1:
    print('Error: start_marker not found')
    sys.exit(1)

cap_start = html.find('<!-- Master Caption Toggle -->', start_idx)
target_closing = '</div>\n          </div>\n\n        </div>\n      </section>'
close_idx = html.find(target_closing, start_idx)

if cap_start == -1 or close_idx == -1:
    print('Error: boundaries not found')
    sys.exit(1)

existing_captions_html = html[cap_start:close_idx].strip()

new_panel_html = f'''<!-- RIGHT COLUMN: TOOLS & ASSETS ADVANCED POST-PRODUCTION SUITE -->
          <div class="caption-inspector tools-assets-panel">
            <div class="tools-panel-header">
              <div class="tools-panel-title-row">
                <span class="tools-panel-title">TOOLS & ASSETS</span>
                <span class="brand-badge" id="toolsActiveModeBadge" style="background: rgba(0, 240, 255, 0.15); color: var(--cyan); font-size: 10.5px;">✨ Effects</span>
              </div>
              <div class="tools-tab-bar">
                <button type="button" class="tools-tab-btn active" id="toolTab-effects" onclick="switchToolsTab('effects')">
                  <span>✨</span> Effects
                </button>
                <button type="button" class="tools-tab-btn" id="toolTab-captions" onclick="switchToolsTab('captions')">
                  <span>💬</span> Captions
                </button>
                <button type="button" class="tools-tab-btn" id="toolTab-motion" onclick="switchToolsTab('motion')">
                  <span>⚡</span> Motion
                </button>
                <button type="button" class="tools-tab-btn" id="toolTab-audio" onclick="switchToolsTab('audio')">
                  <span>🔊</span> Audio / SFX
                </button>
                <button type="button" class="tools-tab-btn" id="toolTab-media" onclick="switchToolsTab('media')">
                  <span>📁</span> Media
                </button>
              </div>
            </div>

            <!-- ================= TAB 1: EFFECTS (ATMOSPHERIC 20 + PRO FX) ================= -->
            <div class="tools-tab-content" id="tabContent-effects">
              <!-- Atmospheric Effects 20 -->
              <div class="atmos-section-header">
                <div class="atmos-section-title">
                  <span>Atmospheric Effects</span>
                  <span class="atmos-count-badge">20</span>
                </div>
                <button type="button" class="btn btn-secondary" onclick="resetAtmosphericEffects()" style="font-size: 10px; padding: 2px 8px;">↺ Reset Look</button>
              </div>

              <!-- 20 Cards Grid -->
              <div class="atmos-grid">
                <div class="atmos-card atmos-normal active" data-preset="normal" onclick="selectAtmosphericEffect('normal')">
                  <span class="atmos-card-label">Normal</span>
                </div>
                <div class="atmos-card atmos-bright light-theme" data-preset="bright" onclick="selectAtmosphericEffect('bright')">
                  <span class="atmos-card-label">Bright</span>
                </div>
                <div class="atmos-card atmos-moody-dark" data-preset="moody_dark" onclick="selectAtmosphericEffect('moody_dark')">
                  <span class="atmos-card-label">Moody Dark</span>
                </div>
                <div class="atmos-card atmos-warm" data-preset="warm" onclick="selectAtmosphericEffect('warm')">
                  <span class="atmos-card-label">Warm</span>
                </div>
                <div class="atmos-card atmos-cool" data-preset="cool" onclick="selectAtmosphericEffect('cool')">
                  <span class="atmos-card-label">Cool</span>
                </div>
                <div class="atmos-card atmos-vintage" data-preset="vintage" onclick="selectAtmosphericEffect('vintage')">
                  <span class="atmos-card-label">Vintage</span>
                </div>
                <div class="atmos-card atmos-bw" data-preset="b_w" onclick="selectAtmosphericEffect('b_w')">
                  <span class="atmos-card-label">B&W</span>
                </div>
                <div class="atmos-card atmos-vivid" data-preset="vivid" onclick="selectAtmosphericEffect('vivid')">
                  <span class="atmos-card-label">Vivid</span>
                </div>
                <div class="atmos-card atmos-dreamy light-theme" data-preset="dreamy" onclick="selectAtmosphericEffect('dreamy')">
                  <span class="atmos-card-label">Dreamy</span>
                </div>
                <div class="atmos-card atmos-neon" data-preset="neon" onclick="selectAtmosphericEffect('neon')">
                  <span class="atmos-card-label">Neon</span>
                </div>
                <div class="atmos-card atmos-golden-hour" data-preset="golden_hour" onclick="selectAtmosphericEffect('golden_hour')">
                  <span class="atmos-card-label">Golden Hour</span>
                </div>
                <div class="atmos-card atmos-cyberpunk" data-preset="cyberpunk" onclick="selectAtmosphericEffect('cyberpunk')">
                  <span class="atmos-card-label">Cyberpunk</span>
                </div>
                <div class="atmos-card atmos-noir" data-preset="noir" onclick="selectAtmosphericEffect('noir')">
                  <span class="atmos-card-label">Noir</span>
                </div>
                <div class="atmos-card atmos-sepia" data-preset="sepia" onclick="selectAtmosphericEffect('sepia')">
                  <span class="atmos-card-label">Sepia</span>
                </div>
                <div class="atmos-card atmos-invert" data-preset="invert" onclick="selectAtmosphericEffect('invert')">
                  <span class="atmos-card-label">Invert</span>
                </div>
                <div class="atmos-card atmos-pastel light-theme" data-preset="pastel" onclick="selectAtmosphericEffect('pastel')">
                  <span class="atmos-card-label">Pastel</span>
                </div>
                <div class="atmos-card atmos-frost light-theme" data-preset="frost" onclick="selectAtmosphericEffect('frost')">
                  <span class="atmos-card-label">Frost</span>
                </div>
                <div class="atmos-card atmos-sunset" data-preset="sunset" onclick="selectAtmosphericEffect('sunset')">
                  <span class="atmos-card-label">Sunset</span>
                </div>
                <div class="atmos-card atmos-ocean" data-preset="ocean" onclick="selectAtmosphericEffect('ocean')">
                  <span class="atmos-card-label">Ocean</span>
                </div>
                <div class="atmos-card atmos-chromatic" data-preset="chromatic" onclick="selectAtmosphericEffect('chromatic')">
                  <span class="atmos-card-label">Chromatic</span>
                </div>
              </div>

              <!-- Adobe Premiere & After Effects Pro Sliders -->
              <div class="inspector-section" style="margin-top: 10px;">
                <div class="section-title">
                  <span>🎛️ Premiere & After Effects Pro Controls</span>
                  <span class="brand-badge" style="font-size: 9.5px;">Live Canvas</span>
                </div>

                <!-- Gaussian Blur -->
                <div style="margin-bottom: 8px;">
                  <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                    <span style="color: #cbd5e1;">Gaussian Blur</span>
                    <span id="fxBlurVal" style="color: var(--cyan); font-family: var(--font-mono);">0px</span>
                  </div>
                  <input type="range" id="fxBlurSlider" min="0" max="15" step="0.5" value="0" class="form-input" style="padding: 2px 0;" oninput="updateCustomEffectSliders()">
                </div>

                <!-- Lumetri Exposure -->
                <div style="margin-bottom: 8px;">
                  <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                    <span style="color: #cbd5e1;">Lumetri Exposure</span>
                    <span id="fxExposureVal" style="color: var(--cyan); font-family: var(--font-mono);">0%</span>
                  </div>
                  <input type="range" id="fxExposureSlider" min="-50" max="50" step="5" value="0" class="form-input" style="padding: 2px 0;" oninput="updateCustomEffectSliders()">
                </div>

                <!-- Lumetri Contrast -->
                <div style="margin-bottom: 8px;">
                  <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                    <span style="color: #cbd5e1;">Lumetri Contrast</span>
                    <span id="fxContrastVal" style="color: var(--cyan); font-family: var(--font-mono);">100%</span>
                  </div>
                  <input type="range" id="fxContrastSlider" min="50" max="180" step="5" value="100" class="form-input" style="padding: 2px 0;" oninput="updateCustomEffectSliders()">
                </div>

                <!-- Lumetri Saturation -->
                <div style="margin-bottom: 10px;">
                  <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                    <span style="color: #cbd5e1;">Lumetri Saturation</span>
                    <span id="fxSaturationVal" style="color: var(--cyan); font-family: var(--font-mono);">100%</span>
                  </div>
                  <input type="range" id="fxSaturationSlider" min="0" max="220" step="10" value="100" class="form-input" style="padding: 2px 0;" oninput="updateCustomEffectSliders()">
                </div>

                <!-- Toggles Row: Vignette, Film Grain, Sharpen, Glow -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 4px;">
                  <label style="display: flex; align-items: center; gap: 8px; font-size: 11.5px; color: #fff; cursor: pointer; background: rgba(255,255,255,0.04); padding: 6px 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
                    <input type="checkbox" id="fxVignetteToggle" onchange="updateCustomEffectSliders()">
                    <span>🎬 Vignette</span>
                  </label>
                  <label style="display: flex; align-items: center; gap: 8px; font-size: 11.5px; color: #fff; cursor: pointer; background: rgba(255,255,255,0.04); padding: 6px 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
                    <input type="checkbox" id="fxGrainToggle" onchange="updateCustomEffectSliders()">
                    <span>🎞️ Film Grain</span>
                  </label>
                  <label style="display: flex; align-items: center; gap: 8px; font-size: 11.5px; color: #fff; cursor: pointer; background: rgba(255,255,255,0.04); padding: 6px 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
                    <input type="checkbox" id="fxSharpenToggle" onchange="updateCustomEffectSliders()">
                    <span>🔪 Sharpen</span>
                  </label>
                  <label style="display: flex; align-items: center; gap: 8px; font-size: 11.5px; color: #fff; cursor: pointer; background: rgba(255,255,255,0.04); padding: 6px 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.06);">
                    <input type="checkbox" id="fxGlowToggle" onchange="updateCustomEffectSliders()">
                    <span>✨ CC Glow</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- ================= TAB 2: CAPTIONS ================= -->
            <div class="tools-tab-content" id="tabContent-captions" style="display: none;">
              {existing_captions_html}
            </div>

            <!-- ================= TAB 3: MOTION & TRANSITIONS ================= -->
            <div class="tools-tab-content" id="tabContent-motion" style="display: none;">
              <!-- Premiere Transitions -->
              <div class="inspector-section">
                <div class="section-title">
                  <span>🎬 Adobe Premiere Pro Transitions</span>
                  <span class="brand-badge" id="activeTransitionBadge">Cross Dissolve</span>
                </div>
                <div class="motion-grid">
                  <div class="motion-card active" data-transition="cross_dissolve" onclick="selectTransitionPreset('cross_dissolve', this)">
                    <div class="motion-card-title">Cross Dissolve</div>
                    <div class="motion-card-sub">Smooth opacity blending</div>
                  </div>
                  <div class="motion-card" data-transition="dip_black" onclick="selectTransitionPreset('dip_black', this)">
                    <div class="motion-card-title">Dip to Black</div>
                    <div class="motion-card-sub">Dramatic scene break fade</div>
                  </div>
                  <div class="motion-card" data-transition="dip_white" onclick="selectTransitionPreset('dip_white', this)">
                    <div class="motion-card-title">Dip to White</div>
                    <div class="motion-card-sub">Cinematic flash transition</div>
                  </div>
                  <div class="motion-card" data-transition="film_dissolve" onclick="selectTransitionPreset('film_dissolve', this)">
                    <div class="motion-card-title">Film Dissolve</div>
                    <div class="motion-card-sub">Optical film exposure curve</div>
                  </div>
                  <div class="motion-card" data-transition="morph_cut" onclick="selectTransitionPreset('morph_cut', this)">
                    <div class="motion-card-title">Morph Cut</div>
                    <div class="motion-card-sub">Seamless cut interpolation</div>
                  </div>
                  <div class="motion-card" data-transition="zoom_trans" onclick="selectTransitionPreset('zoom_trans', this)">
                    <div class="motion-card-title">Zoom / Transform</div>
                    <div class="motion-card-sub">High-energy push zoom</div>
                  </div>
                  <div class="motion-card" data-transition="push_trans" onclick="selectTransitionPreset('push_trans', this)">
                    <div class="motion-card-title">Push Transition</div>
                    <div class="motion-card-sub">Linear screen wipe slide</div>
                  </div>
                  <div class="motion-card" data-transition="whip_blur" onclick="selectTransitionPreset('whip_blur', this)">
                    <div class="motion-card-title">Whip / Blur</div>
                    <div class="motion-card-sub">High-speed motion blur pan</div>
                  </div>
                </div>
              </div>

              <!-- After Effects Camera Movement -->
              <div class="inspector-section" style="margin-top: 10px;">
                <div class="section-title">
                  <span>🎥 After Effects Camera & Animation</span>
                  <span class="brand-badge" id="activeMotionBadge">Push-In Zoom</span>
                </div>
                <div class="motion-grid">
                  <div class="motion-card active" data-motion="motion-zoom-in" onclick="selectMotionPreset('motion-zoom-in', this)">
                    <div class="motion-card-title">Camera Push-In</div>
                    <div class="motion-card-sub">Subtle continuous zoom in</div>
                  </div>
                  <div class="motion-card" data-motion="motion-zoom-out" onclick="selectMotionPreset('motion-zoom-out', this)">
                    <div class="motion-card-title">Camera Pull-Out</div>
                    <div class="motion-card-sub">Wide reveal slow zoom out</div>
                  </div>
                  <div class="motion-card" data-motion="motion-pan-left" onclick="selectMotionPreset('motion-pan-left', this)">
                    <div class="motion-card-title">Pan Left &rarr; Right</div>
                    <div class="motion-card-sub">Horizontal tracking motion</div>
                  </div>
                  <div class="motion-card" data-motion="motion-pan-right" onclick="selectMotionPreset('motion-pan-right', this)">
                    <div class="motion-card-title">Pan Right &rarr; Left</div>
                    <div class="motion-card-sub">Reverse tracking camera</div>
                  </div>
                  <div class="motion-card" data-motion="motion-parallax" onclick="selectMotionPreset('motion-parallax', this)">
                    <div class="motion-card-title">2.5D Parallax</div>
                    <div class="motion-card-sub">Multi-plane dynamic depth</div>
                  </div>
                  <div class="motion-card" data-motion="motion-3d" onclick="selectMotionPreset('motion-3d', this)">
                    <div class="motion-card-title">3D Camera Move</div>
                    <div class="motion-card-sub">Perspective tilt & orbit</div>
                  </div>
                  <div class="motion-card" data-motion="motion-whip" onclick="selectMotionPreset('motion-whip', this)">
                    <div class="motion-card-title">Whip & Shake</div>
                    <div class="motion-card-sub">Snappy kinetic snap</div>
                  </div>
                  <div class="motion-card" data-motion="motion-ease" onclick="selectMotionPreset('motion-ease', this)">
                    <div class="motion-card-title">Easy Ease / Graph</div>
                    <div class="motion-card-sub">Velocitized smooth curve</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- ================= TAB 4: AUDIO & SOUND EFFECTS (SFX) ================= -->
            <div class="tools-tab-content" id="tabContent-audio" style="display: none;">
              <!-- Background Music Volume Ducking Control -->
              <div class="inspector-section" style="background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.25);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span style="font-size: 12px; font-weight: 700; color: #fff;">🎵 Ducked Background Music</span>
                  <span class="brand-badge" id="musicDuckingBadge" style="background: rgba(16, 185, 129, 0.2); color: var(--emerald);">7% (Standard)</span>
                </div>
                <input type="range" id="renderMusicVolumeSlider" min="0" max="30" value="7" class="form-input" style="padding: 2px 0;" oninput="document.getElementById('musicDuckingBadge').textContent = this.value + '%'; window.renderMusicVolume = this.value / 100;">
              </div>

              <!-- Category 1: Whooshes & Swishes -->
              <div class="sfx-category-header"><span>💨</span> Whooshes & Swishes</div>
              <div class="sfx-grid">
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('whoosh')" title="Play Preview">▶</button>
                  <span class="sfx-name">Whoosh</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Whoosh')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('fast_whoosh')" title="Play Preview">▶</button>
                  <span class="sfx-name">Fast Whoosh</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Fast Whoosh')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('short_whoosh')" title="Play Preview">▶</button>
                  <span class="sfx-name">Short Whoosh</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Short Whoosh')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('whoosh_trans')" title="Play Preview">▶</button>
                  <span class="sfx-name">Whoosh Transition</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Whoosh Trans')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('swish')" title="Play Preview">▶</button>
                  <span class="sfx-name">Swish</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Swish')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('fast_swish')" title="Play Preview">▶</button>
                  <span class="sfx-name">Fast Swish</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Fast Swish')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('air_whoosh')" title="Play Preview">▶</button>
                  <span class="sfx-name">Air Whoosh</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Air Whoosh')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('reverse_whoosh')" title="Play Preview">▶</button>
                  <span class="sfx-name">Reverse Whoosh</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Reverse Whoosh')">+ Scene</button>
                </div>
              </div>

              <!-- Category 2: Impacts & Hits -->
              <div class="sfx-category-header"><span>💥</span> Impacts & Hits</div>
              <div class="sfx-grid">
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('cinematic_impact')" title="Play Preview">▶</button>
                  <span class="sfx-name">Cinematic Impact</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Cinematic Impact')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('deep_impact')" title="Play Preview">▶</button>
                  <span class="sfx-name">Deep Impact</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Deep Impact')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('bass_impact')" title="Play Preview">▶</button>
                  <span class="sfx-name">Bass Impact</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Bass Impact')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('trailer_hit')" title="Play Preview">▶</button>
                  <span class="sfx-name">Trailer Hit</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Trailer Hit')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('cinematic_hit')" title="Play Preview">▶</button>
                  <span class="sfx-name">Cinematic Hit</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Cinematic Hit')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('boom_hit')" title="Play Preview">▶</button>
                  <span class="sfx-name">Boom Hit</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Boom Hit')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('low_boom')" title="Play Preview">▶</button>
                  <span class="sfx-name">Low Boom</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Low Boom')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('sub_boom')" title="Play Preview">▶</button>
                  <span class="sfx-name">Sub Boom</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Sub Boom')">+ Scene</button>
                </div>
              </div>

              <!-- Category 3: Build-ups & Risers -->
              <div class="sfx-category-header"><span>📈</span> Build-up & Risers</div>
              <div class="sfx-grid">
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('cinematic_riser')" title="Play Preview">▶</button>
                  <span class="sfx-name">Cinematic Riser</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Cinematic Riser')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('whoosh_riser')" title="Play Preview">▶</button>
                  <span class="sfx-name">Whoosh Riser</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Whoosh Riser')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('tension_riser')" title="Play Preview">▶</button>
                  <span class="sfx-name">Tension Riser</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Tension Riser')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('reverse_riser')" title="Play Preview">▶</button>
                  <span class="sfx-name">Reverse Riser</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Reverse Riser')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('impact_riser')" title="Play Preview">▶</button>
                  <span class="sfx-name">Impact Riser</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Impact Riser')">+ Scene</button>
                </div>
              </div>

              <!-- Category 4: Documentary & Background -->
              <div class="sfx-category-header"><span>🌧️</span> Documentary & Ambience</div>
              <div class="sfx-grid">
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('dark_ambience')" title="Play Preview">▶</button>
                  <span class="sfx-name">Dark Ambience</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Dark Ambience')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('cinematic_ambience')" title="Play Preview">▶</button>
                  <span class="sfx-name">Cinematic Ambience</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Cinema Ambience')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('wind_ambience')" title="Play Preview">▶</button>
                  <span class="sfx-name">Wind Ambience</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Wind Ambience')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('rain_ambience')" title="Play Preview">▶</button>
                  <span class="sfx-name">Rain Ambience</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Rain Ambience')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('crowd_ambience')" title="Play Preview">▶</button>
                  <span class="sfx-name">Crowd Ambience</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Crowd Ambience')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('room_tone')" title="Play Preview">▶</button>
                  <span class="sfx-name">Room Tone</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Room Tone')">+ Scene</button>
                </div>
              </div>

              <!-- Category 5: Small UI & Graphic Sounds -->
              <div class="sfx-category-header"><span>🖱️</span> UI & Graphic Micro Sounds</div>
              <div class="sfx-grid">
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('click')" title="Play Preview">▶</button>
                  <span class="sfx-name">Click</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Click')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('tick')" title="Play Preview">▶</button>
                  <span class="sfx-name">Tick</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Tick')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('pop')" title="Play Preview">▶</button>
                  <span class="sfx-name">Pop</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Pop')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('digital_click')" title="Play Preview">▶</button>
                  <span class="sfx-name">Digital Click</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Digital Click')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('camera_shutter')" title="Play Preview">▶</button>
                  <span class="sfx-name">Camera Shutter</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Camera Shutter')">+ Scene</button>
                </div>
                <div class="sfx-card">
                  <button type="button" class="sfx-play-btn" onclick="playSfx('glitch_hit')" title="Play Preview">▶</button>
                  <span class="sfx-name">Glitch Hit</span>
                  <button type="button" class="sfx-attach-btn" onclick="attachSfxToCurrentScene('Glitch Hit')">+ Scene</button>
                </div>
              </div>
            </div>

            <!-- ================= TAB 5: MEDIA INSPECTOR ================= -->
            <div class="tools-tab-content" id="tabContent-media" style="display: none;">
              <div class="inspector-section">
                <div class="section-title">
                  <span id="mediaInspectorTitle">🎬 Active Scene #01</span>
                  <span class="brand-badge" id="mediaInspectorBadge">Prompt 001</span>
                </div>

                <div style="display: flex; gap: 12px; margin-bottom: 12px; align-items: center;">
                  <img id="mediaInspectorThumb" src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 60'><rect width='100' height='60' fill='%231a1a2e'/></svg>" style="width: 80px; height: 50px; border-radius: 6px; object-fit: cover; border: 1px solid var(--border-subtle);" alt="Active Thumb" />
                  <div style="flex: 1; font-size: 11.5px;">
                    <div>Duration: <strong id="mediaInspectorDuration" style="color: var(--cyan);">1.33s</strong></div>
                    <div style="color: var(--text-dim); margin-top: 2px;">Resolution: <span id="mediaInspectorRes">1024x1024</span></div>
                    <div style="color: var(--emerald); margin-top: 2px;">Status: Valid QA Asset</div>
                  </div>
                </div>

                <div style="margin-bottom: 10px;">
                  <label class="form-label" style="font-size: 11px;">Prompt Description</label>
                  <div id="mediaInspectorPromptText" style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 8px 10px; font-size: 11.5px; color: #cbd5e1; max-height: 100px; overflow-y: auto; line-height: 1.4;">
                    Select or click any scene card in the CapCut timeline to view prompt instructions.
                  </div>
                </div>

                <div style="display: flex; gap: 8px; margin-top: 10px;">
                  <label class="btn btn-secondary" style="flex: 1; justify-content: center; font-size: 11px; cursor: pointer;">
                    <span>📁</span> Replace Image
                    <input type="file" accept="image/*" style="display: none;" onchange="onReplaceSceneImage(this)" />
                  </label>
                  <button type="button" class="btn btn-secondary" onclick="openLightbox(document.getElementById('playerCanvasImage').src, 'active', 'Scene Preview')" style="font-size: 11px;">
                    🔍 Full View
                  </button>
                </div>
              </div>
            </div>
          </div>'''

new_html = html[:start_idx] + new_panel_html + html[close_idx + len('</div>\n          </div>'):]

with open(index_html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Successfully patched index.html!')
