with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="newProjectModal"')
# find the end of modal content (before closing overlay div)
idx2 = text.find('<!-- ==================== LIGHTBOX', idx1)
if idx2 == -1:
    idx2 = text.find('id="lightboxModal"', idx1)

print("idx1:", idx1, "idx2:", idx2)
old_modal_html = text[idx1:idx2]

simple_modal_html = """id="newProjectModal" class="modal-overlay">
    <div class="modal-content" style="max-width: 540px; border-radius: var(--radius-md); box-shadow: 0 20px 60px rgba(0,0,0,0.8);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div style="font-family: var(--font-display); font-size: 19px; font-weight: 800; color: #fff;">
          + Create New Production Project
        </div>
        <button onclick="closeNewProjectModal()" style="background: none; border: none; color: var(--text-dim); font-size: 24px; cursor: pointer;">&times;</button>
      </div>

      <div style="background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: var(--radius-sm); padding: 12px 14px; margin-bottom: 18px; font-size: 12px; color: var(--text-muted); line-height: 1.5;">
        <strong style="color: var(--cyan);">Fast Project Setup:</strong> Enter your project name below. All prompt importing, story scripting, and character consistency are configured directly in <strong style="color: #fff;">Step 1</strong>.
      </div>

      <div class="form-group" style="margin-bottom: 16px;">
        <label class="form-label" style="font-weight: 700;">Project Name / Video Title <span style="color: var(--rose);">*</span></label>
        <input type="text" id="newProjNameSimple" class="form-input" placeholder="e.g. Stickman Epic Quest Episode 1" style="font-size: 14px; padding: 10px 14px;" />
      </div>

      <div class="form-group" style="margin-bottom: 22px;">
        <label class="form-label">Voiceover Audio File (Optional)</label>
        <input type="file" id="newProjVoiceSimple" accept="audio/*" class="form-input" onchange="handleSimpleVoiceFile(this)" />
        <div id="newProjVoiceSimpleStatus" class="file-picked-chip" style="display: none; margin-top: 8px;"></div>
      </div>

      <div style="display: flex; justify-content: flex-end; gap: 10px; border-top: 1px solid var(--border-subtle); padding-top: 16px;">
        <button type="button" class="btn btn-secondary" onclick="closeNewProjectModal()" style="padding: 9px 18px;">Cancel</button>
        <button type="button" class="btn btn-primary" onclick="submitSimpleNewProject()" style="padding: 9px 24px; font-weight: 800; font-size: 13.5px; box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);">
          + Create Project &amp; Open Step 1
        </button>
      </div>
    </div>
  </div>

  """

text = text[:idx1] + simple_modal_html + text[idx2:]

with open(r'E:\stickman-video-automation\studio\public\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: Simplified New Project Modal in index.html!")
