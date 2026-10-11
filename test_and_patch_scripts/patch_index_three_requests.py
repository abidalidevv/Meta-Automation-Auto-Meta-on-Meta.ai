import os

index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Mode 1 buttons to add Start Generating
m1_target = """              <div style="display: flex; gap: 12px;">
                <button class="btn btn-primary" onclick="importRawPrompts()" style="padding: 12px 24px; font-size: 14px; font-weight: 800;">
                  ? Validate & Import Prompts
                </button>
              </div>"""

m1_replacement = """              <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                <button type="button" id="btnM1StartGenerating" class="btn btn-emerald" onclick="startMode1Generating()" style="padding: 13px 28px; font-size: 15px; font-weight: 800; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); display: flex; align-items: center; gap: 8px; cursor: pointer;">
                  <span>🚀</span> Start Generating (1-Click Fleet Launch)
                </button>
                <button type="button" class="btn btn-secondary" onclick="importRawPrompts()" style="padding: 13px 20px; font-size: 13px; font-weight: 700; cursor: pointer;">
                  ✔ Validate & Import Only
                </button>
              </div>"""

assert m1_target in text, "m1_target not found in index.html"
text = text.replace(m1_target, m1_replacement, 1)

# 2. Add Start Generating to Mode 2 Output Canvas as well
m2_target = """                    <button type="button" class="btn btn-primary" onclick="proceedFromM1ToWorkerFarm()" style="font-size: 12px; padding: 6px 16px; cursor: pointer;">
                      ? Proceed to Worker Farm ?
                    </button>"""

m2_replacement = """                    <button type="button" class="btn btn-emerald" onclick="startMode1Generating()" style="font-size: 12px; padding: 6px 18px; cursor: pointer; font-weight: 800; box-shadow: 0 0 15px rgba(16, 185, 129, 0.35);">
                      <span>🚀</span> Start Generating Now
                    </button>
                    <button type="button" class="btn btn-primary" onclick="proceedFromM1ToWorkerFarm()" style="font-size: 12px; padding: 6px 16px; cursor: pointer;">
                      ? Open Worker Farm ?
                    </button>"""

assert m2_target in text, "m2_target not found in index.html"
text = text.replace(m2_target, m2_replacement, 1)

# 3. Make Captions the default active tab in Step 4 tools panel
tabs_target = """              <div class="tools-tab-bar">
                <button type="button" class="tools-tab-btn active" id="toolTab-effects" onclick="switchToolsTab('effects')">
                  <span>?</span> Effects
                </button>
                <button type="button" class="tools-tab-btn" id="toolTab-captions" onclick="switchToolsTab('captions')">
                  <span>?</span> Captions
                </button>"""

tabs_replacement = """              <div class="tools-tab-bar">
                <button type="button" class="tools-tab-btn" id="toolTab-effects" onclick="switchToolsTab('effects')">
                  <span>?</span> Effects
                </button>
                <button type="button" class="tools-tab-btn active" id="toolTab-captions" onclick="switchToolsTab('captions')">
                  <span>?</span> Captions
                </button>"""

assert tabs_target in text, "tabs_target not found in index.html"
text = text.replace(tabs_target, tabs_replacement, 1)

# 4. Swap display styles for effects vs captions in tools tab content
content_target = """            <!-- ================= TAB 1: ATMOSPHERIC EFFECTS ================= -->
            <div class="tools-tab-content" id="tabContent-effects">"""

content_replacement = """            <!-- ================= TAB 1: ATMOSPHERIC EFFECTS ================= -->
            <div class="tools-tab-content" id="tabContent-effects" style="display: none;">"""

assert content_target in text, "content_target not found in index.html"
text = text.replace(content_target, content_replacement, 1)

captions_target = """            <!-- ================= TAB 2: CAPTIONS / WORD-LEVEL TIMING ================= -->
            <div class="tools-tab-content" id="tabContent-captions" style="display: none;">"""

captions_replacement = """            <!-- ================= TAB 2: CAPTIONS / WORD-LEVEL TIMING ================= -->
            <div class="tools-tab-content" id="tabContent-captions" style="display: flex;">"""

assert captions_target in text, "captions_target not found in index.html"
text = text.replace(captions_target, captions_replacement, 1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated index.html with Start Generating button and default Captions tab!")
