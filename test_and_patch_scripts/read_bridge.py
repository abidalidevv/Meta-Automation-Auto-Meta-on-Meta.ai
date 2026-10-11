with open('E:/stickman-video-automation/extensions/veo-automation-with Mbmirza/src/ui/side-panel/bridge-client.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in bridge-client.js: {len(lines)}")
for i, line in enumerate(lines[:120]):
    print(f"{i+1}: {line}", end='')
