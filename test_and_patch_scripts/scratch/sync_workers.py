import os
import shutil

workers_root = 'E:/stickman-video-automation/Workers'
meta_src = 'E:/stickman-video-automation/extensions/meta automation'
flow_src = 'E:/stickman-video-automation/extensions/veo-automation-with Mbmirza'

if os.path.exists(workers_root):
    for w in os.listdir(workers_root):
        w_dir = os.path.join(workers_root, w)
        ext_dir = os.path.join(w_dir, 'extension')
        if os.path.exists(ext_dir):
            # Check worker provider or config
            cfg_file = os.path.join(ext_dir, 'worker-config.js')
            is_meta = False
            if os.path.exists(os.path.join(ext_dir, 'assets/index.ts-BqblPwcc.js')):
                is_meta = True
            
            src = meta_src if is_meta else flow_src
            print(f"Syncing {w} extension from {src}...")
            # Copy service-worker-loader.js and bridge-client.js
            shutil.copy2(os.path.join(src, 'service-worker-loader.js'), os.path.join(ext_dir, 'service-worker-loader.js'))
            shutil.copy2(os.path.join(src, 'src/ui/side-panel/bridge-client.js'), os.path.join(ext_dir, 'src/ui/side-panel/bridge-client.js'))
            print(f"Synced {w}!")
print("All worker profile extensions synchronized.")
