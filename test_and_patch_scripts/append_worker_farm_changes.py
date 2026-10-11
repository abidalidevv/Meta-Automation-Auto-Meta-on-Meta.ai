new_section = """

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
"""

for path in [r'C:\Users\Ali\Desktop\meta automation\changes.md', r'E:\stickman-video-automation\changes.md']:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(new_section)
print("Updated changes.md with Section 4!")
