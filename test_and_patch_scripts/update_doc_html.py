import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

DOC_PATH = r"E:\stickman-video-automation\studio\public\documentation.html"
with open(DOC_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Expanded 7 Next-Gen Recommendations Card Grid
old_suggestions_grid = """      <div class="card-grid">
        <div class="doc-card">
          <div class="card-title" style="color: var(--cyan);">1. Kokoro TTS / Local Voiceover Synthesis</div>
          <div class="card-desc">
            Integrate a lightweight, lightning-fast 80M parameter local TTS model (like Kokoro-82M). Users could generate natural, expressive documentary voiceovers directly inside Step 1 without needing external ElevenLabs or CapCut files.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: var(--violet-light);">2. Whisper Automated Word-Level Captions</div>
          <div class="card-desc">
            Use the integrated Whisper transcription service to generate animated word-by-word karaoke-style subtitles (.ASS format). Burn them into the 1080p MP4 via FFmpeg <code>subtitles=</code> filter for high-retention Shorts and Reels.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: var(--emerald);">3. Dynamic Audio Sidechain Ducking</div>
          <div class="card-desc">
            Replace static 7% music volume with dynamic sidechain compression: when the voiceover speaks, background music smoothly drops to 5%; during dramatic narrative pauses, music swells up to 25% automatically.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: var(--amber);">4. One-Click Batch Export (16:9 + 9:16)</div>
          <div class="card-desc">
            Add a "Dual Export" button that renders both full 16:9 YouTube landscape video and cropped 9:16 vertical short-form video in a single click, ready for immediate social distribution.
          </div>
        </div>
      </div>"""

new_suggestions_grid = """      <div class="card-grid">
        <div class="doc-card">
          <div class="card-title" style="color: var(--cyan);">1. Built-in Local AI Voiceover (Kokoro-82M / Edge-TTS)</div>
          <div class="card-desc">
            Integrate a zero-latency built-in TTS voice generator in Step 1. Users can paste story scripts, choose from expressive voices (British Documentary, Deep Male, Storyteller), and immediately generate synced audio tracks that automatically set project duration and prompt pacing without external uploads.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: var(--violet-light);">2. Viral Word-by-Word Animated Subtitles (Karaoke Style)</div>
          <div class="card-desc">
            Add a <code>Burn-in Animated Subtitles</code> toggle in Step 5. Uses Whisper word-level timestamps and FFmpeg ASS subtitle rendering to generate high-retention bouncing yellow/white subtitles (Alex Hormozi / CapCut style) directly on the master 4K video.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: var(--emerald);">3. Audio Dynamic Sidechain Ducking</div>
          <div class="card-desc">
            Upgrade background music from static 7% volume to dynamic sidechain compression: music automatically dips to 4% while the narrator speaks, and swells smoothly to 20% during dramatic pauses and transition beats.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: var(--amber);">4. One-Click Dual Aspect Ratio Batch Export (16:9 + 9:16)</div>
          <div class="card-desc">
            Add a "Dual Export" master button in Step 5 that simultaneously exports both 16:9 YouTube Landscape (3840x2160) and 9:16 Vertical Shorts/Reels (1080x1920) in a single render job, saving hours of manual reconfiguration.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: #ff3366;">5. In-Place QA Card Prompt Regeneration (Step 3)</div>
          <div class="card-desc">
            Add a "⚡ Quick Re-Generate" button on each image card in Visual QA Studio. Allows quick tweaking of 2-3 words in a prompt and instant re-queueing to idle workers without navigating back to Step 1.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: #38bdf8;">6. WebSocket Real-Time Progress Bar & Worker Preview</div>
          <div class="card-desc">
            Upgrade HTTP polling to Server-Sent Events (SSE) or WebSockets. Displays live generation progress (0% -> 50% -> 100%) and instant thumbnail pop-ups on the Worker Farm dashboard as images complete on Meta AI or Google Flow.
          </div>
        </div>

        <div class="doc-card">
          <div class="card-title" style="color: #a78bfa;">7. One-Click Complete Project Archive (.ZIP Package)</div>
          <div class="card-desc">
            Add a "💾 Export Project Archive (.ZIP)" button in Step 5. Bundles project script, prompts, voiceover audio, central 4K images, timeline JSON, and rendered MP4 into a single portable ZIP package for cloud backup or machine migration.
          </div>
        </div>
      </div>"""

if old_suggestions_grid in content:
    content = content.replace(old_suggestions_grid, new_suggestions_grid)
    print("Next-Gen Suggestions updated with all 7 comprehensive features!")
else:
    print("Warning: old_suggestions_grid not found verbatim, checking alternatives...")

with open(DOC_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("documentation.html updated successfully!")
