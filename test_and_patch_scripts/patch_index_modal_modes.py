with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update modal tabs order and clean text
old_modal_tabs = """      <!-- Mode Selector Tabs -->
      <div class="modal-tabs">
        <button type="button" id="tabNewProjMode1" class="modal-tab-btn active" onclick="switchNewProjectModalTab('MODE_1')">
          MODE 2 ? Generate Everything
        </button>
        <button type="button" id="tabNewProjMode2" class="modal-tab-btn" onclick="switchNewProjectModalTab('MODE_2')">
          MODE 1 ? Existing Prompt List
        </button>
      </div>"""

# Check how it looks right now
import re
tabs_match = re.search(r'<div class="modal-tabs">.*?</div>', text, re.DOTALL)
if tabs_match:
    old_tabs_block = tabs_match.group(0)
    print("Found old tabs block:\n", old_tabs_block)
    
    new_tabs_block = """<div class="modal-tabs">
        <button type="button" id="tabNewProjMode2" class="modal-tab-btn active" onclick="switchNewProjectModalTab('MODE_2')">
          📋 MODE 1 — Existing Prompt List
        </button>
        <button type="button" id="tabNewProjMode1" class="modal-tab-btn" onclick="switchNewProjectModalTab('MODE_1')">
          ⚡ MODE 2 — Generate Everything (Groq AI)
        </button>
      </div>"""
    text = text.replace(old_tabs_block, new_tabs_block)

# 2. Update info box in modalMode1Container (AI Generation)
text = re.sub(
    r'<strong style="color: var\(--cyan\);">Mode 1 Workflow:</strong> Provide Title, Voiceover, Script, Master Prompt & Character Reference\. The Groq AI Story Engine will auto-generate sequential prompt scenes matching your audio duration\.',
    r'<strong style="color: var(--cyan);">Mode 2 Workflow (AI Generation):</strong> Provide Title, Voiceover, Script, Master Prompt &amp; Character Reference. The Groq AI Story Engine will auto-generate sequential prompt scenes matching your audio duration.',
    text
)

# 3. Update info box in modalMode2Container (Prompt List)
text = re.sub(
    r'<strong style="color: var\(--violet\);">Mode 2 Workflow:</strong> You already have a formatted prompt list',
    r'<strong style="color: var(--violet);">Mode 1 Workflow (Existing Prompt List):</strong> You already have a formatted prompt list',
    text
)

# 4. Make sure initial hidden input reflects MODE_2 by default
text = text.replace(
    '<input type="hidden" id="newProjActiveMode" value="MODE_1" />',
    '<input type="hidden" id="newProjActiveMode" value="MODE_2" />'
)

# 5. Also make sure modalMode2Container is displayed first and modalMode1Container is hidden by default
text = text.replace(
    '<div id="modalMode1Container">',
    '<div id="modalMode1Container" style="display: none;">'
)
text = text.replace(
    '<div id="modalMode2Container" style="display: none;">',
    '<div id="modalMode2Container" style="display: block;">'
)

with open(r'E:\stickman-video-automation\studio\public\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated index.html modal tabs & info banners!")
