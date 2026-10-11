import os
import sys

index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Update Step 5 subtitle in stepper
code = code.replace(
    '<span class="stepper-sub">1080p MP4 Video Pipeline</span>',
    '<span class="stepper-sub">4K Ultra HD & 1080p Pipeline</span>'
)

# Pre-populate workersLoginAssistantGrid
target_empty_grid = '<div id="workersLoginAssistantGrid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 14px; max-height: 380px; overflow-y: auto;">\n              <!-- Dynamic worker cards loaded via refreshFleetStatus() -->\n            </div>'

workers_cards = []
for i in range(1, 11):
    w_id = f"W{i:02d}"
    is_flow = (i % 2 == 1)
    prov = "flow" if is_flow else "meta"
    other_prov = "meta" if is_flow else "flow"
    prov_badge = '<span class="badge" style="background: rgba(0,240,255,0.15); color: var(--cyan); border: 1px solid rgba(0,240,255,0.3); font-size: 10px; font-weight: 800;">⚡ FLOW</span>' if is_flow else '<span class="badge" style="background: rgba(139,92,246,0.15); color: var(--violet); border: 1px solid rgba(139,92,246,0.3); font-size: 10px; font-weight: 800;">🌐 META</span>'
    btn_text = f"🚀 Open {'Flow' if is_flow else 'Meta'} Login"
    
    card = f'''<div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span style="font-family: var(--font-mono); font-weight: 800; font-size: 13px; color: #fff;">{w_id}</span>
                  {prov_badge}
                </div>
                <div style="margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                  <span style="color: var(--emerald); font-size: 10px; font-weight: 700;">🟢 Session Saved</span>
                  <button type="button" class="btn btn-secondary" onclick="toggleWorkerProvider('{w_id}', '{prov}')" title="Switch between Flow and Meta" style="font-size: 9.5px; padding: 2px 6px;">
                    ⇄ {other_prov.upper()}
                  </button>
                </div>
                <button type="button" class="btn btn-secondary" onclick="openWorkerLogin('{w_id}', '{prov}')" style="width: 100%; justify-content: center; font-size: 11px; padding: 5px 8px; font-weight: 700;">
                  {btn_text}
                </button>
              </div>'''
    workers_cards.append(card)

populated_grid = '<div id="workersLoginAssistantGrid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 14px; max-height: 380px; overflow-y: auto;">\n              ' + '\n              '.join(workers_cards) + '\n            </div>'

if target_empty_grid in code:
    code = code.replace(target_empty_grid, populated_grid)
    print("Pre-populated workersLoginAssistantGrid with 10 worker cards!")
else:
    # Try finding by start
    g_start = code.find('<div id="workersLoginAssistantGrid"')
    g_end = code.find('</div>', g_start)
    if g_start != -1 and g_end != -1:
        code = code[:g_start] + populated_grid + code[g_end + len('</div>'):]
        print("Replaced workersLoginAssistantGrid boundaries with 10 worker cards!")
    else:
        print("Could not find workersLoginAssistantGrid!")
        sys.exit(1)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("index.html updated successfully!")
