import re
import os

print("Starting UI Mode 1 & 2 update...")

index_file = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Locate the Mode 1 subViewMode1 card
# We want to replace from inside <div id="subViewMode1" class="sub-view-content"> down to right before </div><!-- END OF subViewMode1 --> or the closing of card

old_subview_mode1_pat = r'(<div id="subViewMode1" class="sub-view-content">)[\s\S]*?(</div>\s*<!-- SUB VIEW B: MODE 2)'

new_subview_mode1_content = r'''\1
            <div class="card">
              <div class="card-header">
                <div class="card-title-group">
                  <div class="card-icon">⚡</div>
                  <div>
                    <div class="card-title">Mode 1: Groq AI Story Engine</div>
                    <div class="card-subtitle">Generate complete sequential stickman prompts from story script with character consistency</div>
                  </div>
                </div>
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                  <span class="brand-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--emerald); border-color: rgba(16, 185, 129, 0.3);">⚡ Groq: llama-3.3-70b (Auto Fallbacks)</span>
                  <span id="m1PromptEstimateBadge" class="brand-badge">~683 stickman prompts</span>
                  <!-- Hidden model select for JS compatibility -->
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

                <!-- Collapsible Details for Character Consistency -->
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

          <!-- SUB VIEW B: MODE 2'''

html = re.sub(old_subview_mode1_pat, lambda m: new_subview_mode1_content, html)

# Also update Mode 2 header button text to clarify
html = html.replace(
    'Upload .txt / .md File',
    'Import Prompts from File (.txt / .md)'
)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
