new_section = """

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
"""

for path in [r'C:\Users\Ali\Desktop\meta automation\changes.md', r'E:\stickman-video-automation\changes.md']:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(new_section)
print('Updated both changes.md files successfully!')
