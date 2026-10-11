with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure all toolTab-effects do NOT have active
text = text.replace('class="tools-tab-btn active" id="toolTab-effects"', 'class="tools-tab-btn" id="toolTab-effects"')
# Make sure all toolTab-captions HAVE active
text = text.replace('class="tools-tab-btn" id="toolTab-captions"', 'class="tools-tab-btn active" id="toolTab-captions"')
# Make sure tabContent-effects is hidden
text = text.replace('<div class="tools-tab-content" id="tabContent-effects">', '<div class="tools-tab-content" id="tabContent-effects" style="display: none;">')
# Make sure tabContent-captions is visible
text = text.replace('<div class="tools-tab-content" id="tabContent-captions" style="display: none;">', '<div class="tools-tab-content" id="tabContent-captions" style="display: flex;">')

with open(r'E:\stickman-video-automation\studio\public\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully ensured Captions tab is active and visible in all occurrences in index.html!')
