manual_md = """# 🎬 Stickman Studio V2 — Master Engineering & Workflow Manual
> **Ultra HD 4K / 1080p Video Production Engine • 10-Worker Browser Cluster (Meta.ai & Flow) • Professional CapCut Multi-Track Timeline • 5-Tab Tools & Assets Studio Suite**

---

## 📌 Executive Summary & Architecture Overview

Stickman Studio V2 is an automated local desktop video production studio designed for Windows. It orchestrates a 10-worker browser farm (alternating between **Meta.ai** and **Google Flow / ImageFX**) to generate consistent character scenes, validate incoming media assets, synchronize slides to voiceover audio with sub-second pacing, apply professional Adobe Premiere / After Effects visual looks and captions, and export broadcast-ready **4K Ultra HD** or **1080p Full HD MP4 videos at 60 FPS** via an optimized, multi-threaded FFmpeg engine.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                STICKMAN STUDIO V2 PIPELINE                             │
├─────────────────┬─────────────────┬──────────────────┬─────────────────┬───────────────┤
│ STEP 1          │ STEP 2          │ STEP 3           │ STEP 4          │ STEP 5 & 6    │
│ Prompt Importer │ 10-Worker Farm  │ Media Assets &   │ CapCut Timeline │ 4K/60FPS MP4  │
│ & Groq Story    │ Batch Scheduler │ Visual QA Vault  │ & Tools Suite   │ Export & Auth │
└─────────────────┴─────────────────┴──────────────────┴─────────────────┴───────────────┘
```

---

## 🚀 Step-by-Step Complete Operational Guide

### 📝 Step 1: Script & Prompt Engineering
Stickman Studio V2 provides two distinct operational modes and a dedicated queue manager:

1. **Mode 1: Clean Prompt List Importer (Default Active)**
   * **Purpose:** Paste or upload an existing raw prompt list generated externally or from custom prompts.
   * **Clean Parser:** Automatically strips markdown noise, quotation marks, numbered prefixes (`Prompt 01:`, `1.`, `001-`), and extracts clean prompt descriptions ready for workers.
   * **Direct Import:** Automatically parses, counts, and imports all prompts into the project database.
2. **Mode 2: Groq AI Story Engine**
   * **Purpose:** Transform raw story text or voiceover scripts into sequential scene prompts.
   * **Voiceover File Picker:** Upload an `.mp3` or `.wav` file; audio duration is automatically scanned and detected in seconds.
   * **Auto-Pacing Calculator:** Calculates the exact prompt count required based on user-selected pacing (`1/4s` = 4.0s/img, `2/4s` = 2.0s/img, `3/4s` = 1.33s/img, `4/4s` = 1.0s/img, `5/4s` = 0.8s/img).
   * **Character Consistency Image Picker:** Upload a stickman or character reference image (`.png` / `.jpg`) to lock character visual attributes across all scene prompts.
3. **Sub-Tab 3: Project Prompts Queue**
   * Real-time counter of total prompts in queue.
   * **Queue Actions:**
     * `↻ Retry Failed Prompts`: Resets all `FAILED` prompts back to `QUEUED` / `PENDING` so workers can immediately re-attempt generation.
     * `✕ Clear Failed Prompts`: Deletes failed prompts and dead jobs from the queue.
     * `🗑️ Clear All Prompts`: Clears the active project's prompt queue.

---

### 🚜 Step 2: 10-Worker Chrome Farm Fleet & Batch Scheduler
* **10 Dedicated Chrome Workers (W01 to W10):**
  * Odd workers (`W01`, `W03`, `W05`, `W07`, `W09`) run on **Meta.ai**.
  * Even workers (`W02`, `W04`, `W06`, `W08`, `W10`) run on **Google Flow / ImageFX**.
  * Each worker has an isolated, persistent user data profile in `Workers/Worker-W01` through `Worker-W10`.
* **Dynamic Fleet Calculator & Scheduler:**
  * Displays total prompts in queue, needed workers, Meta worker count, and Flow worker count.
  * Uses the batch scheduling formula:
    $$\text{Batches} = \left\lceil \frac{N}{10} \right\rceil$$
  * Distributes jobs across all 10 workers evenly with lease tracking and auto-recovery of stale leases.

---

### 🎨 Step 3: Media Assets & Visual QA Studio
* **What Media is Shown?**
  * Displays all rendered images generated and downloaded by the 10 Chrome workers for the current project.
  * Each card displays the **Prompt ID** (`001`, `002`...), **Worker ID** (`W01`..`W10`), and **QA Integrity Score**.
* **Button Functions:**
  1. `Reconcile Storage`: Audits physical files on disk (`central_images`) against the SQLite database, repairs prompt records, detects 0-byte corrupt files, and recovers orphan assets.
  2. `🔄 Scan & Ingest Assets`: Triggers the ingestion engine to scan worker download folders, validates binary PNG/JPEG magic bytes, transfers images to `central_images`, and refreshes the gallery.
* **Sequence Guarantee:**
  * Queries `SELECT * FROM prompts WHERE project_id = ? ORDER BY prompt_index ASC`.
  * Images are **strictly and automatically ordered prompt-wise and story-wise (001, 002, 003... NNN)**.

---

### 🎬 Step 4: CapCut Multi-Track Timeline & "TOOLS & ASSETS" Professional Editor Suite

#### A. CapCut Multi-Track Timeline & Interactive Player
* **Strict Prompt Sequencing:** Scenes are ordered `#01` to `#NN` matching the prompt list.
* **Pacing & Duration Badges:** Each scene displays its calculated duration (e.g. `1.33s`).
* **Duration Micro-Adjusters:** Click `+` or `-` buttons to extend or shorten individual scene durations by 0.25s.
* **Drag-and-Drop Reordering:** Drag scene cards left or right to reorder sequence visually.
* **Check for Missing Images:** Highlights missing assets with warning alerts and provides 1-click re-queueing.

#### B. Right-Side "TOOLS & ASSETS" 5-Tab Post-Production Suite
Modeled after Adobe Premiere Pro & After Effects with real-time video canvas preview:

1. **Tab 1: `✨ Effects` (Atmospheric Effects 20 & Pro Controls):**
   * **20 Atmospheric Effects Cards Grid:**
     `Normal`, `Bright`, `Moody Dark`, `Warm`, `Cool`, `Vintage`, `B&W`, `Vivid`, `Dreamy`, `Neon`, `Golden Hour`, `Cyberpunk`, `Noir`, `Sepia`, `Invert`, `Pastel`, `Frost`, `Sunset`, `Ocean`, `Chromatic`.
   * **Live Premiere & After Effects Controls:**
     * Gaussian Blur (`0px` to `15px`)
     * Lumetri Exposure (`-50%` to `+50%`)
     * Lumetri Contrast (`50%` to `180%`)
     * Lumetri Saturation (`0%` to `220%`)
     * Vignette (Live toggle + cinematic radial shadow overlay on canvas)
     * Film Grain / Noise
     * Sharpen / Unsharp Mask
     * CC Glow / Bloom
     * `↺ Reset Look` (1-click return to clean defaults)
2. **Tab 2: `💬 Captions` (Dynamic Captions & 18 Viral Templates):**
   * 18 Viral creator templates: Yellow Highlight, Hormozi, MrBeast, Vox, Alex, Cyan, Cinematic Bronze, etc.
   * Placement presets: Left, Right, Bottom, Center.
   * Font Size presets: Medium (95px), Large (125px), Huge (145px), Extra Huge (160px), Custom Slider.
   * Font Family Override (12 creator fonts).
   * Caption Background Box with opacity and color customization.
3. **Tab 3: `⚡ Motion & Transitions`:**
   * **8 Premiere Pro Transitions:** `Cross Dissolve`, `Dip to Black`, `Dip to White`, `Film Dissolve`, `Morph Cut`, `Zoom / Transform`, `Push Transition`, `Whip / Blur`.
   * **8 After Effects Camera Movements:** `Camera Push-In`, `Camera Pull-Out`, `Pan Left -> Right`, `Pan Right -> Left`, `2.5D Parallax`, `3D Camera Move`, `Whip & Shake`, `Easy Ease`.
   * Live animation immediately previews on the canvas player!
4. **Tab 4: `🔊 Audio & Sound Effects (SFX)`:**
   * **35+ Categorized Soundboard:**
     * *Whooshes & Swishes (8):* Whoosh, Fast Whoosh, Short Whoosh, Whoosh Transition, Swish, Fast Swish, Air Whoosh, Reverse Whoosh.
     * *Impacts & Hits (8):* Cinematic Impact, Deep Impact, Bass Impact, Trailer Hit, Cinematic Hit, Boom Hit, Low Boom, Sub Boom.
     * *Build-up & Risers (5):* Cinematic Riser, Whoosh Riser, Tension Riser, Reverse Riser, Impact Riser.
     * *Documentary & Ambience (6):* Dark Ambience, Cinematic Ambience, Wind Ambience, Rain Ambience, Crowd Ambience, Room Tone.
     * *UI & Graphic Micro Sounds (6):* Click, Tick, Pop, Digital Click, Camera Shutter, Glitch Hit.
   * **Zero-Dependency Web Audio API Synthesizer:** Instant auditioning (clicking ▶ plays the sound live through speakers without missing asset errors).
   * **`+ Scene` Button:** Binds chosen SFX directly to the active scene in the timeline.
   * **Ducked Background Music Slider:** Standard 7% ducking slider with live readout.
5. **Tab 5: `📁 Media Inspector`:**
   * Active scene details (`Scene #01`, `Prompt 001`, `1024x1024`, `1.33s`).
   * Scene prompt description block.
   * `Replace Image` file picker to update slide images on the fly.

---

### 🚀 Step 5: Broadcast & Ultra HD 4K / 1080p Export Engine
* **Video Format & Resolution Options:**
  * `3840x2160` — **4K Ultra HD (16:9 Cinema / YouTube 4K Master)**
  * `2560x1440` — **2K Quad HD (16:9 High-Res / 1440p)**
  * `1920x1080` — **1080p Full HD (16:9 Broadcast Standard - Default)**
  * `2160x3840` — **4K Ultra HD Vertical (9:16 Shorts / Reels Ultra)**
  * `1080x1920` — **1080p Vertical (9:16 Shorts / Reels / TikTok)**
* **Frame Rate (FPS):** Default **60 FPS** for butter-smooth Ken Burns motion, with 30 FPS and 24 FPS quick-select buttons.
* **Speed & Hardware Acceleration:**
  * Speed presets: `ultrafast` (5x speed), `superfast`, `veryfast` (default), `fast`, `medium`.
  * Multi-Core CPU acceleration (`-threads 0`) unlocks all processor cores for rapid rendering.
* **Visual Fidelity & Audio Bitrate:**
  * CRF 18 (Ultra HD Lossless) / CRF 20 (Broadcast Master).
  * 320 kbps AAC Studio Master audio bitrate.
* **Baked-In Effects Guarantee:**
  * All selected atmospheric visual looks, vignettes, blur, sharpen, and transitions are translated into FFmpeg video filters (`eq`, `hue`, `colorchannelmixer`, `vignette=PI/4`, `unsharp`) and baked into the exported MP4!
* **Direct Actions:**
  * In-page video player to watch the rendered 4K/1080p MP4 immediately.
  * Direct `⬇ Download MP4` button.
  * `📂 Open Output Folder` button (pops open Windows Explorer directly to the renders directory).

---

### ⚙️ Step 6: Settings, API Keys Vault & 10-Worker Login Assistant
1. **AI Cloud API Keys Vault:**
   * **Groq Cloud API Key:** Input with show/hide password toggle, multi-key rotation pool (3–5 keys), and live `⚡ Test Key` connection validator.
   * **ElevenLabs API Key:** For realistic AI voice generation.
   * **OpenAI API Key:** For Whisper transcription and fallback LLM.
   * **Fal.ai / Stability AI Key:** For image generation fallback.
   * `💾 Save All Settings & Keys` button with persistent database storage.
2. **10-Worker One-Time Login Assistant (Rock-Solid):**
   * **Master Launch Button:** `🚀 Launch All 10 Worker Profiles for One-Time Login` launches Chrome windows with **both Meta.ai and Flow tabs opened** with a smooth 1.2s stagger.
   * **Individual Worker Launch Grid:** 10 individual buttons (`W01` to `W10`) to open specific worker profiles.
   * **Lockfile & Zombie Process Auto-Cleaner:** Automatically terminates hanging Chrome crashpad/gpu sub-processes and deletes stale `lockfile` / `SingletonLock` so Chrome never fails to launch or exits with code 21.
   * **Permanent Session Persistence:** Cookies and login tokens are permanently preserved in `Workers/Worker-W01` through `Worker-W10`.
   * **`🛑 Stop All Workers` Button:** 1-click shutdown of all running worker browser windows.
3. **Live System Telemetry & Plain-Text File Logging:**
   * Real-time live telemetry stream in UI.
   * Writes human-readable plain-text logs to `studio/logs/studio.log` and `studio/logs/studio_errors.log`.
   * `📄 View studio.log` button (opens raw log file in browser tab).
   * `📂 Open Studio Logs Folder` button (opens logs folder in Windows Explorer).

---

## 🛠️ Verification & System Health
* **Server Health:** Active on `http://127.0.0.1:45450/api/v1/health`
* **Syntax Validation:** All files (`routes.js`, `render_engine.js`, `profile_manager.js`, `logger.js`, `app_v2.js`) checked with `node -c` (0 errors).
* **Database:** SQLite `studio.sqlite` active with migrations and 10 workers seeded.
"""

paths = [
    r'c:\Users\Ali\Desktop\meta automation\STUDIO_V2_COMPLETE_MANUAL.md',
    r'E:\stickman-video-automation\STUDIO_V2_COMPLETE_MANUAL.md'
]

for p in paths:
    with open(p, 'w', encoding='utf-8') as f:
        f.write(manual_md)
    print(f'Successfully wrote manual to {p}')
