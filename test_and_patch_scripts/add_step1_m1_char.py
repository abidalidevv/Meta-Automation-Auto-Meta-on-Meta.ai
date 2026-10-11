with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """              <!-- Prompts Input Textarea -->
              <div class="form-group">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <label class="form-label" style="margin-bottom: 0;">Paste Raw Prompts (1 per line with 001_ prefix)</label>"""

char_card = """              <!-- Mode 1 Character Reference & Visual Consistency -->
              <div style="background: rgba(10, 14, 24, 0.7); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 18px;">
                <div style="font-size: 12px; font-weight: 800; color: var(--cyan); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">
                  🎭 Character Reference & Visual Consistency
                </div>

                <div class="char-ref-card" style="margin-bottom: 14px;">
                  <div class="char-ref-thumb-box" id="step1M1CharThumbBox">
                    <span id="step1M1CharPlaceholder" class="char-ref-placeholder">🎭</span>
                    <img id="step1M1CharThumb" class="char-ref-thumb-img" alt="Character Reference" />
                  </div>
                  <div class="char-ref-meta">
                    <div class="char-ref-name">Character Consistency Reference Image</div>
                    <div class="char-ref-status" id="step1M1CharStatusText">Pick reference image to lock character appearance across all scenes</div>
                    <div style="display: flex; gap: 8px; margin-top: 6px;">
                      <input type="file" id="step1M1CharFile" accept="image/*" style="display: none;" onchange="handleStep1M1CharImage(this)" />
                      <button type="button" class="btn btn-secondary" onclick="document.getElementById('step1M1CharFile').click()" style="font-size: 11.5px; padding: 6px 12px; cursor: pointer;">
                        📁 Pick Reference Image
                      </button>
                      <button type="button" class="btn btn-secondary" id="step1M1CharRemoveBtn" onclick="removeStep1M1CharImage()" style="font-size: 11.5px; padding: 6px 10px; display: none; color: var(--rose); cursor: pointer;">
                        ✕ Remove
                      </button>
                    </div>
                  </div>
                </div>

                <div class="grid-2">
                  <div class="form-group">
                    <label class="form-label">Character Name</label>
                    <input type="text" id="step1M1CharName" class="form-input" value="Main Stickman" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Character Visual Consistency Prompt Tags</label>
                    <input type="text" id="step1M1CharDesc" class="form-input" placeholder="e.g. Minimalist stickman hero wearing red headband and blue sneakers, black ink outlines" />
                  </div>
                </div>
              </div>

              <!-- Prompts Input Textarea -->
              <div class="form-group">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <label class="form-label" style="margin-bottom: 0;">Paste Raw Prompts (1 per line with 001_ prefix)</label>"""

if target in text:
    text = text.replace(target, char_card)
    with open(r'E:\stickman-video-automation\studio\public\index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Added Character Reference to Step 1 Mode 1 in index.html!")
else:
    print("TARGET NOT FOUND in index.html!")
