manual_path = r'c:\Users\Ali\Desktop\meta automation\STUDIO_V2_COMPLETE_MANUAL.md'
with open(manual_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_content = """
---

## 5. Live Fleet & UI Usability Updates

### 1-Click "Start Generating" Fleet Launch
- **Location**: Step 1 (Mode 1 & Mode 2) right below the prompt text area.
- **Action**: Users click `🚀 Start Generating (1-Click Fleet Launch)` to simultaneously:
  1. Validate & import raw prompts into SQLite.
  2. Compute optimal worker partitioning (50 prompts per worker, safe concurrency cap).
  3. Auto-spawn browser worker instances (`auto_launch: true`) with isolated clean profiles.
  4. Automatically navigate the user directly into **Step 3 (Worker Farm)** with live polling active.

### Live Thumbnail Auto-Sync & Real Image Serving
- **Endpoint**: `GET /api/v1/projects/:id/prompts/:promptIndex/image`
- **Behavior**: Scans browser download directories (`Downloads/<project>`, `Downloads/veo-folder-1`, etc.) for newly downloaded `.jpg` / `.png` / `.webp` stickman illustrations, copies them to `central_images`, updates prompt status to `COMPLETED`, and serves the binary image to the frontend.
- **Fix**: Eliminates dark/random solid color placeholders in Media Manager, Scene Cards, and CapCut Timeline.

### Step 4 Default Tools Panel: Captions Tab
- The tools panel in Step 4 now defaults to **Captions** (`#toolTab-captions` active, `#tabContent-captions` flex).
- Caption styling, subtitle syncing, and word-level karaoke controls are immediately displayed when entering Step 4.
"""

with open(manual_path, 'a', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully updated STUDIO_V2_COMPLETE_MANUAL.md!")
