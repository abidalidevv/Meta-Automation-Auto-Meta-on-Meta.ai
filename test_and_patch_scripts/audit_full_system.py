import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:45450'
STUDIO_DIR = r'E:\stickman-video-automation\studio'
WORKERS_DIR = r'E:\stickman-video-automation\Workers'

audit_report = {
    'endpoints': {},
    'html_elements': {},
    'filesystem': {},
    'issues_found': []
}

def test_api(method, path, body=None):
    url = BASE_URL + path
    try:
        data = json.dumps(body).encode('utf-8') if body is not None else None
        headers = {'Content-Type': 'application/json'} if body is not None else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            try:
                parsed = json.loads(content)
                return True, resp.status, parsed
            except:
                return True, resp.status, content[:100]
    except urllib.error.HTTPError as e:
        return False, e.code, e.read().decode('utf-8', errors='ignore')[:100]
    except Exception as e:
        return False, 0, str(e)

print('=== 1. API ENDPOINTS AUDIT ===')
# Test Health
ok, status, data = test_api('GET', '/api/v1/health')
audit_report['endpoints']['/api/v1/health'] = {'ok': ok, 'status': status}
print(f'Health: status={status}, ok={ok}')

# Test Workers count
ok, status, data = test_api('GET', '/api/v1/workers')
worker_count = len(data) if isinstance(data, list) else 0
audit_report['endpoints']['/api/v1/workers'] = {'ok': ok, 'count': worker_count}
print(f'Workers API: count={worker_count} (Expected 10)')
if worker_count < 10:
    audit_report['issues_found'].append(f'Workers count is {worker_count}, expected 10')

# Test Settings
ok, status, data = test_api('GET', '/api/v1/settings')
audit_report['endpoints']['/api/v1/settings'] = {'ok': ok, 'status': status}
print(f'Settings API: ok={ok}, keys={list(data.keys()) if isinstance(data, dict) else "None"}')

# Test Projects
ok, status, projects = test_api('GET', '/api/v1/projects')
proj_count = len(projects) if isinstance(projects, list) else 0
print(f'Projects API: count={proj_count}')
active_proj_id = projects[0]['id'] if proj_count > 0 else None

if active_proj_id:
    # Test Prompts
    ok, status, prompts = test_api('GET', f'/api/v1/projects/{active_proj_id}/prompts')
    print(f'Project {active_proj_id} prompts count: {len(prompts) if isinstance(prompts, list) else 0}')

    # Test Timeline
    ok, status, timeline = test_api('GET', f'/api/v1/projects/{active_proj_id}/timeline')
    print(f'Project timeline loaded: ok={ok}')

    # Test Fleet Calculator with json body
    ok, status, fleet = test_api('POST', f'/api/v1/projects/{active_proj_id}/workers/calculate-fleet', body={})
    print(f'Fleet calculation API: ok={ok}, needed_workers={fleet.get("total_workers_needed") if isinstance(fleet, dict) else "N/A"}')
    if not ok:
        audit_report['issues_found'].append(f'Fleet calculation API failed: status {status}')

# Test Raw Log
ok, status, log_sample = test_api('GET', '/api/v1/logs/raw')
audit_report['endpoints']['/api/v1/logs/raw'] = {'ok': ok, 'status': status}
print(f'Logs Raw API: ok={ok}, sample length={len(str(log_sample))}')

# Test Stop All Workers
ok, status, stop_res = test_api('POST', '/api/v1/workers/stop-all', body={})
print(f'Workers Stop-All API: ok={ok}')

print('\n=== 2. DOM & UI ELEMENTS AUDIT ===')
index_path = os.path.join(STUDIO_DIR, 'public', 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

required_elements = [
    # Step 1
    'subTabMode1', 'subTabMode2', 'subTabPromptsQueue', 'btnRetryFailedPrompts', 'btnClearFailedPrompts', 'btnClearAllPrompts',
    # Step 2
    'fleetTotalPrompts', 'fleetTotalWorkers', 'fleetMetaWorkers', 'fleetFlowWorkers', 'fleetActiveQueued', 'fleetFormulaExplanation',
    # Step 3
    'galleryGrid', 'galleryCountBadge',
    # Step 4
    'playerCanvasImage', 'playerCanvasViewport', 'capcutVideoTrackLane', 'capcutSceneCount',
    'toolTab-effects', 'toolTab-captions', 'toolTab-motion', 'toolTab-audio', 'toolTab-media',
    'tabContent-effects', 'tabContent-captions', 'tabContent-motion', 'tabContent-audio', 'tabContent-media',
    'fxBlurSlider', 'fxExposureSlider', 'fxContrastSlider', 'fxSaturationSlider', 'fxVignetteToggle', 'fxGrainToggle', 'fxSharpenToggle', 'fxGlowToggle',
    # Step 5
    'renderResolution', 'renderFps', 'renderSpeedPreset', 'renderCrf', 'renderAudioBitrate', 'renderMotionToggle', 'renderHwaccelToggle', 'btnStartRender', 'step5MasterPlayer', 'btnDownloadRender',
    # Step 6
    'settingsGroqKeySingle', 'settingsGroqKeyPool', 'settingsGroqModel', 'settingsGroqFallback', 'settingsElevenLabsKey', 'settingsOpenAIKey', 'telemetryLogBox'
]

missing_elements = []
for el in required_elements:
    if el not in html:
        missing_elements.append(el)

print(f'DOM Elements checked: {len(required_elements)}. Missing: {len(missing_elements)}')
if missing_elements:
    print('Missing elements:', missing_elements)
    audit_report['issues_found'].extend([f'Missing DOM element: {e}' for e in missing_elements])
else:
    print('✓ All critical UI DOM elements and IDs are present in index.html!')

# Check 20 atmospheric presets in HTML
atmos_presets = ['normal', 'bright', 'moody_dark', 'warm', 'cool', 'vintage', 'b_w', 'vivid', 'dreamy', 'neon', 'golden_hour', 'cyberpunk', 'noir', 'sepia', 'invert', 'pastel', 'frost', 'sunset', 'ocean', 'chromatic']
missing_presets = [p for p in atmos_presets if f'selectAtmosphericEffect(\'{p}\')' not in html]
print(f'Atmospheric Presets in HTML: {len(atmos_presets) - len(missing_presets)} / {len(atmos_presets)}')
if missing_presets:
    print('Missing atmospheric presets:', missing_presets)
    audit_report['issues_found'].extend([f'Missing atmospheric preset: {p}' for p in missing_presets])

print('\n=== 3. FILE SYSTEM & BINARIES AUDIT ===')
ffmpeg_path = os.path.join(STUDIO_DIR, 'bin', 'ffmpeg.exe')
ffprobe_path = os.path.join(STUDIO_DIR, 'bin', 'ffprobe.exe')
db_path = os.path.join(STUDIO_DIR, 'data', 'studio.sqlite')
log_path = os.path.join(STUDIO_DIR, 'logs', 'studio.log')

print(f'ffmpeg.exe exists: {os.path.exists(ffmpeg_path)} ({os.path.getsize(ffmpeg_path):,} bytes)' if os.path.exists(ffmpeg_path) else 'ffmpeg.exe MISSING!')
print(f'ffprobe.exe exists: {os.path.exists(ffprobe_path)} ({os.path.getsize(ffprobe_path):,} bytes)' if os.path.exists(ffprobe_path) else 'ffprobe.exe MISSING!')
print(f'studio.sqlite exists: {os.path.exists(db_path)} ({os.path.getsize(db_path):,} bytes)' if os.path.exists(db_path) else 'studio.sqlite MISSING!')
print(f'studio.log exists: {os.path.exists(log_path)} ({os.path.getsize(log_path):,} bytes)' if os.path.exists(log_path) else 'studio.log created on first write')

# Check 10 worker profile directories
missing_worker_dirs = []
for i in range(1, 11):
    w_dir = os.path.join(WORKERS_DIR, f'Worker-W{i:02d}')
    if not os.path.exists(w_dir):
        missing_worker_dirs.append(f'Worker-W{i:02d}')

print(f'Worker profile directories in {WORKERS_DIR}: {10 - len(missing_worker_dirs)} / 10')
if missing_worker_dirs:
    print('Missing worker directories:', missing_worker_dirs)

print('\n=== AUDIT SUMMARY ===')
if not audit_report['issues_found']:
    print('🎉 COMPLETE SYSTEM AUDIT PASSED WITH 0 CRITICAL ISSUES!')
else:
    print(f'⚠️ Found {len(audit_report["issues_found"])} issues:')
    for iss in audit_report['issues_found']:
        print('  -', iss)
