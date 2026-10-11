import os
import sys

app_path = r'E:\stickman-video-automation\studio\public\app_v2.js'
with open(app_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    "if (stepNum === 6) { fetchLogs(); loadSettings(); }",
    "if (stepNum === 6) { fetchLogs(); loadSettings(); refreshFleetStatus(); }"
)

code = code.replace(
    "loadDefaultMasterPrompt();\n}",
    "loadDefaultMasterPrompt();\n  loadSettings();\n  refreshFleetStatus();\n}"
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated goToStep and initApp to call refreshFleetStatus() and loadSettings()')
