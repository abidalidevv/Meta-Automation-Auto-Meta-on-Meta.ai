import os
import sys

index_path = r'E:\stickman-video-automation\studio\public\index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<!-- ==================== STEP 5: STUDIO RENDER ==================== -->'
end_marker = '<!-- ==================== MODALS ==================== -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Error: Could not locate step 5 and step 6 boundaries')
    sys.exit(1)

new_step5_and_step6 = """<!-- ==================== STEP 5: STUDIO RENDER & ULTRA HD EXPORT ==================== -->
      <section id="step-5-panel" class="view-panel">
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
              <span class="brand-badge" style="background: rgba(16, 185, 129, 0.15); color: var(--emerald);">60 FPS Ready</span>
            </div>

            <!-- Resolution Selector -->
            <div class="form-group">
              <label class="form-label" style="display: flex; justify-content: space-between;">
                <span>Video Format & Resolution</span>
                <span id="resBadge" style="color: var(--cyan); font-weight: 700;">1080p Full HD</span>
              </label>
              <select id="renderResolution" class="form-select" onchange="onRenderResolutionChange(this.value)">
                <option value="3840x2160">🌟 3840x2160 (16:9 - 4K Ultra HD Master - YouTube 4K Quality)</option>
                <option value="2560x1440">💎 2560x1440 (16:9 - 2K Quad HD / 1440p High-Res)</option>
                <option value="1920x1080" selected>🎬 1920x1080 (16:9 - 1080p Full HD Broadcast Standard)</option>
                <option value="2160x3840">📱 2160x3840 (9:16 - 4K Ultra HD Vertical Shorts / Reels Ultra)</option>
                <option value="1080x1920">📱 1080x1920 (9:16 - 1080p Vertical Shorts / TikTok / Reels)</option>
              </select>
            </div>

            <!-- Frame Rate (FPS) and Speed Preset -->
            <div class="grid-2">
              <div class="form-group">
                <label class="form-label" style="display: flex; justify-content: space-between;">
                  <span>Frame Rate (FPS)</span>
                  <span style="color: var(--emerald); font-weight: 700;">60 FPS (Default)</span>
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
                  <option value="ultrafast">⚡ ultrafast (Lightning Fast Export — 5x Speed)</option>
                  <option value="superfast">🚀 superfast (Ultra-Fast Render)</option>
                  <option value="veryfast" selected>⚡ veryfast (Fast & Balanced — High Quality)</option>
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
                  <option value="18">🌟 Ultra HD Lossless (CRF 18 — High Bitrate)</option>
                  <option value="20" selected>🎬 Broadcast Master (CRF 20 — Standard)</option>
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
              <span>🎬</span> Export Ultra HD / 1080p MP4 Video
            </button>

            <!-- Render Status Box -->
            <div id="renderStatusCard" style="display: none; margin-top: 18px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: var(--radius-sm); padding: 16px;">
              <div style="height: 8px; background: rgba(255,255,255,0.08); border-radius: 4px; overflow: hidden; margin-bottom: 10px;">
                <div id="renderBar" style="width: 0%; height: 100%; background: var(--grad-brand); transition: width 0.4s ease;"></div>
              </div>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div id="renderProgressText" style="font-size: 13px; font-family: var(--font-mono); color: var(--cyan);">Encoding MP4 via FFmpeg...</div>
                <div id="renderProgressPct" style="font-size: 12px; color: #fff; font-weight: 700;">0%</div>
              </div>

              <!-- Completion Action Buttons (Hidden until render done) -->
              <div id="renderCompletionActions" style="display: none; margin-top: 14px; gap: 10px; flex-wrap: wrap;">
                <a id="btnDownloadRender" href="#" download class="btn btn-emerald" style="text-decoration: none; padding: 8px 14px; font-size: 12px;">
                  ⬇ Download MP4
                </a>
                <button type="button" class="btn btn-secondary" onclick="openOutputFolder('renders')" style="font-size: 12px; padding: 8px 14px;">
                  📂 Open Output Folder
                </button>
              </div>
            </div>
          </div>

          <!-- Video Playback & Render History Card -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">📺</div>
                <div>
                  <div class="card-title">Completed Master Video & History</div>
                  <div class="card-subtitle">Instant playback of rendered MP4 and export archive</div>
                </div>
              </div>
              <button class="btn btn-secondary" onclick="loadRenderHistory()" style="font-size: 11.5px; padding: 4px 10px;">Refresh</button>
            </div>

            <!-- In-Page Master Player -->
            <div style="background: #000; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); overflow: hidden; margin-bottom: 14px; display: flex; align-items: center; justify-content: center; min-height: 220px;">
              <video id="step5MasterPlayer" controls style="width: 100%; max-height: 280px; display: none;"></video>
              <div id="step5PlayerPlaceholder" style="color: var(--text-dim); text-align: center; padding: 30px; font-size: 12.5px;">
                <div style="font-size: 30px; margin-bottom: 8px;">🎬</div>
                <div>Rendered video will appear here for instant playback.</div>
              </div>
            </div>

            <div style="font-size: 12px; font-weight: 700; color: #fff; margin-bottom: 8px;">Project Export Archive</div>
            <div id="renderHistoryList" style="max-height: 220px; overflow-y: auto; display: flex; flex-direction: column; gap: 6px;">
              <!-- Dynamic renders loaded via JS -->
            </div>
          </div>

        </div>
      </section>

      <!-- ==================== STEP 6: SETTINGS, API KEYS & 10-WORKER LOGIN ASSISTANT ==================== -->
      <section id="step-6-panel" class="view-panel">
        <div class="grid-2">
          
          <!-- Card 1: Multi-Provider AI API Keys Vault -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">⚡</div>
                <div>
                  <div class="card-title">AI Engine & Cloud API Keys Vault</div>
                  <div class="card-subtitle">Configure Groq, ElevenLabs, OpenAI, and Image Generation APIs</div>
                </div>
              </div>
            </div>

            <!-- 1. Groq Cloud API -->
            <div style="background: rgba(0, 240, 255, 0.04); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label class="form-label" style="margin-bottom: 0; font-weight: 800; color: #fff;">
                  ⚡ Groq AI Primary Key
                </label>
                <a href="https://console.groq.com/keys" target="_blank" style="font-size: 11px; color: var(--cyan); text-decoration: none;">Get Free Key &rarr;</a>
              </div>
              <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                <input type="password" id="settingsGroqKeySingle" class="form-input" placeholder="gsk_..." style="font-family: var(--font-mono); font-size: 12px;" />
                <button type="button" class="btn btn-secondary" onclick="togglePasswordVisibility('settingsGroqKeySingle')" style="padding: 0 10px;">👁</button>
                <button type="button" class="btn btn-secondary" onclick="testGroqKeyConnection()" style="font-size: 11px; padding: 0 12px; white-space: nowrap;">⚡ Test Key</button>
              </div>

              <!-- Groq Multi-Key Pool (Rotator) -->
              <label class="form-label" style="font-size: 11px; display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span>Groq Key Rotation Pool (3–5 Keys, 1 per line)</span>
                <span id="keyPoolCountLabel" style="color: var(--cyan); font-weight: 700;">1 Key Loaded</span>
              </label>
              <textarea id="settingsGroqKeyPool" class="form-textarea" placeholder="gsk_key1...&#10;gsk_key2...&#10;gsk_key3..." style="font-family: var(--font-mono); font-size: 11.5px; min-height: 60px;"></textarea>

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
                  🎙️ ElevenLabs API Key (Optional Realistic Voiceover)
                </label>
                <a href="https://elevenlabs.io/app/voice-library" target="_blank" style="font-size: 11px; color: var(--violet); text-decoration: none;">elevenlabs.io &rarr;</a>
              </div>
              <input type="password" id="settingsElevenLabsKey" class="form-input" placeholder="Optional ElevenLabs API key..." style="font-family: var(--font-mono); font-size: 12px;" />
            </div>

            <!-- 3. OpenAI & Image Fallback Keys -->
            <div style="background: rgba(16, 185, 129, 0.04); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 12px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <label class="form-label" style="margin-bottom: 0; font-weight: 800; color: #fff;">
                  🤖 OpenAI / Whisper API Key (Optional)
                </label>
                <a href="https://platform.openai.com/api-keys" target="_blank" style="font-size: 11px; color: var(--emerald); text-decoration: none;">openai.com &rarr;</a>
              </div>
              <input type="password" id="settingsOpenAIKey" class="form-input" placeholder="sk-..." style="font-family: var(--font-mono); font-size: 12px;" />
            </div>

            <div style="display: flex; gap: 10px; margin-top: 14px;">
              <button class="btn btn-primary" onclick="saveAllSettings()" style="flex: 1; justify-content: center; padding: 12px; font-weight: 800;">
                💾 Save All Settings & Keys
              </button>
              <button class="btn btn-secondary" onclick="triggerReconciliation()" style="padding: 12px 16px;">
                Reconcile Storage
              </button>
            </div>
          </div>

          <!-- Card 2: 10-Worker One-Time Login Assistant (Upgraded) -->
          <div class="card">
            <div class="card-header">
              <div class="card-title-group">
                <div class="card-icon">🔑</div>
                <div>
                  <div class="card-title">10-Worker One-Time Login Assistant</div>
                  <div class="card-subtitle">Permanent cookie sessions for workers W01–W10 on Meta.ai & Flow</div>
                </div>
              </div>
              <button class="btn btn-secondary" onclick="stopAllWorkers()" style="font-size: 11px; padding: 4px 10px; color: #f87171; border-color: rgba(248, 113, 113, 0.3);">
                🛑 Stop All Workers
              </button>
            </div>

            <div style="background: rgba(0, 240, 255, 0.04); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: var(--radius-sm); padding: 12px; margin-bottom: 14px; font-size: 12px; color: var(--text-muted); line-height: 1.5;">
              <strong style="color: #fff;">How it works:</strong> Click the button below to launch Chrome worker windows with 
              <span style="color: var(--cyan); font-weight: 700;">Meta.ai</span> and 
              <span style="color: var(--violet); font-weight: 700;">Flow</span> tabs opened automatically. 
              Log in once by hand in each window. Chrome permanently persists authentication in <code style="color: #fff;">Workers/Worker-Wnn</code>, allowing the 10-worker cluster to generate images non-stop without re-logging!
            </div>

            <!-- Master Launch Button -->
            <button class="btn btn-primary" onclick="openWorkerLogin('ALL')" style="width: 100%; justify-content: center; padding: 13px; font-size: 14px; font-weight: 800; margin-bottom: 14px; background: linear-gradient(135deg, #00f0ff, #8b5cf6);">
              🚀 Launch All 10 Worker Profiles for One-Time Login
            </button>

            <!-- Individual Launch Grid (W01 to W10) -->
            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px; display: flex; justify-content: space-between;">
              <span>Or Launch Individual Worker Profile:</span>
              <span style="color: var(--cyan);">Dual-Tab (Meta + Flow)</span>
            </div>

            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin-bottom: 14px;">
              <button class="btn btn-secondary" onclick="openWorkerLogin('W01')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W01</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W02')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W02</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W03')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W03</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W04')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W04</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W05')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W05</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W06')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W06</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W07')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W07</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W08')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W08</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W09')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W09</button>
              <button class="btn btn-secondary" onclick="openWorkerLogin('W10')" style="font-size: 11.5px; padding: 8px 0; justify-content: center; font-weight: 700;">W10</button>
            </div>

            <!-- Quick Directory Shortcuts -->
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <button class="btn btn-secondary" onclick="openOutputFolder('workers')" style="font-size: 11px; padding: 6px 10px; flex: 1; justify-content: center;">
                📁 Open Workers Profiles Folder
              </button>
              <button class="btn btn-secondary" onclick="openOutputFolder('logs')" style="font-size: 11px; padding: 6px 10px; flex: 1; justify-content: center;">
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
      </section>

      """

new_html = html[:start_idx] + new_step5_and_step6 + html[end_idx:]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Successfully patched Step 5 and Step 6 in index.html!')
