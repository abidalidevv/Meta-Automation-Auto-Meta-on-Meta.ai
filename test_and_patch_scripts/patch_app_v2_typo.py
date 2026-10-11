with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """      showToast(data.message, 'success');
      await loadWorkersStatus();
      await loadWorkersProcesses();
      await loadFleetCalculation();"""

replacement = """      showToast(data.message, 'success');
      if (typeof refreshWorkers === 'function') await refreshWorkers();
      if (typeof refreshFleetStatus === 'function') await refreshFleetStatus();
      if (typeof loadFleetCalculation === 'function') await loadFleetCalculation();"""

if target in text:
    text = text.replace(target, replacement)
    with open(r'E:\stickman-video-automation\studio\public\app_v2.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: app_v2.js line 240 patched!")
else:
    print("TARGET NOT FOUND in app_v2.js!")
