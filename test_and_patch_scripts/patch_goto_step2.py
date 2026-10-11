with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """      // Auto-navigate to Step 3 (Workers Farm) to monitor live progress
      if (typeof goToStep === 'function') {
        goToStep(3);
      }"""

replacement = """      // Auto-navigate to Step 2 (Workers Farm) to monitor live progress
      if (typeof goToStep === 'function') {
        goToStep(2);
      }"""

if target in text:
    text = text.replace(target, replacement)
    with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: goToStep(3) replaced with goToStep(2) in app_v2.js!")
else:
    print("TARGET NOT FOUND in app_v2.js")
