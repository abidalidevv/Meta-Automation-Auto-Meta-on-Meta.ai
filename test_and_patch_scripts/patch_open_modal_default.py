with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace switchNewProjectModalTab('MODE_1') with switchNewProjectModalTab('MODE_2') in openNewProjectModal
text = text.replace(
    "switchNewProjectModalTab('MODE_1');\n\n  // Pre-load default master prompt",
    "switchNewProjectModalTab('MODE_2');\n\n  // Pre-load default master prompt"
)

with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated openNewProjectModal in app_v2.js!")
