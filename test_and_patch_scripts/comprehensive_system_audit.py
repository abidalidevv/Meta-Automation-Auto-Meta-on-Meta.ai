import urllib.request
import urllib.error
import json
import os
import re

print("=====================================================================")
print("   STICKMAN STUDIO V2 - FULL COMPREHENSIVE 6-STEP SYSTEM AUDIT")
print("=====================================================================")

BASE_URL = "http://127.0.0.1:45450/api/v1"
INDEX_PATH = r"E:\stickman-video-automation\studio\public\index.html"
APP_JS_PATH = r"E:\stickman-video-automation\studio\public\app_v2.js"
ROUTES_PATH = r"E:\stickman-video-automation\studio\server\routes.js"

audit_report = {
    "endpoints": {"passed": 0, "failed": 0, "details": []},
    "dom_elements": {"passed": 0, "failed": 0, "missing": []},
    "js_functions": {"passed": 0, "failed": 0, "missing": []},
    "database": {"passed": 0, "failed": 0, "details": []},
    "workers": {"passed": 0, "failed": 0, "details": []}
}

# 1. Audit API Endpoints
endpoints_to_test = [
    ("GET", "/health", None, 200),
    ("GET", "/workers/fleet-status", None, 200),
    ("GET", "/settings", None, 200),
    ("GET", "/logs/raw", None, 200),
    ("GET", "/ai/models", None, 200),
    ("GET", "/projects", None, 200),
]

print("\n--- 1. Testing Core REST Endpoints ---")
for method, ep, payload, expected_status in endpoints_to_test:
    url = f"http://127.0.0.1:45450{ep}" if ep == "/health" else f"{BASE_URL}{ep}"
    try:
        req = urllib.request.Request(url, method=method)
        resp = urllib.request.urlopen(req, timeout=5)
        status = resp.getcode()
        if status == expected_status:
            audit_report["endpoints"]["passed"] += 1
            print(f"  [PASS] {method} {ep} -> HTTP {status}")
        else:
            audit_report["endpoints"]["failed"] += 1
            print(f"  [FAIL] {method} {ep} -> Expected {expected_status}, got {status}")
    except Exception as e:
        audit_report["endpoints"]["failed"] += 1
        print(f"  [FAIL] {method} {ep} -> Error: {e}")

# 2. Audit DOM IDs in index.html
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_html = f.read()

essential_dom_ids = [
    # Step 1
    "mode1_clean_prompt_list", "mode2_groq_story", "projectPromptsQueueTab",
    "btnRetryFailedPrompts", "btnClearFailedPrompts", "btnClearAllPrompts",
    # Step 2
    "fleetStatusBadge", "fleetTotalPrompts", "fleetNeededWorkers", "workersLoginAssistantGrid",
    # Step 3
    "projectGalleryGrid", "visualQaStatusBadge",
    # Step 4
    "playerCanvasImage", "playerVideoViewport", "toolsTab_effects", "toolsTab_captions",
    "toolsTab_transitions", "toolsTab_audio", "toolsTab_inspector",
    "filterBlur", "filterExposure", "filterContrast", "filterSaturation", "filterVignette",
    # Step 5
    "renderResolution", "resBadge", "renderFps", "renderSpeedPreset", "renderCrf",
    "renderAudioBitrate", "renderMotionToggle", "renderHwaccelToggle", "btnStartRender",
    "step5MasterPlayer", "step5DownloadBtn", "step5OpenFolderBtn",
    # Step 6
    "settingsGroqKeySingle", "settingsGroqKeyPool", "settingsGroqModel", "settingsGroqFallback",
    "settingsElevenLabsKey", "settingsElevenLabsVoiceId", "settingsOpenAIKey", "settingsOpenAIModel",
    "settingsStabilityKey", "settingsPexelsKey", "telemetryLogBox"
]

print("\n--- 2. Auditing Crucial DOM Elements in index.html ---")
for elem_id in essential_dom_ids:
    if f'id="{elem_id}"' in index_html or f"id='{elem_id}'" in index_html:
        audit_report["dom_elements"]["passed"] += 1
    else:
        audit_report["dom_elements"]["failed"] += 1
        audit_report["dom_elements"]["missing"].append(elem_id)
        print(f"  [MISSING DOM ID] {elem_id}")

print(f"  DOM Elements Checked: {len(essential_dom_ids)} | Passed: {audit_report['dom_elements']['passed']} | Missing: {len(audit_report['dom_elements']['missing'])}")

# 3. Audit JavaScript Event Handler Functions in app_v2.js
with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
    app_js = f.read()

essential_js_functions = [
    "switchToolsTab", "selectAtmosphericEffect", "updateCustomEffectSliders",
    "applyAtmosphericEffectToCanvas", "playSfx", "attachSfxToCurrentScene",
    "selectMotionPreset", "selectTransitionPreset", "triggerRender",
    "onRenderResolutionChange", "openOutputFolder", "refreshFleetStatus",
    "openWorkerLogin", "toggleWorkerProvider", "stopAllWorkers",
    "saveAllSettings", "loadSettings", "testGroqKeyConnection", "fetchLogs"
]

print("\n--- 3. Auditing JavaScript Functions in app_v2.js ---")
for fn in essential_js_functions:
    pattern = rf"(function\s+{fn}|const\s+{fn}\s*=|window\.{fn}\s*=)"
    if re.search(pattern, app_js):
        audit_report["js_functions"]["passed"] += 1
    else:
        audit_report["js_functions"]["failed"] += 1
        audit_report["js_functions"]["missing"].append(fn)
        print(f"  [MISSING JS FUNCTION] {fn}")

print(f"  JS Functions Checked: {len(essential_js_functions)} | Passed: {audit_report['js_functions']['passed']} | Missing: {len(audit_report['js_functions']['missing'])}")

# 4. Audit Worker Fleet State in DB and Profile Dirs
print("\n--- 4. Auditing 10-Worker Isolated Profiles ---")
workers_base = r"E:\stickman-video-automation\Workers"
for i in range(1, 11):
    w_id = f"W{i:02d}"
    w_dir = os.path.join(workers_base, f"Worker-{w_id}")
    ext_dir = os.path.join(w_dir, "extension")
    cfg_file = os.path.join(ext_dir, "worker-config.js")
    exists = os.path.exists(w_dir)
    ext_exists = os.path.exists(ext_dir)
    cfg_exists = os.path.exists(cfg_file)
    
    cfg_content = ""
    if cfg_exists:
        with open(cfg_file, 'r', encoding='utf-8') as f:
            cfg_content = f.read().replace('\n', ' ')

    if exists and ext_exists and cfg_exists:
        audit_report["workers"]["passed"] += 1
        print(f"  [WORKER {w_id} OK] Ext Provisioned | {cfg_content.strip()}")
    else:
        audit_report["workers"]["failed"] += 1
        print(f"  [WORKER {w_id} INCOMPLETE] dir={exists}, ext={ext_exists}, cfg={cfg_exists}")

print("\n=====================================================================")
print(f"   AUDIT SUMMARY:")
print(f"   - Endpoints: {audit_report['endpoints']['passed']} Passed, {audit_report['endpoints']['failed']} Failed")
print(f"   - DOM Elements: {audit_report['dom_elements']['passed']} Passed, {audit_report['dom_elements']['failed']} Failed")
print(f"   - JS Functions: {audit_report['js_functions']['passed']} Passed, {audit_report['js_functions']['failed']} Failed")
print(f"   - 10-Worker Profiles: {audit_report['workers']['passed']}/10 Fully Provisioned")
print("=====================================================================")
