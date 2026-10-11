import json

with open('E:/stickman-video-automation/extensions/veo-automation-with Mbmirza/manifest.json', 'r', encoding='utf-8') as f:
    veo_m = json.load(f)
print("=== VEO MANIFEST ===")
print("name:", veo_m.get("name"))
print("action:", veo_m.get("action"))
print("side_panel:", veo_m.get("side_panel"))
print("content_scripts:", veo_m.get("content_scripts"))
print("background:", veo_m.get("background"))
print("permissions:", veo_m.get("permissions"))

with open('E:/stickman-video-automation/extensions/meta automation/manifest.json', 'r', encoding='utf-8') as f:
    meta_m = json.load(f)
print("\n=== META MANIFEST ===")
print("name:", meta_m.get("name"))
print("action:", meta_m.get("action"))
print("side_panel:", meta_m.get("side_panel"))
print("content_scripts:", meta_m.get("content_scripts"))
print("background:", meta_m.get("background"))
print("permissions:", meta_m.get("permissions"))
