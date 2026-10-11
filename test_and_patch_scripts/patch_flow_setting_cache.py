import os

target = 'c([["mode",t.mode],["aspectRatio",t.aspectRatio],["model",t.model],["outputCount",t.outputCount]])'
replacement = 'c([["mode",t.mode],["aspectRatio",t.aspectRatio],["model",t.model],["outputCount",t.outputCount]],!0)'

def patch_flow_ext(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping (not found): {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if target in content:
        new_content = content.replace(target, replacement, 1)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully patched {file_path}")
    elif replacement in content:
        print(f"Already patched {file_path}")
    else:
        print(f"Target pattern not found in {file_path}")

# 1. Base extension in extensions folder
base_path = r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\assets\index.ts-D1zBd6hg.js'
patch_flow_ext(base_path)

# 2. Worker copies for odd workers (Flow: W01, W03, W05, W07, W09)
workers_base = r'E:\stickman-video-automation\Workers'
for i in [1, 3, 5, 7, 9]:
    w_file = os.path.join(workers_base, f"Worker-W{i:02d}", "extension", "assets", "index.ts-D1zBd6hg.js")
    patch_flow_ext(w_file)

print("Flow extension patch complete!")
