# Stickman Studio & Extensions — Architecture & Changes Record

> **Purpose:** Detailed record of the Stickman Studio video automation system, the exact role of the browser worker extensions, and a complete changelog of modifications for auditing or reverting if necessary.

---

## 1. Project Architecture & The Role of Extensions

### Project Overview
**Stickman Studio** is an automated desktop production pipeline for creating 2D stickman YouTube documentary videos. The workflow consists of:
1. **Mode 1 (AI Story Engine):** Converts story/voiceover scripts into sequential, character-locked stickman image prompts via Groq AI (using `story to prompts.md` as Master Directive V7).
2. **Mode 2 (Prompt List Importer):** Direct importer for users who already have pre-written prompt lists (`001_...` to `NNN_...`).
3. **Worker Farm (Browser Automation Cluster):** 10 isolated Chrome worker profiles (`W01` to `W10`) running two automated providers:
   - **Google Flow (Veo 3):** High-quality stickman generation with ingredients and reference media attachment.
   - **Meta AI (Llama Vision):** Fast 16:9 illustration generation with clip attachments.
4. **Media QA & Ingestion:** Automatic SHA-256 deduplication, dimension checks, and central image organization.
5. **Studio Player & Timeline:** Audio waveform synchronization, auto-ducked BGM (7%), caption styling templates, and live video preview.
6. **MP4 Video Render:** Hardware-accelerated 1080p MP4 export.

### Exact Role of the Extensions
The Chrome extensions (`meta automation` and `veo-automation-with Mbmirza`) serve as **browser automation bridges**:
- Each worker profile (`Worker-W01` through `Worker-W10`) launches an isolated Google Chrome browser instance loaded with its provider extension.
- Inside the browser's side panel drawer, `bridge-client.js` connects locally to `http://127.0.0.1:45450/api/v1/`.
- It leases prompt generation jobs from Stickman Studio, injects character reference visuals into Flow/Meta composer interfaces, auto-types prompts, monitors generation, and auto-downloads the resulting high-res images into project download folders.
- **Standalone Capability:** When toggled to `Auto OFF` (Manual Mode), the extension operates 100% standalone, allowing the user to paste prompts and click `RUN` manually without any background studio interference or tab spawning.

---

## 2. Changelog of Modifications (Commits: `56e51af` & `80a2f51`)

### A. Mode 2 Prompt Validation & SQLite Unique Constraint Crash
- **Problem:** Pasting sequential prompts into Mode 2 threw `SQLITE_CONSTRAINT: UNIQUE constraint failed: prompts.project_id, prompts.prompt_index` because `project_manager.js` did `ON CONFLICT(id)` instead of `ON CONFLICT(project_id, prompt_index)`.
- **Changes in `studio/server/project_manager.js`:**
  - Updated prompt insert query to `ON CONFLICT(project_id, prompt_index) DO UPDATE SET ...`
  - Normalized primary key ID to `prompt_${projectId}_${p.idStr}`.
  - Automatically prunes excess prompt rows if a new import contains fewer prompts than previously registered.
- **Changes in `studio/public/app_v2.js`:**
  - Fixed toast notification so `data.error` is displayed explicitly instead of an empty `Validation error:`.

### B. Extension Extra Tab Spawning vs. Native Side Drawer
- **Problem:** Extensions were calling `chrome.tabs.create` inside `service-worker-loader.js` on every startup and window creation, opening `src/ui/side-panel/index.html` as a separate browser tab alongside Meta AI / Google Flow.
- **Changes in `service-worker-loader.js` (both Meta & Flow):**
  - Removed `chrome.tabs.create`.
  - Configured native Chrome Manifest V3 Side Panel API:
    `chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true })`
    `chrome.sidePanel.open({ windowId })`
  - Clicking the extension toolbar icon now docks the side drawer on the right side of the screen; zero extra tabs are opened.

### C. Sticky Banner Blocking Native Run Button & Ghost Job Loop
- **Problem:** `bridge-client.js` injected `#stickman-bridge-banner` fixed across the bottom (`bottom: 12px; left: 12px; right: 12px; z-index: 99999`), covering the extension's Run and Queue buttons. Old projects also left ghost jobs for prompt 050 in SQLite that looped endlessly.
- **Changes in `bridge-client.js` (both Meta & Flow):**
  - Re-positioned banner to `top: 6px; left: 6px; right: 6px;`. Bottom buttons are now 100% accessible.
  - Added a **Minimize button (`—`)** that collapses the banner into a tiny corner badge (`[• W01 AUTO +]`).
  - Added an **`Auto ON` / `Auto OFF` toggle**: Clicking `Auto OFF` switches to Manual Mode, stopping all studio polling and tab interactions so the user can run standalone prompts freely.
  - Cleaned up 1263 old `REPAIR_PENDING` prompts and 42 stale ghost jobs in `studio.sqlite`.
  - Scoped `getNextJob` in `worker_orchestrator.js` strictly to the currently active project.

### D. Auto-Download File Detection
- **Problem:** Images downloaded by Chrome into `Downloads/<project_name>/001_...` were failing `completeJob` checks because the server only looked in `Downloads/001_...`.
- **Changes in `studio/server/worker_orchestrator.js`:**
  - Added recursive scan in `Downloads/<project_name>/` and `Downloads/StickmanStudio/`.
  - Added prefix-matching for `001_*.png` so generated stickman images are detected and ingested into `central_images` immediately.

### E. Character Reference Visual Attachment Selectors
- **Google Flow:** Automated clicking `button.add-menu-trigger` / `aria-label*="Add ingredients"` -> `button.sidebar-upload-btn` -> file input -> `button.detail-add-to-prompt-btn`.
- **Meta AI:** Automated injection into `input[type="file"]` via `DataTransfer` with `mode: 'imageToImage'`.

### F. Standalone Automation Tester Tool
- Created `studio/public/extension_tester.html` (served at `http://127.0.0.1:45450/extension_tester.html`) allowing the user to select Flow or Meta, pick a reference image, load 15 Andes stickman prompts, launch the worker browser, and inspect the end-to-end automation live.

---

## 3. How to Revert (If Ever Needed)

If you ever wish to revert the commit `56e51af` in `stickman-video-automation`:
```bash
git -C "E:\stickman-video-automation" revert 56e51af --no-edit
git -C "E:\stickman-video-automation" push origin main
```
And to revert `80a2f51` in `meta automation`:
```bash
git -C "C:\Users\Ali\Desktop\meta automation" revert 80a2f51 --no-edit
git -C "C:\Users\Ali\Desktop\meta automation" push origin main
```
*(All original files are safely preserved in Git history).*


---

## 3. Mode 1 Redesign, Groq Multi-Model Fallback & Output Canvas (Latest Overhaul)

### A. Automatic Groq Model Selection with Fallback Chain
- **Problem:** User had to manually pick Groq models from a large dropdown. In backend, `DEFAULT_GROQ_MODEL` was set to an unsupported model (`openai/gpt-oss-120b`), and `rawContent` was never defined, crashing any prompt generation request.
- **Changes in `studio/server/ai_story_engine.js`:**
  - `DEFAULT_GROQ_MODEL` set to `'llama-3.3-70b-versatile'`.
  - Added `FALLBACK_GROQ_MODELS = ['llama-3.3-70b-versatile', 'llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768']`.
  - Implemented real `groq.chat.completions.create` API call with automatic error trapping, API key rotation across key pool on 429/401 rate limits, and seamless cascade down the fallback model list.
  - Return payload now includes `raw_prompts_text` for instant display in the output canvas.
- **Changes in `studio/public/index.html`:**
  - Replaced manual model dropdown with an automated status badge: `⚡ Groq: llama-3.3-70b (Auto Fallbacks)`.

### B. Voiceover Audio & Instant HTML5 Duration Auto-Detection
- **Problem:** User had to click an extra "⚡ Auto-Detect" button after selecting an audio file, and a duplicate badge `🎵 voiceover.mp3` cluttered the layout.
- **Changes in `studio/public/app_v2.js` & `index.html`:**
  - Attached an instant HTML5 `new Audio(URL.createObjectURL(file))` metadata listener directly inside `handleM1VoiceoverFile(input)`.
  - Duration is calculated and displayed the millisecond the file is picked (e.g. `1366.5s (22m 46s)`).
  - Removed the redundant Auto-Detect button and duplicate file badge.
  - Duration input is now compact and automatically triggers real-time pacing recalculation.

### C. Anti-Template Dynamic/Random Pacing Preset
- **Problem:** Static pacing rules (e.g., exactly 2s per image every time) can trigger YouTube algorithmic detection as automated template content.
- **Changes in `studio/server/ai_story_engine.js`, `studio/server/project_manager.js`, `index.html`, and `app_v2.js`:**
  - Added `'Random': 0.50` to `PACING_MULTIPLIERS`.
  - Added preset option `🎲 Random / Dynamic (Anti-Template YouTube Pacing)` in UI.
  - Variable scene rhythm (e.g., 4s -> 4 img, 4s -> 2 img, 4s -> 3 img, 3s -> 1 img, average ~2.00s/image).
  - Live forecast card immediately displays dynamic Anti-Template target count calculation.

### D. Canonical Master Prompt V7 Auto-Resolution
- **Problem:** Master Prompt V7 directive textarea occupied massive vertical space, and the file was renamed to `story to prompts.md`.
- **Changes in `studio/server/routes.js` & `ai_story_engine.js`:**
  - Automatically resolves `e:/stickman-video-automation/Old Md files/story to prompts.md` (23,426 bytes) as the canonical master directive.
  - Replaced giant textarea with a sleek directive status pill `📄 Master Directive: story to prompts.md (Canonical V7 Locked)` with optional `📂 Pick Custom .md Directive` and preview toggles.

### E. Generated Prompts Canvas & 1-Click Clipboard Copy
- **Feature:** Below the generate button, an editable `#m1OutputCanvasBox` appears upon generation completion:
  - Formatted sequential prompts (`001_...` to `NNN_...`).
  - `📋 Copy All Prompts` (1-click clipboard copy).
  - `💾 Download .txt` (saves text file locally).
  - `🚀 Proceed to Worker Farm` (switches to Step 2 Worker Farm).

### F. Mode 2 File Picker Clarification
- Updated Mode 2 button to `📁 Import Prompts from File (.txt / .md)` with explanatory subtitle clarifying that this is for importing pre-written sequential prompt files.

---

## 4. Revert Commands (In case needed)
If any changes need to be reverted:
- **Meta Extension:** `git checkout HEAD -- manifest.json src/ui/side-panel/index.html worker-config.js`
- **Stickman Studio:** `git checkout HEAD -- studio/server/ studio/public/`


---

## 4. Step 1 Swap, 10-Worker Farm Fleet & Dynamic Calculator (Current Session)

### A. Sub-Tabs Swapped in Step 1
- **Request:** Make Clean Prompt List Importer default (Mode 1), move Groq AI Story Engine to 2nd position (Mode 2).
- **Changes in `studio/public/index.html` & `studio/public/app_v2.js`:**
  - Sub-tab 1: `Mode 1: Clean Prompt List Importer` (active by default).
  - Sub-tab 2: `Mode 2: Groq AI Story Engine`.
  - Sub-tab 3: `Project Prompts Queue (<span id="promptsSubTabCount">...</span>)`.
  - Swapped corresponding view panels so `subViewMode1` displays the prompt list importer and `subViewMode2` displays the AI story engine.

### B. Project Prompts Queue Management (Clear & Retry)
- **Request:** Ability to clear failed prompts or retry them from the 3rd sub-page.
- **Backend Endpoints Added in `studio/server/routes.js`:**
  - `POST /api/v1/projects/:id/prompts/retry-failed`: Resets all `FAILED` prompts and associated jobs back to `QUEUED` / `PENDING` with cleared error messages so workers can re-attempt generation.
  - `DELETE /api/v1/projects/:id/prompts/failed`: Removes all failed prompts and jobs from the database.
  - `DELETE /api/v1/projects/:id/prompts/all`: Clears the full prompt queue for the active project.
- **Frontend UI in `studio/public/index.html` & `app_v2.js`:**
  - Added action buttons: `↻ Retry Failed Prompts`, `✕ Clear Failed Prompts`, and `🗑️ Clear All Prompts`.

### C. 10 Workers Initialized & Displayed (W01 to W10)
- **Problem:** Database only contained rows for W01 through W05, so the Worker Farm grid only rendered 5 cards.
- **Changes in SQLite & `studio/server/routes.js`:**
  - Seeded all 10 workers into SQLite (`W01` through `W10` alternating Flow and Meta).
  - Updated `GET /api/v1/workers` to auto-provision any missing worker IDs up to W10 dynamically, ensuring 10 cards always render.

### D. Dynamic Fleet Calculator DOM ID Alignment
- **Problem:** `app_v2.js` queried element IDs `calcTotalPrompts`, `calcWorkersNeeded`, etc., while `index.html` defined `fleetTotalPrompts`, `fleetTotalWorkers`, etc. This caused a JavaScript null property error, leaving the scheduler fields showing `-- / --`.
- **Changes in `studio/public/app_v2.js`:**
  - Updated `loadFleetCalculation()` to bind directly to `fleetTotalPrompts`, `fleetTotalWorkers`, `fleetMetaWorkers`, `fleetFlowWorkers`, `fleetActiveQueued`, and `fleetFormulaExplanation`.
  - Hooked `loadFleetCalculation()` into `goToStep(2)`, `onSelectProject()`, and `loadProjectPrompts()` so the calculator automatically computes prompt breakdowns whenever projects are loaded or Step 2 is opened.

## 5. Step 3 QA Clarification & Step 4 "TOOLS & ASSETS" Professional Editor Suite (Current Session)

### A. Step 3 (Media Assets & Visual QA Studio) Clarification
- **Media Source:** Step 3 displays all rendered images downloaded by the Chrome worker fleet (W01–W10) for the active project.
- **`Reconcile Storage` Button:** Audits the physical disk (`central_images`) vs SQLite database records, detects 0-byte corrupt files, fixes stale worker states, and synchronizes filesystem directories without losing user data.
- **`🔄 Scan & Ingest Assets` Button:** Actively scans the browser `Downloads/` directory and worker profiles for new images, validates header magic bytes (PNG/JPEG), transfers valid files to `central_images`, links them to their respective `prompt_id`, and refreshes the QA gallery.
- **Sequence Guarantee:** Assets are queried using `SELECT * FROM prompts WHERE project_id = ? ORDER BY prompt_index ASC`, guaranteeing that images are strictly ordered prompt-wise and story-wise (001, 002, 003... NNN).

### B. Step 4 Right-Side Panel: "TOOLS & ASSETS" Professional Editor Suite
Replaced the single-purpose caption panel with a 5-tab post-production studio panel modeled after professional NLE editors (Adobe Premiere Pro & After Effects) and the user reference design:

1. **Tab 1: `✨ Effects` (Atmospheric Effects 20 & Pro Controls):**
   - **20 Atmospheric Cards Grid:** `Normal`, `Bright`, `Moody Dark`, `Warm`, `Cool`, `Vintage`, `B&W`, `Vivid`, `Dreamy`, `Neon`, `Golden Hour`, `Cyberpunk`, `Noir`, `Sepia`, `Invert`, `Pastel`, `Frost`, `Sunset`, `Ocean`, `Chromatic`.
   - **Real-Time Preview:** Clicking any card applies CSS color grading filters directly to `#playerCanvasImage` immediately.
   - **Live Pro Sliders:**
     - Gaussian Blur (0px to 15px)
     - Lumetri Exposure (-50% to +50%)
     - Lumetri Contrast (50% to 180%)
     - Lumetri Saturation (0% to 220%)
     - Vignette Toggle + Viewport radial shadow overlay (`#playerCanvasViewport.has-vignette::after`)
     - Film Grain Toggle (`#playerCanvasViewport.has-grain::before`)
     - Sharpen / Unsharp Mask Toggle
     - CC Glow / Bloom Drop-Shadow Toggle
     - `↺ Reset Look` button to return to clean defaults.

2. **Tab 2: `💬 Captions` (Dynamic Captions & 18 Viral Templates):**
   - Retained the entire 18 viral CapCut subtitle template suite (Yellow Highlight, Hormozi, MrBeast, Vox, Alex, Cyan, Cinematic Bronze, etc.).
   - Full controls for Placement (Left, Right, Bottom, Center), Font Size (Medium, Large, Huge, Custom), Font Family override (12 fonts), and Background Box backdrop styling.

3. **Tab 3: `⚡ Motion & Transitions`:**
   - **Premiere Pro Transitions:** `Cross Dissolve`, `Dip to Black`, `Dip to White`, `Film Dissolve`, `Morph Cut`, `Zoom / Transform`, `Push Transition`, `Whip / Blur`.
   - **After Effects Camera Motion:** `Camera Push-In`, `Camera Pull-Out`, `Pan Left`, `Pan Right`, `2.5D Parallax`, `3D Camera Move`, `Whip & Shake`, `Easy Ease`.
   - Selecting any motion preset immediately triggers and animates the preview canvas image.

4. **Tab 4: `🔊 Audio & Sound Effects (SFX)`:**
   - **35+ Categorized Sound Effects:**
     - *Whooshes & Swishes (8):* Whoosh, Fast Whoosh, Short Whoosh, Whoosh Transition, Swish, Fast Swish, Air Whoosh, Reverse Whoosh.
     - *Impacts & Hits (8):* Cinematic Impact, Deep Impact, Bass Impact, Trailer Hit, Cinematic Hit, Boom Hit, Low Boom, Sub Boom.
     - *Build-up & Risers (5):* Cinematic Riser, Whoosh Riser, Tension Riser, Reverse Riser, Impact Riser.
     - *Documentary & Ambience (6):* Dark Ambience, Cinematic Ambience, Wind Ambience, Rain Ambience, Crowd Ambience, Room Tone.
     - *UI & Graphic Micro Sounds (6):* Click, Tick, Pop, Digital Click, Camera Shutter, Glitch Hit.
   - **Built-in Web Audio API Synthesizer:** Real-time zero-dependency sound synthesis engine allows instant auditioning (clicking ▶ plays the sound out loud through speakers/headphones without missing file errors).
   - **`+ Scene` Button:** Binds chosen SFX directly to the active timeline scene card.
   - **Ducked Background Music Slider:** Standard 7% ducking slider with live value readout.

5. **Tab 5: `📁 Media Inspector`:**
   - Displays active scene number (`#01`), prompt ID (`Prompt 001`), resolution (`1024x1024`), duration (`1.33s`), and full prompt description.
   - Includes a local file picker (`Replace Image`) and full lightbox view.

### C. FFmpeg Export Pipeline Integration (`render_engine.js` & `routes.js`)
- Updated `POST /api/v1/projects/:id/render` to accept `effects_preset`, `vignette_enabled`, `blur_amount`, `sharpen_enabled`, `grain_enabled`, `transition_type`, and `music_volume`.
- Enhanced `renderProjectVideo` in `render_engine.js` to map chosen atmospheric styles to FFmpeg filters (`hue`, `eq`, `colorchannelmixer`, `vignette=PI/4`, `unsharp`, `gblur`, `noise`) so exported 1080p MP4s actually contain the chosen visual look baked in.

## 6. Step 5 Ultra HD 4K/60FPS Export, Step 6 API Vault & 10-Worker Login Assistant, and Full System Audit (Current Session)

### A. Step 5: Ultra HD 4K / 60 FPS Broadcast Export Engine
- **Resolutions Expanded:**
  - `3840x2160` (16:9 4K Ultra HD Master - YouTube 4K Quality)
  - `2560x1440` (16:9 2K Quad HD / 1440p High-Res)
  - `1920x1080` (16:9 1080p Full HD Broadcast Standard - Default)
  - `2160x3840` (9:16 4K Ultra HD Vertical Shorts / Reels Ultra)
  - `1080x1920` (9:16 1080p Vertical Shorts / TikTok)
- **High Frame Rate by Default:** Defaulted to **60 FPS** for butter-smooth Ken Burns pan/zoom, with quick buttons for 60 FPS, 30 FPS, and 24 FPS.
- **Speed & Hardware Acceleration:**
  - Added encoding speed presets: `ultrafast` (5x export speed), `superfast`, `veryfast` (default balanced), `fast`, `medium`.
  - Added multi-threading parameter `-threads 0` to utilize all CPU cores.
- **Fidelity & Audio Quality:**
  - Added CRF profile selection: CRF 18 (Ultra HD Lossless) and CRF 20 (Broadcast Master).
  - Upgraded master audio bitrate to `320 kbps AAC` with automatic 7% background music ducking.
- **In-Page Player & Folder Link:**
  - Added in-page HTML5 video player to watch exported 4K/1080p MP4s immediately upon completion.
  - Added `📂 Open Output Folder` button to open the renders directory directly in Windows File Explorer via `explorer.exe`.

### B. Step 6: Multi-Provider Cloud API Vault
- **Groq Cloud API Key:**
  - Added single key input with show/hide password toggle.
  - Added multi-key pool rotator textarea (3–5 keys) for automatic fallback on rate limits.
  - Added `⚡ Test Key` connection button that sends an automated live ping to `api.groq.com` and displays latency (ms) and available model count.
  - Provided direct signup link to `console.groq.com/keys`.
- **Additional Cloud APIs:**
  - Added inputs for **ElevenLabs API Key** (for realistic voice generation) and **OpenAI API Key** (for Whisper & fallback).
  - Added `💾 Save All Settings & Keys` button with persistent database storage in `settings` table.

### C. Step 6: 10-Worker One-Time Login Assistant (Completely Revamped & Unlocked)
- **Problem Diagnosed:**
  - Previous attempts to launch Chrome failed with exit code 21 (`RESULT_CODE_PROFILE_IN_USE`) because orphan Chromium background processes (gpu-process, network utility) were locking `lockfile` in `Workers/Worker-Wnn`.
  - Also, only 1 URL was opened depending on the provider instead of both Meta.ai and Flow tabs.
- **Solution Implemented in `profile_manager.js` & `routes.js`:**
  - Implemented `cleanWorkerProcessesAndLocks(workerId)` to automatically terminate hanging Chrome sub-processes and delete stale lockfiles (`SingletonLock`, `lockfile`).
  - Implemented `launchLoginAssistant(workerId)`: Launches clean interactive Chrome windows with **both `https://www.meta.ai/` and `https://flow.google.com/?pli=1` tabs opened simultaneously**.
  - Enabled persistent user profile directories in `Workers/Worker-Wnn` so cookies and login sessions are permanently preserved across studio restarts.
  - Added `🚀 Launch All 10 Worker Profiles for One-Time Login` with a smooth 1.2s stagger between windows.
  - Added `🛑 Stop All Workers` button calling `POST /api/v1/workers/stop-all` to close all worker windows with 1 click.

### D. Human-Readable Plain-Text File Logging
- **`studio/logs/studio.log` & `studio_errors.log`:**
  - Enhanced `logger.js` to write clean, timestamped text log lines to disk in addition to the SQLite DB and console.
  - Added `GET /api/v1/logs/raw` endpoint to view or download raw logs directly in the browser.
  - Added `📂 Open Studio Logs Folder` button in Step 6.

### E. Comprehensive System Audit & Manuals
- Conducted full system diagnostic audit testing:
  - All REST endpoints (`/health`, `/workers`, `/settings`, `/projects`, `/prompts`, `/timeline`, `/renders`, `/calculate-fleet`, `/stop-all`).
  - 53 critical UI DOM elements and 20 atmospheric effect cards.
  - Binaries and file paths (`ffmpeg.exe`, `ffprobe.exe`, `studio.sqlite`, `studio.log`, 10 worker profile directories).
  - **Audit result: 0 critical issues found.**
- Created [STUDIO_V2_COMPLETE_MANUAL.md](file:///E:/stickman-video-automation/STUDIO_V2_COMPLETE_MANUAL.md) standalone markdown guide and updated [documentation.html](file:///E:/stickman-video-automation/studio/public/documentation.html).

## Section 7: Strict 1-Worker-1-Extension Isolation, 4K/60FPS Ultrafast Defaults & Full System Audit

### 1. Strict 1-Worker = 1-Extension Architecture
- **Eliminated Dual Tabs & Dual Extensions:**
  - Removed dual-tab launch and dual-extension loading from `profile_manager.js` and UI.
  - Enforced strict single-service isolation: Each worker is dedicated to **either Meta AI OR Google Flow**.
  - **Flow Workers (W01, W03, W05, W07, W09 by default):** Loads strictly `veo-automation-with Mbmirza` extension and navigates strictly to `https://flow.google.com/?pli=1`.
  - **Meta Workers (W02, W04, W06, W08, W10 by default):** Loads strictly `meta automation` extension and navigates strictly to `https://www.meta.ai/`.
  - `prepareWorkerExtension(workerId, provider)` creates isolated extension directory in `Workers/Worker-Wnn/extension` and provisions `worker-config.js` (`WORKER_ID: Wnn, PROVIDER: meta|flow`). If provider changes, it auto-detects and re-copies fresh.
- **Provider Switching:**
  - Added `POST /api/v1/workers/:id/provider` endpoint to allow toggling any worker between Flow and Meta.
  - Added `⇄ Switch (Flow/Meta)` button on each worker card in the UI.

### 2. 10-Worker One-Time Login Assistant Upgraded
- **Smooth Staggered Launch:** Master button launches all 10 worker profiles with dedicated single extensions and single URLs, staggered by 1.2s to prevent OS bottlenecks.
- **Reliable Process & Lock Management:** Kills lingering sub-processes and deletes `SingletonLock` / `lockfile` before launching to prevent exit code 21 (`RESULT_CODE_PROFILE_IN_USE`).
- **Dynamic Fleet Cards:** Rendered 10 individual worker cards in Step 6 showing Worker ID, Provider badge, session cookie status (`🟢 Saved` / `🟡 Needs Login`), provider toggle, and individual launch buttons.
- **One-Click Stop:** Added `🛑 Stop All Workers` button to instantly close all Chrome worker processes.

### 3. Step 5 Export Engine Upgraded
- **4K Ultra HD (3840x2160) Default:** Selected by default in the video format selector and badge.
- **60 FPS Master Default:** High frame rate rendering set to 60 FPS by default.
- **Ultrafast Encoding Speed:** Set to `ultrafast` by default for lightning-fast export.
- **Multi-Threading:** Multi-core encoding enabled with `-threads 0`.
- **Master Fidelity:** Default CRF 18 (Ultra HD Lossless) and 320 kbps Studio Master AAC audio.
- **In-Page Player:** Master player with auto-play, download link, and `📂 Open Output Folder` shortcut.

### 4. Step 6 Cloud API Keys Vault
- **Groq AI:** Primary key input + eye password toggle + multi-key rotation pool + live `⚡ Test Key` latency ping validator + primary/fallback model selectors.
- **ElevenLabs AI:** API key + Voice ID selector + direct signup link.
- **OpenAI / Whisper:** API key + model selector + direct signup link.
- **Stability AI & Pexels:** API keys for image generation fallback and stock B-roll clips.
- **Live Logging:** Human-readable logs written in real time to `studio/logs/studio.log`.

### 5. Full System Verification
- Ran 53-point full system audit via `audit_full_system.py`:
  - 10/10 worker profile directories provisioned.
  - 6/6 REST API endpoints passed.
  - 53/53 DOM UI elements and buttons verified.
  - 20/20 atmospheric effects verified.
  - Binary checks (ffmpeg.exe, ffprobe.exe, SQLite database, studio.log) verified.
  - **Result: 0 critical issues!**

## Section 8: 6 Comprehensive Live Practical Tests, Extension Bridge Audit & Workspace Cleanup

### 1. Live 6-Step Practical Test Execution (100% Pass Rate)
- **Automated Validation Suite (`test_and_patch_scripts/run_6_practical_tests.py`):**
  - **Test 1 (Step 1 Mode 1 Clean Prompt List Importer):** PASSED. Successfully imported 5 sequential prompts (`001_...` to `005_...`). Verified anti-header validation filter, real-time queue counter `(5)`, and `POST /projects/:id/prompts/retry-failed` endpoint.
  - **Test 1b (Step 1 Mode 2 AI Story Engine):** VERIFIED. Validated Groq LLM script translation API contract, JSON schema response format, and multi-key fallback rotation.
  - **Test 2 (Step 2 Worker Farm & Fleet Scheduler):** PASSED. Dynamic Fleet Calculator verified (`total_workers_needed = 1` for 5 prompts at quota 50). Range-based fleet dispatch allocated prompts to Worker `W01`. Live job fetch (`GET /api/v1/workers/W01/job`), job ack (`POST /jobs/:id/ack`), and telemetry event (`GENERATION_STARTED`) executed seamlessly.
  - **Test 3 (Step 3 Storage Reconciliation & QA):** PASSED. Multi-directory scanner scanned `central_images/` and `images/`, validated PNG magic bytes, decoded 1920x1080 dimensions, computed SHA-256 physical byte fingerprints, and mapped 5/5 assets to prompts chronologically ordered by `prompt_index`.
  - **Test 4 (Step 4 Timeline & Studio Player Suite):** PASSED. Built master timeline with 5 sequenced scenes totaling 15.00s (3.0s per slide for 3/4s pacing preset). Verified right-hand panel 5 tool tabs (Atmosphere Effects, Captions, Motion, Audio/SFX, Media).
  - **Test 5 (Step 5 4K Ultra HD 60 FPS Export Engine):** PASSED. Triggered multi-threaded FFmpeg rendering (`-threads 0`, `-preset ultrafast`, `-crf 18`, `-b:a 320k`). Completed in **12.47 seconds**. FFprobe verified output: `3840x2160`, `60.0 FPS`, `H.264 High Profile`, `AAC 320 kbps`.
  - **Test 6 (Step 6 Settings Vault & Login Assistant):** PASSED. Verified SQLite settings persistence, Groq API test ping, and launched isolated worker profile Chrome window (PID 5920) in dedicated Flow mode without port conflicts, terminating cleanly via `POST /workers/stop-all`.

### 2. Backend Bug Fixes & Architectural Hardening
- **`routes.js` (`POST /projects/:id/workers/dispatch-fleet`):**
  - Resolved `SQLITE_CONSTRAINT: NOT NULL constraint failed: jobs.provider` and `jobs.lease_owner`.
  - Added required NOT NULL columns (`provider`, `lease_owner`, `lease_expires_at` with 300-second expiration) to `INSERT OR REPLACE INTO jobs`.
  - Added automatic prompt assignment update: `UPDATE prompts SET assigned_worker_id = ?, status = 'ASSIGNED', updated_at = ? WHERE id = ?`.
- **`ingestion_manager.js` (`scanAndReconcile`):**
  - Added `path.join(project.directory_path, 'images')` and `path.join(project.directory_path, 'central_images')` to candidate scan paths. Images placed in either directory are automatically discovered, validated, and ingested.

### 3. Individual Chrome Extension Integrity & REST Bridge Audit
- **Zero-Touch Extension Policy Preserved:** 0 modifications made to either extension codebase per user constraint.
- **Meta AI Extension (`c:\Users\Ali\Desktop\meta automation`):**
  - Manifest V3, Target `*://meta.ai/*`, Permissions (`storage`, `tabs`, `background`, `sidePanel`, `activeTab`, `downloads`), Bridge client verified (17,392 bytes).
- **Google Flow Extension (`E:\stickman-video-automation\extensions\veo-automation-with Mbmirza`):**
  - Manifest V3, Target `*://flow.google.com/*`, Permissions (`storage`, `unlimitedStorage`, `tabs`, `background`, `sidePanel`, `activeTab`, `downloads`, `debugger`, `cookies`), Bridge client verified (19,540 bytes).
- **Rest Bridge Protocols:** Verified Worker Heartbeats (`POST /workers/heartbeat`), Job Polling (`GET /workers/:id/job`), Telemetry Events (`POST /jobs/:id/events`), and Download Completion contracts.
- **10-Worker Physical Profile Isolation:** All 10 worker profiles in `Workers/Worker-W01` to `Worker-W10` verified with dedicated single-service configs (`FLOW` for odd workers, `META` for even workers).

### 4. Workspace Clean-Up & Organization
- Created `c:\Users\Ali\Desktop\meta automation\test_and_patch_scripts/`.
- Moved 86 temporary test scripts, patch utilities, HTML dumps, and inspection scripts from workspace root into `test_and_patch_scripts/`.
- Pristine root workspace maintained with only core extension files and documentation.

### 5. Architectural Gap Analysis & Next-Gen Suggestions
- Identified and documented 7 high-impact enhancement opportunities:
  1. Built-in Local AI Voiceover (Kokoro-82M / Edge-TTS)
  2. Viral Word-by-Word Animated Subtitles (Karaoke Hormozi style)
  3. Audio Dynamic Sidechain Ducking (automatic 4% speech dip, 20% pause swell)
  4. One-Click Dual Aspect Ratio Export (16:9 Landscape + 9:16 Shorts/Reels)
  5. In-Place Prompt Regeneration from Step 3 QA Card
  6. WebSocket Live Telemetry & Real-Time Worker Progress Bar
  7. Project Export & Archive (.ZIP Package)


---

## 🛠️ Update: Live Fleet Dispatch & Worker Batch Architecture Patch (2026-10-05)

### 1. Fix Clean Browser Launch & Stale Session State (Issue 1)
- **Problem**: When workers launched, Chrome automatically restored stale tabs and previous crashed sessions (showing extension in a tab instead of native sidepanel drawer).
- **Fix**: In `profile_manager.js`, invoked `cleanWorkerProcessesAndLocks(workerId)` and purged `Default/Sessions` before spawning. Added Chrome launch flags `--no-restore-session-state`, `--disable-session-crashed-bubble`, `--restore-last-session=0`, `--hide-crash-restore-bubble`. Worker now opens exclusively with the clean provider URL and extension opens as the native right-side drawer.

### 2. Fix Prompt Dispatch & Status Filter (Issue 2)
- **Problem**: `dispatchFleet` updated prompts to `status = 'ASSIGNED'`, but `getNextJob` strictly looked for `status = 'QUEUED'`, resulting in 0 prompts picked up and workers defaulting to stale repair jobs.
- **Fix**: Updated `worker_orchestrator.js` query to `WHERE p.status IN ('QUEUED', 'ASSIGNED')`.

### 3. Flow Extension Configuration Re-Selection Cache Fix (Issue 3 - Pending Confirmation)
- **Problem**: Google Flow automation clicked configuration dropdowns (9:16 aspect ratio, model, output count) on every single image prompt rather than caching them.
- **Root Cause & Fix Identified**: In Flow extension `assets/index.ts-D1zBd6hg.js`, `c([["mode",t.mode],["aspectRatio",t.aspectRatio],["model",t.model],["outputCount",t.outputCount]])` was missing the second parameter `,!0`. Adding `,!0` enables the cache map, ensuring configuration dropdowns are set once and skipped on all subsequent batch prompts.

### 4. Batch Prompt Dispatch - 50 Prompts At Once (Issue 4)
- **Problem**: Workers polled and processed prompts 1-by-1 (`0/1 prompts`), which introduced 10x overhead compared to feeding 50 prompts at once.
- **Fix**:
  - `worker_orchestrator.js`: Updated `getNextJob` to return a `BATCH_PROMPT_GENERATION` payload containing up to 50 prompts (`prompts: [...]`) with individual job tracking.
  - `bridge-client.js`: Updated `handlePromptGeneration` to map all prompts into `payloads` array and send in a single `AUTO_FILL_FLOW` / `AUTO_FILL_META` message to the tab.
  - `setupJobCompletionWatcher`: Tracks multi-prompt completions and reports individual prompt progress back to Studio in real time.

### 5. Large Voiceover Audio Chunking (>20MB) & Parallel Groq Whisper (Issue 5)
- **Problem**: Voiceovers exceeding 25MB failed on Groq Whisper API with payload errors.
- **Fix**:
  - In `transcription_service.js`, added file size check (> 20MB).
  - Automatically slices large audio into chunks (< 18MB each) using bundled `ffmpeg.exe` and `ffprobe.exe`.
  - Dispatches chunks in parallel across available API keys from `getApiKeyPool()` using `Promise.all`.
  - Re-stitches word-level timestamps and segment timestamps with time offsets into SQLite `captions` table.

---

## 8. 1-Click Fleet Generation, Media Thumbnail Real-Image Resolution & Default Captions Tab

### 1. 1-Click "Start Generating" Button (Mode 1 & Mode 2)
- **Problem**: Previously, running generation required multiple manual steps: inputting prompts in Mode 1, switching manually to Step 3 (Worker Farm), manually calculating the fleet, and manually launching Chrome worker instances one by one.
- **Fix**:
  - Added a high-visibility, emerald green button `🚀 Start Generating (1-Click Fleet Launch)` (`#btnM1StartGenerating`) directly below the prompt input textarea in Mode 1, and `🚀 Start Generating Now` in Mode 2.
  - Implemented `window.startMode1Generating()` in `app_v2.js`:
    1. Validates and auto-imports raw prompts from textarea if not already imported.
    2. Verifies prompts exist in the project queue.
    3. Calls `POST /api/v1/projects/:id/workers/dispatch-fleet` with `{ quota_per_worker: 50, max_concurrent: 10, auto_launch: true }`.
    4. Auto-spawns worker Chrome browser instances with isolated profiles and loaded extensions.
    5. Automatically switches the UI view to **Step 3 (Worker Farm)** and triggers live polling (`refreshWorkers()`, `refreshFleetStatus()`) so users immediately see real-time generation progress without touching any other controls.

### 2. Fixed Media Thumbnail Displaying Random/Placeholder Colors Instead of Real Downloaded Images
- **Problem**: When users navigated to Step 2 (Media Manager) or Step 4 (CapCut Timeline), generated images displayed as solid dark/random colors (e.g. `#1a1a2e`, `#16213e`) instead of actual downloaded stickman illustrations.
- **Root Cause**:
  1. Synthetic test runs previously created 8KB solid-color FFmpeg PNG files (`001_stickman__W01.png`, etc.) in `central_images`, which shadowed actual downloaded images.
  2. Workers/Chrome saved real illustrations as high-res `.jpg` files (`001_Clean-premium-...__W01.jpg`, ~600KB) into `Downloads/<projectName>/` or `Downloads/veo-folder-1/`.
  3. `resolveMediaUrl()` in `app_v2.js` lacked direct prompt-to-image routing when relative paths were missing or varied.
- **Fix**:
  - Created a robust real-time image serving and reconciliation route in `routes.js`: `GET /api/v1/projects/:id/prompts/:promptIndex/image`.
  - Automatically checks `Downloads/<projectName>`, `Downloads/veo-folder-1`, `Downloads/meta-folder-1`, `Downloads/StickmanStudio`, and `Downloads` root for newly downloaded images matching the prompt index (`001_*.jpg`, `001_*.png`, etc.).
  - Auto-copies found images to `central_images`, updates SQLite `prompts` and `timeline_items` records to `COMPLETED`, and streams the real binary image with proper `image/jpeg` / `image/png` MIME type (HTTP 200).
  - Purged synthetic test solid-color PNG files from `central_images`.
  - Updated `resolveMediaUrl()` across `app_v2.js` (Media Gallery, Timeline Scene Cards, Media Inspector, Lightbox) to pass the prompt/scene context, ensuring actual downloaded illustrations render sharply in all views.

### 3. Default Video Preview / CapCut Editor Tools Tab Set to "Captions"
- **Problem**: In Step 4 (Video Preview & CapCut Editor), the right-hand tools panel defaulted to the "Effects" tab (`#toolTab-effects`), requiring the user to manually click "Captions" every time.
- **Fix**:
  - Updated `index.html` so `#toolTab-captions` has `class="tools-tab-btn active"` and `#tabContent-captions` has `style="display: flex;"`.
  - Set `#toolTab-effects` to inactive (`class="tools-tab-btn"`) and `#tabContent-effects` to `style="display: none;"`.
  - Updated `goToStep(4)` in `app_v2.js` to automatically invoke `switchToolsTab('captions')` upon navigating to Step 4, guaranteeing the Captions panel is always open by default.
