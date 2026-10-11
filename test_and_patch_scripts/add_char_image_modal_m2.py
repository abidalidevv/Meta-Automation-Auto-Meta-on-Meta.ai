with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Add character reference image picker to Modal Mode 2
old_char_section = """        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Character Reference Name</label>
            <input type="text" id="newProjCharNameM2" class="form-input" value="Main Stickman" />
          </div>

          <div class="form-group">
            <label class="form-label">Character Visual Consistency Description</label>
            <input type="text" id="newProjCharDescM2" class="form-input" placeholder="e.g. Minimalist stickman hero, red headband, sneakers" />
          </div>
        </div>
      </div>"""

new_char_section = """        <div class="char-ref-picker-card" style="margin-bottom: 14px; margin-top: 6px;">
          <div class="char-ref-thumb-box" id="newProjCharThumbBoxM2">
            <span class="char-ref-thumb-placeholder" id="newProjCharPlaceholderM2">&#127760;</span>
            <img id="newProjCharThumbM2" class="char-ref-thumb-img" alt="Character Reference" />
          </div>
          <div class="char-ref-meta">
            <div class="char-ref-name">Stickman Character Reference Image</div>
            <div class="char-ref-status" id="newProjCharStatusTextM2">Upload reference image to lock character visual consistency across all scenes</div>
            <div style="display: flex; gap: 8px; margin-top: 6px;">
              <input type="file" id="newProjCharFileM2" accept="image/*" style="display: none;" onchange="handleModalCharImage(this, 'm2')" />
              <button type="button" class="btn btn-secondary" onclick="document.getElementById('newProjCharFileM2').click()" style="font-size: 11.5px; padding: 6px 12px; cursor: pointer;">
                &#127775; Pick Reference Image
              </button>
              <button type="button" class="btn btn-secondary" id="newProjCharRemoveBtnM2" onclick="removeModalCharImage('m2')" style="font-size: 11.5px; padding: 6px 10px; display: none; color: var(--rose); cursor: pointer;">
                &#10006; Remove
              </button>
            </div>
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Character Reference Name</label>
            <input type="text" id="newProjCharNameM2" class="form-input" value="Main Stickman" />
          </div>

          <div class="form-group">
            <label class="form-label">Character Visual Consistency Description</label>
            <input type="text" id="newProjCharDescM2" class="form-input" placeholder="e.g. Minimalist stickman hero, red headband, sneakers" />
          </div>
        </div>
      </div>"""

if old_char_section in text:
    text = text.replace(old_char_section, new_char_section)
    with open(r'E:\stickman-video-automation\studio\public\index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully added character reference image picker to Modal Mode 2!")
else:
    print("Target string not found in index.html")
    # Let's try to find what's there
    idx = text.find('newProjCharNameM2')
    print("Context around newProjCharNameM2:")
    print(repr(text[idx-300:idx+400]))
