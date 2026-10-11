import os

changes_path = r'c:\Users\Ali\Desktop\meta automation\changes.md'
with open(changes_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_entry = """

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
"""

with open(changes_path, 'a', encoding='utf-8') as f:
    f.write(new_entry)

print("Updated changes.md successfully")
