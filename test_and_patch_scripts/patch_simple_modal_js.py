with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

simple_code = """
// Simple New Project Modal Handler
let simpleVoiceFile = null;

function handleSimpleVoiceFile(input) {
  if (input.files && input.files[0]) {
    simpleVoiceFile = input.files[0];
    const status = document.getElementById('newProjVoiceSimpleStatus');
    if (status) {
      status.style.display = 'inline-flex';
      status.innerHTML = `<strong style="color: var(--emerald);">✓ Voiceover ready:</strong> ${simpleVoiceFile.name}`;
    }
  }
}

async function submitSimpleNewProject() {
  const nameInput = document.getElementById('newProjNameSimple');
  const name = nameInput ? nameInput.value.trim() : '';

  if (!name) {
    showToast('Please enter a Project Name / Video Title', 'warn');
    return;
  }

  try {
    showToast('Creating production project...', 'info');
    const res = await fetch('/api/v1/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        mode: 'MODE_1',
        voiceover_path: simpleVoiceFile ? simpleVoiceFile.name : null
      })
    });
    const created = await res.json();
    if (created.id) {
      if (simpleVoiceFile) {
        const formData = new FormData();
        formData.append('audio', simpleVoiceFile);
        formData.append('track_type', 'VOICEOVER');
        await fetch(`/api/v1/projects/${created.id}/audio/upload`, { method: 'POST', body: formData }).catch(console.error);
      }

      showToast(`Project created: ${created.name}`, 'success');
      closeNewProjectModal();
      if (nameInput) nameInput.value = '';
      simpleVoiceFile = null;
      await loadProjects();
      await onSelectProject(created.id);
      goToStep(1);
    } else {
      showToast(created.error || 'Failed to create project', 'error');
    }
  } catch (err) {
    showToast(`Error creating project: ${err.message}`, 'error');
  }
}

window.submitSimpleNewProject = submitSimpleNewProject;
window.handleSimpleVoiceFile = handleSimpleVoiceFile;
"""

# Append to end of app_v2.js
text = text + "\n" + simple_code

with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: Added simple modal handlers to app_v2.js!")
