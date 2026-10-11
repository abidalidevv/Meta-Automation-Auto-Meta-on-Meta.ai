import os

manual_path1 = r'c:\Users\Ali\Desktop\meta automation\STUDIO_V2_COMPLETE_MANUAL.md'
manual_path2 = r'E:\stickman-video-automation\STUDIO_V2_COMPLETE_MANUAL.md'

with open(manual_path1, 'r', encoding='utf-8') as f:
    text = f.read()

# Update Step 5 section to emphasize 4K 60FPS Ultrafast defaults
old_s5 = """### 🚀 Step 5: Broadcast & Ultra HD 4K / 1080p Export Engine
1. **Video Format & Resolution:**
   * 🌟 **3840x2160 (16:9 - 4K Ultra HD Master - YouTube 4K Quality)**
   * 💎 **2560x1440 (16:9 - 2K Quad HD / 1440p High-Res)**
   * 🎬 **1920x1080 (16:9 - 1080p Full HD Broadcast Standard)**
   * 📱 **2160x3840 (9:16 - 4K Ultra HD Vertical Shorts / Reels Ultra)**
   * 📱 **1080x1920 (9:16 - 1080p Vertical Shorts / TikTok / Reels)**
2. **High-Speed Encoding & Frame Rate Controls:**
   * **Frame Rate (FPS):** Defaults to **60 FPS** (with instant 60/30/24 FPS quick-toggle buttons).
   * **Encoding Speed Presets:** `ultrafast` (5x faster render), `superfast`, `veryfast` (default), `fast`, `medium`.
   * **Multi-Threading:** Automatically invokes `-threads 0` to leverage all CPU cores simultaneously."""

new_s5 = """### 🚀 Step 5: Broadcast & Ultra HD 4K / 1080p Export Engine
1. **Default Master Resolution (4K Ultra HD):**
   * 🌟 **3840x2160 (16:9 - 4K Ultra HD Master - YouTube 4K Quality)** — Selected by default for pristine visual fidelity!
   * 💎 **2560x1440 (16:9 - 2K Quad HD / 1440p High-Res)**
   * 🎬 **1920x1080 (16:9 - 1080p Full HD Broadcast Standard)**
   * 📱 **2160x3840 (9:16 - 4K Ultra HD Vertical Shorts / Reels Ultra)**
   * 📱 **1080x1920 (9:16 - 1080p Vertical Shorts / TikTok / Reels)**
2. **High-Speed Encoding & 60 FPS Master Controls:**
   * **Frame Rate (FPS):** Defaults to **60 FPS Master** (with quick-select buttons for 60, 30, and 24 FPS).
   * **Speed Preset:** Defaults to **`ultrafast`** (5x acceleration) utilizing multi-core multi-threading (`-threads 0`).
   * **Video Fidelity (CRF):** Defaults to **CRF 18** (Ultra HD Lossless profile) for maximum bitrate and clarity.
   * **Audio Bitrate:** Defaults to **320 kbps** Studio Master AAC Audio with 7% background music ducking."""

if old_s5 in text:
    text = text.replace(old_s5, new_s5)

# Update Step 6 section to reflect strict 1-worker-1-extension architecture
old_s6 = """### ⚙️ Step 6: Settings, API Keys Vault & 10-Worker Login Assistant
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
   * `📂 Open Studio Logs Folder` button (opens logs folder in Windows Explorer)."""

new_s6 = """### ⚙️ Step 6: Settings, API Keys Vault & 10-Worker Login Assistant
1. **AI Cloud API Keys Vault:**
   * **Groq Cloud API Key:** Primary key input with show/hide password toggle, multi-key rotation pool (1 key per line for automatic failover), model selectors (`llama-3.3-70b-versatile` & `llama-3.1-8b-instant`), and live `⚡ Test Key` connection validator with latency ping.
   * **ElevenLabs API Key & Voice ID:** Supports realistic narration voices (e.g. Rachel `21m00Tcm4TlvDq8ikWAM`).
   * **OpenAI API Key & Model:** For GPT-4o story script generation and high-accuracy Whisper voice alignment.
   * **Stability AI / SDXL Key:** For image generation fallback.
   * **Pexels API Key:** For stock B-roll video footage and visual clips.
   * `💾 Save All Settings & API Keys` button with persistent SQLite database storage.
2. **Dedicated 1-Worker = 1-Extension Architecture (No Dual Tabs):**
   * **Strict Isolation Rule:** Each worker profile runs strictly **ONE service and ONE extension** (either Meta.ai OR Google Flow). Dual tabs and dual extensions are forbidden to prevent cookie collisions and session invalidations.
   * **Flow Workers (W01, W03, W05, W07, W09):** Opens `https://flow.google.com/?pli=1` with `Veo Flow Automation` extension loaded and isolated config (`WORKER_ID: Wnn, PROVIDER: flow`).
   * **Meta Workers (W02, W04, W06, W08, W10):** Opens `https://www.meta.ai/` with `Meta Automation` extension loaded and isolated config (`WORKER_ID: Wnn, PROVIDER: meta`).
   * **Provider Toggle (`⇄ Switch`):** Instant 1-click toggle to switch any worker between Flow and Meta directly from the UI or via `POST /api/v1/workers/:id/provider`.
   * **Master Launch Button:** `🚀 Launch All 10 Worker Profiles for One-Time Login` launches all 10 dedicated profiles with a 1.2s smooth stagger.
   * **Individual Worker Launch Grid:** Dynamic 10-card fleet grid showing Worker ID, Provider badge, session cookie status (`🟢 Saved` / `🟡 Login Needed`), and individual `🚀 Open Login` buttons.
   * **Lockfile & Zombie Process Auto-Cleaner:** Automatically terminates hanging Chrome crashpad/gpu sub-processes and unlinks stale `SingletonLock` / `lockfile` so Chrome launches with 100% reliability.
   * **Permanent Session Persistence:** Cookies and tokens are saved in `Workers/Worker-Wnn/Default/Network/Cookies`. Log in once by hand, and the automated farm runs indefinitely without prompts.
   * **`🛑 Stop All Workers` Button:** 1-click safe shutdown of all running Chrome worker instances.
3. **Live System Telemetry & Plain-Text File Logging:**
   * Real-time live telemetry stream in UI.
   * Writes human-readable plain-text logs to `studio/logs/studio.log` and `studio/logs/studio_errors.log`.
   * `📄 View studio.log` button (opens raw log file in browser tab).
   * `📂 Open Studio Logs Folder` & `📁 Open Workers Profiles Folder` shortcuts in Windows Explorer."""

text = text.replace(old_s6, new_s6)

# Write to both paths
with open(manual_path1, 'w', encoding='utf-8') as f:
    f.write(text)

with open(manual_path2, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated STUDIO_V2_COMPLETE_MANUAL.md in both locations!')
