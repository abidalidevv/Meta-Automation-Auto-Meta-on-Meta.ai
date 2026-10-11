index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Patch Mode 1 button
pos1 = text.find('onclick="importRawPrompts()"')
start_div = text.rfind('<div style="display: flex; gap: 12px;">', 0, pos1)
end_div = text.find('</div>', pos1) + 6

old_btn_chunk = text[start_div:end_div]
new_btn_chunk = """<div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                <button type="button" id="btnM1StartGenerating" class="btn btn-emerald" onclick="startMode1Generating()" style="padding: 13px 28px; font-size: 15px; font-weight: 800; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); display: flex; align-items: center; gap: 8px; cursor: pointer;">
                  <span>🚀</span> Start Generating (1-Click Fleet Launch)
                </button>
                <button type="button" class="btn btn-secondary" onclick="importRawPrompts()" style="padding: 13px 20px; font-size: 13px; font-weight: 700; cursor: pointer;">
                  ✔ Validate & Import Only
                </button>
              </div>"""

text = text[:start_div] + new_btn_chunk + text[end_div:]

# 2. Patch Mode 2 output canvas button
pos2 = text.find('proceedFromM1ToWorkerFarm()')
p_start = text.rfind('<button type="button" class="btn btn-primary" onclick="proceedFromM1ToWorkerFarm()"', 0, pos2)
p_end = text.find('</button>', pos2) + 9

old_m2_chunk = text[p_start:p_end]
new_m2_chunk = """<button type="button" class="btn btn-emerald" onclick="startMode1Generating()" style="font-size: 12px; padding: 6px 18px; cursor: pointer; font-weight: 800; box-shadow: 0 0 15px rgba(16, 185, 129, 0.35); display: inline-flex; align-items: center; gap: 6px;">
                      <span>🚀</span> Start Generating Now
                    </button>
                    <button type="button" class="btn btn-primary" onclick="proceedFromM1ToWorkerFarm()" style="font-size: 12px; padding: 6px 16px; cursor: pointer;">
                      → Open Worker Farm →
                    </button>"""

text = text[:p_start] + new_m2_chunk + text[p_end:]

# 3. Patch tools tabs in Step 4
pos_eff = text.find('id="toolTab-effects"')
p_eff_start = text.rfind('<button', 0, pos_eff)
p_eff_end = text.find('</button>', pos_eff) + 9

pos_cap = text.find('id="toolTab-captions"')
p_cap_start = text.rfind('<button', 0, pos_cap)
p_cap_end = text.find('</button>', pos_cap) + 9

# Swap active class
btn_eff = text[p_eff_start:p_eff_end].replace('active', '').replace('  ', ' ')
btn_cap = text[p_cap_start:p_cap_end].replace('class="tools-tab-btn"', 'class="tools-tab-btn active"')

# We replace cap first because it appears after eff
text = text[:p_cap_start] + btn_cap + text[p_cap_end:]
# Now re-find eff and replace
pos_eff2 = text.find('id="toolTab-effects"')
p_eff_start2 = text.rfind('<button', 0, pos_eff2)
p_eff_end2 = text.find('</button>', pos_eff2) + 9
text = text[:p_eff_start2] + btn_eff + text[p_eff_end2:]

# 4. Patch tools tab content: effects hide, captions show
c_eff = text.find('id="tabContent-effects"')
if 'style="display: none;"' not in text[c_eff:c_eff+100]:
    text = text[:c_eff] + 'id="tabContent-effects" style="display: none;"' + text[c_eff+len('id="tabContent-effects"'):]

c_cap = text.find('id="tabContent-captions"')
if 'style="display: none;"' in text[c_cap:c_cap+100]:
    text = text[:c_cap] + 'id="tabContent-captions" style="display: flex;"' + text[c_cap+len('id="tabContent-captions" style="display: none;"'):]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patch applied to index.html successfully!")
