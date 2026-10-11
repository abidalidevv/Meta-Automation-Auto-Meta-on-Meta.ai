with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Swap MODE 1 <-> MODE 2 labels ONLY in the New Project Modal
# The modal tab buttons
text = text.replace(
    'id="tabNewProjMode1" class="modal-tab-btn active" onclick="switchNewProjectModalTab(\'MODE_1\')"',
    'id="tabNewProjMode1" class="modal-tab-btn active" onclick="switchNewProjectModalTab(\'MODE_1\')" data-swapped="true"'
)

# Swap tab button text
old_tab1 = '''id="tabNewProjMode1" class="modal-tab-btn active" onclick="switchNewProjectModalTab('MODE_1')" data-swapped="true">
          MODE 1'''
new_tab1 = '''id="tabNewProjMode1" class="modal-tab-btn active" onclick="switchNewProjectModalTab('MODE_1')">
          MODE 2'''

old_tab2 = '''id="tabNewProjMode2" class="modal-tab-btn" onclick="switchNewProjectModalTab('MODE_2')">
          MODE 2'''
new_tab2 = '''id="tabNewProjMode2" class="modal-tab-btn" onclick="switchNewProjectModalTab('MODE_2')">
          MODE 1'''

text = text.replace(old_tab1, new_tab1)
text = text.replace(old_tab2, new_tab2)

with open(r'E:\stickman-video-automation\studio\public\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# Verify
with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    check = f.read()

idx = check.find('tabNewProjMode1')
print('Modal tab buttons after change:')
print(check[idx:idx+500].encode('ascii', 'replace').decode('ascii'))
