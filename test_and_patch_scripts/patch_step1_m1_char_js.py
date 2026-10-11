with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Add step1M1Char functions right after handleModalCharImage
idx = text.find('function handleModalPromptFile')
new_funcs = """let step1M1CharBase64 = null;

function handleStep1M1CharImage(input) {
  if (input.files && input.files[0]) {
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      step1M1CharBase64 = e.target.result;
      const thumb = document.getElementById('step1M1CharThumb');
      const placeholder = document.getElementById('step1M1CharPlaceholder');
      const removeBtn = document.getElementById('step1M1CharRemoveBtn');
      const statusText = document.getElementById('step1M1CharStatusText');

      if (thumb) {
        thumb.src = e.target.result;
        thumb.style.display = 'block';
      }
      if (placeholder) placeholder.style.display = 'none';
      if (removeBtn) removeBtn.style.display = 'inline-flex';
      if (statusText) {
        statusText.innerHTML = `<strong style="color: var(--emerald);">✓ Reference Loaded:</strong> ${file.name}`;
      }
      showToast(`Character reference loaded: ${file.name}`, 'success');
    };
    reader.readAsDataURL(file);
  }
}

function removeStep1M1CharImage() {
  step1M1CharBase64 = null;
  const fileInput = document.getElementById('step1M1CharFile');
  if (fileInput) fileInput.value = '';
  const thumb = document.getElementById('step1M1CharThumb');
  const placeholder = document.getElementById('step1M1CharPlaceholder');
  const removeBtn = document.getElementById('step1M1CharRemoveBtn');
  const statusText = document.getElementById('step1M1CharStatusText');

  if (thumb) {
    thumb.src = '';
    thumb.style.display = 'none';
  }
  if (placeholder) placeholder.style.display = 'flex';
  if (removeBtn) removeBtn.style.display = 'none';
  if (statusText) statusText.textContent = 'Pick reference image to lock character appearance across all scenes';
  showToast('Character reference removed', 'info');
}

"""

if idx != -1:
    text = text[:idx] + new_funcs + text[idx:]

# In window.startMode1Generating, save character reference if provided
target_gen = "  // 2. Verify project has prompts in queue"
char_save_code = """  // Save Mode 1 character reference if provided
  const charNameEl = document.getElementById('step1M1CharName');
  const charDescEl = document.getElementById('step1M1CharDesc');
  const charName = charNameEl ? charNameEl.value.trim() : 'Main Stickman';
  const charDesc = charDescEl ? charDescEl.value.trim() : '';

  if (step1M1CharBase64 || charDesc) {
    try {
      await fetch(`/api/v1/projects/${pId}/character-reference`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          character_name: charName,
          character_description: charDesc,
          image_base64: step1M1CharBase64
        })
      });
      console.log('Step 1 Mode 1 character reference saved successfully');
    } catch (cErr) {
      console.warn('Saving character reference error:', cErr);
    }
  }

  // 2. Verify project has prompts in queue"""

if target_gen in text:
    text = text.replace(target_gen, char_save_code)

with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: Added Step 1 Mode 1 character reference handlers and saving to app_v2.js!")
