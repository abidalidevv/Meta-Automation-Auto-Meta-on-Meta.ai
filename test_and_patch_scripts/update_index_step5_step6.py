import os
import sys

index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Step 5 defaults: 4K UHD, 60 FPS, ultrafast, CRF 18
s5_target_start = code.find('<section id="step-5-panel" class="view-panel">')
s5_target_end = code.find('</section>', s5_target_start)

if s5_target_start == -1 or s5_target_end == -1:
    print('Error: Could not find step-5-panel')
    sys.exit(1)

new_step5 = '''<section id="step-5-panel" class="view-panel">
        <div class="grid-2">
          
          <!-- Render Config Card -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">🎬</div>
                <div>
                  <div class="card-title">Broadcast & Ultra HD Render Engine</div>
                  <div class="card-subtitle">FFmpeg 4K / 1080p High-Speed Multi-Threaded H.264 MP4 Export</div>
                </div>
              </div>
              <span class="brand-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--emerald);">60 FPS Master Ready</span>
            </div>

            <!-- Resolution Selector -->
            <div class="form-group">
              <label class="form-label" style="display: flex; justify-content: space-between;">
                <span>Video Format & Resolution</span>
                <span id="resBadge" style="color: var(--cyan); font-weight: 700;">🌟 4K Ultra HD (3840x2160)</span>
              </label>
              <select id="renderResolution" class="form-select" onchange="onRenderResolutionChange(this.value)">
                <option value="3840x2160" selected>🌟 3840x2160 (16:9 - 4K Ultra HD Master - YouTube 4K Quality)</option>
                <option value="2560x1440">💎 2560x1440 (16:9 - 2K Quad HD / 1440p High-Res)</option>
                <option value="1920x1080">🎬 1920x1080 (16:9 - 1080p Full HD Broadcast Standard)</option>
                <option value="2160x3840">📱 2160x3840 (9:16 - 4K Ultra HD Vertical Shorts / Reels Ultra)</option>
                <option value="1080x1920">📱 1080x1920 (9:16 - 1080p Vertical Shorts / TikTok / Reels)</option>
              </select>
            </div>

            <!-- Frame Rate (FPS) and Speed Preset -->
            <div class="grid-2">
              <div class="form-group">
                <label class="form-label" style="display: flex; justify-content: space-between;">
                  <span>Frame Rate (FPS)</span>
                  <span style="color: var(--emerald); font-weight: 700;">60 FPS (Default Master)</span>
                </label>
                <div style="display: flex; gap: 6px;">
                  <input type="number" id="renderFps" class="form-input" value="60" min="24" max="120" style="width: 80px;" />
                  <button type="button" class="btn btn-secondary" onclick="document.getElementById('renderFps').value = 60;" style="flex: 1; font-size: 11px; padding: 4px 6px;">60 FPS</button>
                  <button type="button" class="btn btn-secondary" onclick="document.getElementById('renderFps').value = 30;" style="flex: 1; font-size: 11px; padding: 4px 6px;">30 FPS</button>
                  <button type="button" class="btn btn-secondary" onclick="document.getElementById('renderFps').value = 24;" style="flex: 1; font-size: 11px; padding: 4px 6px;">24 FPS</button>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Render Speed / Encoding Preset</label>
                <select id="renderSpeedPreset" class="form-select">
                  <option value="ultrafast" selected>⚡ ultrafast (Lightning Fast Export — 5x Speed)</option>
                  <option value="superfast">🚀 superfast (Ultra-Fast Render)</option>
                  <option value="veryfast">⚡ veryfast (Fast & Balanced — High Quality)</option>
                  <option value="fast">📦 fast (Standard)</option>
                  <option value="medium">💎 medium (Maximum Compression)</option>
                </select>
              </div>
            </div>

            <!-- Visual Quality & Audio Bitrate -->
            <div class="grid-2">
              <div class="form-group">
                <label class="form-label">Video Fidelity (CRF Profile)</label>
                <select id="renderCrf" class="form-select">
                  <option value="18" selected>🌟 Ultra HD Lossless (CRF 18 — High Bitrate)</option>
                  <option value="20">🎬 Broadcast Master (CRF 20 — Standard)</option>
                  <option value="23">📦 Web Compression (CRF 23 — Compact)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Audio Quality & Bitrate</label>
                <select id="renderAudioBitrate" class="form-select">
                  <option value="320k" selected>🔊 320 kbps (Studio Master AAC Audio)</option>
                  <option value="192k">🔉 192 kbps (Standard High Quality)</option>
                  <option value="128k">🔈 128 kbps (Compact Web Audio)</option>
                </select>
              </div>
            </div>

            <!-- Performance Toggles -->
            <div class="grid-2" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 10px 14px; margin-bottom: 12px;">
              <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: #fff; cursor: pointer;">
                <input type="checkbox" id="renderMotionToggle" checked style="width: 18px; height: 18px; accent-color: var(--cyan);" />
                <span>Dynamic Pan & Slow Zoom</span>
              </label>

              <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: #fff; cursor: pointer;">
                <input type="checkbox" id="renderHwaccelToggle" checked style="width: 18px; height: 18px; accent-color: var(--cyan);" />
                <span>Multi-Core Multi-Threading (threads=0)</span>
              </label>
            </div>

            <button id="btnStartRender" class="btn btn-primary" onclick="triggerRender()" style="width: 100%; justify-content: center; padding: 14px; font-size: 15px; font-weight: 800;">
              <span>🎬</span> Export Ultra HD 4K / 60 FPS MP4 Video
            </button>

            <!-- Render Status Box -->
            <div id="renderStatusCard" style="display: none; margin-top: 18px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: var(--radius-sm); padding: 16px;">
              <div style="height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; margin-bottom: 10px;">
                <div id="renderBar" style="width: 0%; height: 100%; background: var(--grad-brand); transition: width 0.4s ease;"></div>
              </div>
              <div style="display: flex; justify-content: space-between; font-size: 12px;">
                <span id="renderStatusText" style="color: var(--cyan); font-weight: 600;">Exporting 4K 60FPS Video...</span>
                <span id="renderPercent" style="font-family: var(--font-mono); font-weight: 700;">0%</span>
              </div>
            </div>
          </div>

          <!-- Video Preview & Master Player Card -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">📺</div>
                <div>
                  <div class="card-title">Exported Video Master Player</div>
                  <div class="card-subtitle">In-Page MP4 Player with Instant Download & Folder Access</div>
                </div>
              </div>
              <span id="renderSuccessBadge" class="brand-badge" style="display: none; background: rgba(16, 185, 129, 0.2); color: var(--emerald);">Ready</span>
            </div>

            <!-- In-page HTML5 Video Player -->
            <div style="background: #000; border-radius: var(--radius-sm); overflow: hidden; margin-bottom: 14px; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border-subtle); position: relative;">
              <video id="step5MasterPlayer" controls style="width: 100%; height: 100%; display: none; object-fit: contain;"></video>
              <div id="step5PlayerPlaceholder" style="text-align: center; color: var(--text-muted); padding: 20px;">
                <div style="font-size: 38px; margin-bottom: 10px; opacity: 0.6;">🎬</div>
                <div style="font-size: 13px; font-weight: 600; color: #fff;">No Rendered Master Yet</div>
                <div style="font-size: 11px; margin-top: 4px;">Click "Export Ultra HD 4K / 60 FPS MP4 Video" to generate and preview your video here!</div>
              </div>
            </div>

            <!-- Video File Metadata Info & Action Buttons -->
            <div id="step5VideoMetaBox" style="display: none; background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 14px; font-size: 12px;">
              <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: var(--text-muted);">Master File:</span>
                <span id="step5FileName" style="font-family: var(--font-mono); font-weight: 700; color: #fff;">video.mp4</span>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: var(--text-muted);">Resolution & FPS:</span>
                <span id="step5FileSpec" style="color: var(--cyan); font-weight: 700;">3840x2160 @ 60 FPS</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-muted);">Master File Size:</span>
                <span id="step5FileSize" style="font-family: var(--font-mono); color: var(--emerald); font-weight: 700;">-- MB</span>
              </div>
            </div>

            <!-- Post-Render Action Buttons -->
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <a id="step5DownloadBtn" href="#" download class="btn btn-primary" style="display: none; flex: 1; justify-content: center; text-decoration: none; padding: 11px; font-size: 13px; font-weight: 700;">
                ⬇️ Download 4K Master MP4
              </a>
              <button id="step5OpenFolderBtn" class="btn btn-secondary" onclick="openOutputFolder('output')" style="display: none; padding: 11px 16px; font-size: 13px;">
                📂 Open Output Folder
              </button>
            </div>
          </div>

        </div>
      </section>'''

code = code[:s5_target_start] + new_step5 + code[s5_target_end + len('</section>'):]

# 2. Update Step 6: Multi-API Vault + Strict 1-Worker-1-Extension Login Assistant
s6_target_start = code.find('<section id="step-6-panel" class="view-panel">')
s6_target_end = code.find('</section>', s6_target_start)

if s6_target_start == -1 or s6_target_end == -1:
    print('Error: Could not find step-6-panel')
    sys.exit(1)

new_step6 = '''<section id="step-6-panel" class="view-panel">
        <div class="grid-2">
          
          <!-- Card 1: Multi-Provider AI API Keys Vault -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">⚡</div>
                <div>
                  <div class="card-title">AI Engine & Cloud API Keys Vault</div>
                  <div class="card-subtitle">Configure Groq, ElevenLabs, OpenAI, Stability AI, and Media APIs</div>
                </div>
              </div>
            </div>

            <!-- 1. Groq Cloud API -->
            <div style="background: rgba(0, 240, 255, 0.04); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label class="form-label" style="margin-bottom: 0; font-weight: 800; color: #fff;">
                  ⚡ Groq AI Primary Key (Free & Ultra Fast)
                </label>
                <a href="https://console.groq.com/keys" target="_blank" style="font-size: 11px; color: var(--cyan); text-decoration: none;">Get Free Groq Key &rarr;</a>
              </div>
              <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                <input type="password" id="settingsGroqKeySingle" class="form-input" placeholder="gsk_..." style="font-family: var(--font-mono); font-size: 12px;" />
                <button type="button" class="btn btn-secondary" onclick="togglePasswordVisibility('settingsGroqKeySingle')" style="padding: 0 10px;">👁</button>
                <button type="button" class="btn btn-secondary" onclick="testGroqKeyConnection()" style="font-size: 11px; padding: 0 12px; white-space: nowrap;">⚡ Test Key</button>
              </div>

              <!-- Groq Multi-Key Pool (Rotator) -->
              <label class="form-label" style="font-size: 11px; display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span>Groq Key Rotation Pool (Automatic Failover, 1 per line)</span>
                <span id="keyPoolCountLabel" style="color: var(--cyan); font-weight: 700;">1 Key Loaded</span>
              </label>
              <textarea id="settingsGroqKeyPool" class="form-textarea" placeholder="gsk_key1...&#10;gsk_key2...&#10;gsk_key3..." style="font-family: var(--font-mono); font-size: 11.5px; min-height: 55px;"></textarea>

              <div class="grid-2" style="margin-top: 8px;">
                <div>
                  <label class="form-label" style="font-size: 11px;">Primary AI Model</label>
                  <input type="text" id="settingsGroqModel" class="form-input" value="llama-3.3-70b-versatile" style="font-size: 12px;" />
                </div>
                <div>
                  <label class="form-label" style="font-size: 11px;">Fallback AI Model</label>
                  <input type="text" id="settingsGroqFallback" class="form-input" value="llama-3.1-8b-instant" style="font-size: 12px;" />
                </div>
              </div>
            </div>

            <!-- 2. ElevenLabs AI Voiceover Key -->
            <div style="background: rgba(139, 92, 246, 0.04); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label class="form-label" style="margin-bottom: 0; font-weight: 800; color: #fff;">
                  🎙️ ElevenLabs API Key (Ultra-Realistic AI Voiceovers)
                </label>
                <a href="https://elevenlabs.io/app/voice-library" target="_blank" style="font-size: 11px; color: var(--violet); text-decoration: none;">elevenlabs.io &rarr;</a>
              </div>
              <div style="display: flex; gap: 8px; margin-bottom: 6px;">
                <input type="password" id="settingsElevenLabsKey" class="form-input" placeholder="ElevenLabs API Key..." style="font-family: var(--font-mono); font-size: 12px;" />
                <button type="button" class="btn btn-secondary" onclick="togglePasswordVisibility('settingsElevenLabsKey')" style="padding: 0 10px;">👁</button>
              </div>
              <div>
                <label class="form-label" style="font-size: 11px;">Default Voice ID (e.g. 21m00Tcm4TlvDq8ikWAM)</label>
                <input type="text" id="settingsElevenLabsVoiceId" class="form-input" placeholder="Default: Rachel (21m00Tcm4TlvDq8ikWAM)" style="font-size: 12px;" />
              </div>
            </div>

            <!-- 3. OpenAI & Whisper API Key -->
            <div style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label class="form-label" style="margin-bottom: 0; font-weight: 800; color: #fff;">
                  🤖 OpenAI / Whisper API Key (Optional Script & Voice Transcriptions)
                </label>
                <a href="https://platform.openai.com/api-keys" target="_blank" style="font-size: 11px; color: var(--emerald); text-decoration: none;">openai.com &rarr;</a>
              </div>
              <div style="display: flex; gap: 8px; margin-bottom: 6px;">
                <input type="password" id="settingsOpenAIKey" class="form-input" placeholder="sk-..." style="font-family: var(--font-mono); font-size: 12px;" />
                <button type="button" class="btn btn-secondary" onclick="togglePasswordVisibility('settingsOpenAIKey')" style="padding: 0 10px;">👁</button>
              </div>
              <div>
                <label class="form-label" style="font-size: 11px;">OpenAI Model</label>
                <input type="text" id="settingsOpenAIModel" class="form-input" value="gpt-4o-mini" style="font-size: 12px;" />
              </div>
            </div>

            <!-- 4. Stability AI & Stock Media API Keys -->
            <div style="background: rgba(245, 158, 11, 0.04); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label class="form-label" style="margin-bottom: 0; font-weight: 800; color: #fff;">
                  🎨 Stability AI / SDXL Key (Optional Image Generation Fallback)
                </label>
                <a href="https://platform.stability.ai" target="_blank" style="font-size: 11px; color: var(--amber); text-decoration: none;">stability.ai &rarr;</a>
              </div>
              <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                <input type="password" id="settingsStabilityKey" class="form-input" placeholder="sk-..." style="font-family: var(--font-mono); font-size: 12px;" />
                <button type="button" class="btn btn-secondary" onclick="togglePasswordVisibility('settingsStabilityKey')" style="padding: 0 10px;">👁</button>
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label class="form-label" style="margin-bottom: 0; font-weight: 800; color: #fff;">
                  🎥 Pexels Stock Footage API Key (Optional Video B-Roll)
                </label>
                <a href="https://www.pexels.com/api/" target="_blank" style="font-size: 11px; color: var(--amber); text-decoration: none;">pexels.com &rarr;</a>
              </div>
              <div style="display: flex; gap: 8px;">
                <input type="password" id="settingsPexelsKey" class="form-input" placeholder="Pexels API Key..." style="font-family: var(--font-mono); font-size: 12px;" />
                <button type="button" class="btn btn-secondary" onclick="togglePasswordVisibility('settingsPexelsKey')" style="padding: 0 10px;">👁</button>
              </div>
            </div>

            <div style="display: flex; gap: 10px; margin-top: 14px;">
              <button class="btn btn-primary" onclick="saveAllSettings()" style="flex: 1; justify-content: center; padding: 12px; font-weight: 800;">
                💾 Save All Settings & API Keys
              </button>
              <button class="btn btn-secondary" onclick="triggerReconciliation()" style="padding: 12px 16px;">
                Reconcile Storage
              </button>
            </div>
          </div>

          <!-- Card 2: 10-Worker One-Time Login Assistant (Dedicated Single-Extension Architecture) -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">🔑</div>
                <div>
                  <div class="card-title">10-Worker One-Time Login Assistant</div>
                  <div class="card-subtitle">Strict 1-Worker-1-Extension: Isolated sessions for Meta.ai OR Google Flow</div>
                </div>
              </div>
              <button class="btn btn-secondary" onclick="stopAllWorkers()" style="font-size: 11px; padding: 4px 10px; color: #f87171; border-color: rgba(248, 113, 113, 0.3);">
                🛑 Stop All Workers
              </button>
            </div>

            <!-- Architecture Info Box -->
            <div style="background: rgba(0, 240, 255, 0.04); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 14px; font-size: 12px; color: var(--text-muted); line-height: 1.5;">
              <strong style="color: #fff;">Strict Dedicated Architecture:</strong> Each worker profile runs strictly 
              <strong style="color: var(--cyan);">ONE service and ONE extension</strong> 
              (either Google Flow OR Meta.ai). No dual tabs, no dual extensions. 
              Click below to launch all 10 or launch individual workers. 
              Log in once by hand in each window. Chrome permanently persists authentication in <code style="color: #fff;">Workers/Worker-Wnn</code>, 
              so the automated farm runs continuously without re-prompting!
            </div>

            <!-- Master Launch Button -->
            <button class="btn btn-primary" onclick="openWorkerLogin('ALL')" style="width: 100%; justify-content: center; padding: 13px; font-size: 14px; font-weight: 800; margin-bottom: 14px; background: linear-gradient(135deg, #00f0ff, #8b5cf6);">
              🚀 Launch All 10 Worker Profiles for One-Time Login
            </button>

            <!-- Dynamic 10-Worker Grid (Populated by refreshFleetStatus) -->
            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
              <span>Worker Fleet Status & Individual Launch:</span>
              <span style="color: var(--cyan);">1 Worker = 1 Extension</span>
            </div>

            <div id="workersLoginAssistantGrid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 14px; max-height: 380px; overflow-y: auto;">
              <!-- Dynamic worker cards loaded via refreshFleetStatus() -->
            </div>

            <!-- Quick Directory Shortcuts -->
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <button class="btn btn-secondary" onclick="openOutputFolder('workers')" style="font-size: 11px; padding: 8px 10px; flex: 1; justify-content: center;">
                📁 Open Workers Profiles Folder
              </button>
              <button class="btn btn-secondary" onclick="openOutputFolder('logs')" style="font-size: 11px; padding: 8px 10px; flex: 1; justify-content: center;">
                📄 Open Studio Logs Folder
              </button>
            </div>
          </div>

        </div>

        <!-- Real-Time Telemetry & System Diagnostics Logs (Full Width) -->
        <div class="card" style="margin-top: 16px;">
          <div class="card-header">
            <div class="card-title-group">
              <div class="card-icon">📡</div>
              <div>
                <div class="card-title">Live Telemetry & System Diagnostics Event Stream</div>
                <div class="card-subtitle">Real-time worker lifecycle events, render logs, and physical file stream</div>
              </div>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
              <a href="/api/v1/logs/raw" target="_blank" class="btn btn-secondary" style="font-size: 11.5px; padding: 6px 12px; text-decoration: none;">
                📄 View studio.log
              </a>
              <button class="btn btn-secondary" onclick="fetchLogs()" style="font-size: 11.5px; padding: 6px 12px;">Refresh</button>
            </div>
          </div>

          <div id="telemetryLogBox" style="background: rgba(5, 5, 10, 0.9); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 14px; height: 300px; overflow-y: auto; font-family: var(--font-mono); font-size: 12px; line-height: 1.5;">
            <!-- Dynamic logs -->
          </div>
        </div>
      </section>'''

code = code[:s6_target_start] + new_step6 + code[s6_target_end + len('</section>'):]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('index.html updated successfully with 4K/60FPS/Ultrafast Step 5 and Strict 1-Worker-1-Extension Step 6!')
