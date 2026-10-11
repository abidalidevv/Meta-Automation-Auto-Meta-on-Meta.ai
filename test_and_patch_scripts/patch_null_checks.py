import sys
sys.stdout.reconfigure(encoding='utf-8')

app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix switchStep1SubTab with safe null checks
old_switch = """function switchStep1SubTab(tab) {
  document.getElementById('subTabMode1').classList.remove('active');
  document.getElementById('subTabMode2').classList.remove('active');
  document.getElementById('subTabPromptsQueue').classList.remove('active');

  document.getElementById('subViewMode1').style.display = 'none';
  document.getElementById('subViewMode2').style.display = 'none';
  document.getElementById('subViewQueue').style.display = 'none';

  if (tab === 'mode1') {
    document.getElementById('subTabMode1').classList.add('active');
    document.getElementById('subViewMode1').style.display = 'block';
  } else if (tab === 'mode2') {
    document.getElementById('subTabMode2').classList.add('active');
    document.getElementById('subViewMode2').style.display = 'block';
  } else if (tab === 'queue') {
    document.getElementById('subTabPromptsQueue').classList.add('active');
    document.getElementById('subViewQueue').style.display = 'block';
    loadProjectPrompts();
  }
}"""

new_switch = """function switchStep1SubTab(tab) {
  const t1 = document.getElementById('subTabMode1');
  const t2 = document.getElementById('subTabMode2');
  const tQ = document.getElementById('subTabPromptsQueue');
  const v1 = document.getElementById('subViewMode1');
  const v2 = document.getElementById('subViewMode2');
  const vQ = document.getElementById('subViewQueue');

  if (t1) t1.classList.remove('active');
  if (t2) t2.classList.remove('active');
  if (tQ) tQ.classList.remove('active');

  if (v1) v1.style.display = 'none';
  if (v2) v2.style.display = 'none';
  if (vQ) vQ.style.display = 'none';

  if (tab === 'mode1') {
    if (t1) t1.classList.add('active');
    if (v1) v1.style.display = 'block';
  } else if (tab === 'mode2') {
    if (t2) t2.classList.add('active');
    if (v2) v2.style.display = 'block';
  } else if (tab === 'queue') {
    if (tQ) tQ.classList.add('active');
    if (vQ) vQ.style.display = 'block';
    loadProjectPrompts();
  }
}"""

if old_switch in code:
    code = code.replace(old_switch, new_switch)
    print("Fixed switchStep1SubTab")
else:
    print("Could not find exact old switchStep1SubTab string")

# 2. Fix promptsCountBadge in loadProjectPrompts
code = code.replace(
    "document.getElementById('promptsCountBadge').textContent = `${prompts.length} Prompts`;",
    "const pBadge = document.getElementById('promptsCountBadge'); if (pBadge) pBadge.textContent = `${prompts.length} Prompts`;"
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app_v2.js with safe null checks!")
