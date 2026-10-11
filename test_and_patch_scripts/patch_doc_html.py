import os
import sys

doc_path = r'E:\stickman-video-automation\studio\public\documentation.html'
with open(doc_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace step5 section
target_step5 = """    <!-- Section 8: Step 5 Master Render -->
    <section id="step5" class="doc-section">
      <div class="section-header">
        <div class="section-num">08</div>
        <h2 class="section-title">Step 5: Post-Production & FFmpeg 1080p Export</h2>
      </div>

      <p style="color: var(--text-muted); margin-bottom: 16px;">
        When you are satisfied with pacing and scene sequence, Step 5 renders the master broadcast video via FFmpeg:
      </p>

      <div class="code-box">
Core FFmpeg Render Command:
ffmpeg.exe -y -f concat -safe 0 -i concat_list.txt -i voiceover.mp3 -i background_music.mp3 \\
  -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps=30[vout];[2:a]volume=0.07,atrim=0:DURATION[music];[1:a][music]amix=inputs=2:duration=first[aout]" \\
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -preset fast -crf 20 -r 30 \\
  -c:a aac -b:a 192k -movflags +faststart output_master_1080p.mp4
      </div>

      <div class="card-grid">
        <div class="doc-card">
          <div class="card-title">Strict 7% Audio Ducking</div>
          <div class="card-desc">Background music is automatically normalized and ducked to exactly 7% (<code>volume=0.07</code>) so the narrator voice is crystal clear and never overpowered.</div>
        </div>

        <div class="doc-card">
          <div class="card-title">Auto Letterboxing & Scaling</div>
          <div class="card-desc">Images with non-standard dimensions are smoothly letterboxed to crisp 1920x1080 (or 1080x1920) with pure black padding, preventing distortion or stretching.</div>
        </div>

        <div class="doc-card">
          <div class="card-title">Post-Render Probing</div>
          <div class="card-desc">Before displaying to user, FFprobe verifies stream codec (H.264), audio codec (AAC), duration parity (>90%), and non-empty byte size.</div>
        </div>
      </div>
    </section>"""

new_step5 = """    <!-- Section 8: Step 5 Master Render & Ultra HD Engine -->
    <section id="step5" class="doc-section">
      <div class="section-header">
        <div class="section-num">08</div>
        <h2 class="section-title">Step 5: Broadcast & Ultra HD 4K / 1080p Export Engine</h2>
      </div>

      <p style="color: var(--text-muted); margin-bottom: 16px;">
        When you are satisfied with pacing, transitions, and effects, Step 5 renders the master broadcast video via an optimized, multi-threaded FFmpeg pipeline:
      </p>

      <div class="code-box">
Ultra HD 4K / 60 FPS Multi-Threaded Command:
ffmpeg.exe -y -f concat -safe 0 -i concat_list.txt -i voiceover.mp3 -i background_music.mp3 \\
  -filter_complex "[0:v]scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2:color=black,fps=60,vignette=PI/4[vout];[2:a]volume=0.07,atrim=0:DURATION[music];[1:a][music]amix=inputs=2:duration=first[aout]" \\
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -preset veryfast -crf 18 -r 60 -threads 0 \\
  -c:a aac -b:a 320k -movflags +faststart output_master_4k.mp4
      </div>

      <div class="card-grid">
        <div class="doc-card">
          <div class="card-title">🌟 4K Ultra HD & 2K Quad HD</div>
          <div class="card-desc">Full support for 3840x2160 (4K Cinema Master), 2560x1440 (2K Quad HD), 1920x1080 (Broadcast Standard), and 2160x3840 / 1080x1920 vertical video for Shorts & Reels.</div>
        </div>

        <div class="doc-card">
          <div class="card-title">⚡ 60 FPS Butter-Smooth Motion</div>
          <div class="card-desc">Defaults to 60 FPS for ultra-smooth Ken Burns pan/zoom and dynamic transitions without stutter, with 30 FPS and 24 FPS quick selectors.</div>
        </div>

        <div class="doc-card">
          <div class="card-title">🚀 Multi-Threaded Speed Acceleration</div>
          <div class="card-desc">Utilizes <code>-threads 0</code> and speed presets (<code>ultrafast</code> for 5x export speed, <code>veryfast</code> for balanced master quality) to minimize rendering time.</div>
        </div>

        <div class="doc-card">
          <div class="card-title">💎 Lossless CRF & 320k Audio</div>
          <div class="card-desc">CRF 18 for pristine 4K clarity, CRF 20 for broadcast master, and uncompressed 320 kbps AAC audio with strict 7% background music ducking.</div>
        </div>

        <div class="doc-card">
          <div class="card-title">🎨 Baked-In Atmospheric Effects</div>
          <div class="card-desc">All selected atmospheric looks (Cyberpunk, Noir, Vintage, Moody Dark, Warm, Cool), vignettes, blur, and sharpening are baked directly into the MP4 video stream.</div>
        </div>

        <div class="doc-card">
          <div class="card-title">📂 In-Page Player & Direct Open</div>
          <div class="card-desc">Instant HTML5 video playback in the studio plus <code>📂 Open Output Folder</code> button to open the renders directory directly in Windows Explorer.</div>
        </div>
      </div>
    </section>"""

if target_step5 in html:
    html = html.replace(target_step5, new_step5)
    print('Updated step5 in documentation.html')
else:
    print('Warning: target_step5 not found directly')

# Replace step6 section
target_step6 = """    <!-- Section 9: Step 6 Telemetry & API -->
    <section id="step6" class="doc-section">
      <div class="section-header">
        <div class="section-num">09</div>
        <h2 class="section-title">Step 6: Telemetry, Reconcile & REST API Reference</h2>
      </div>"""

new_step6 = """    <!-- Section 9: Step 6 Settings, API Keys Vault & 10-Worker Login Assistant -->
    <section id="step6" class="doc-section">
      <div class="section-header">
        <div class="section-num">09</div>
        <h2 class="section-title">Step 6: Settings, API Keys Vault & 10-Worker Login Assistant</h2>
      </div>

      <div class="card-grid" style="margin-bottom: 20px;">
        <div class="doc-card">
          <div class="card-title">🔑 10-Worker One-Time Login Assistant</div>
          <div class="card-desc">
            Launches dedicated Chrome windows for workers W01–W10 with <strong>both Meta.ai and Flow tabs opened</strong>. Log in once by hand; Chrome permanently saves cookies in <code>Workers/Worker-Wnn</code>.
            Automatic cleanup of stale lockfiles (<code>SingletonLock</code>) prevents startup errors.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title">⚡ Multi-Provider Cloud API Vault</div>
          <div class="card-desc">
            Centralized settings for Groq Cloud API (with 3–5 key rotation pool and live latency test), ElevenLabs AI voiceover key, OpenAI Whisper key, and Fal.ai / Stability fallback keys.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title">📄 Human-Readable Text Logs</div>
          <div class="card-desc">
            All system operations, worker lifecycle events, and render outputs are logged to <code>studio/logs/studio.log</code> and <code>studio/logs/studio_errors.log</code> for instant inspection and debugging.
          </div>
        </div>
      </div>"""

if target_step6 in html:
    html = html.replace(target_step6, new_step6)
    print('Updated step6 in documentation.html')
else:
    print('Warning: target_step6 not found directly')

with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully patched documentation.html')
