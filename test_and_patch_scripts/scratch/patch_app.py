filepath = 'E:/stickman-video-automation/studio/public/app_v2.js'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

target = "showToast(`Validation error: ${(data.errors || []).join(', ')}`, 'error');"
replacement = "const errMsg = (data.errors && data.errors.length) ? data.errors.join(', ') : (data.error || 'Failed to import prompts'); showToast(`Validation error: ${errMsg}`, 'error');"

if target in text:
    text = text.replace(target, replacement)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: app_v2.js updated!")
else:
    print("WARNING: target not found!")
