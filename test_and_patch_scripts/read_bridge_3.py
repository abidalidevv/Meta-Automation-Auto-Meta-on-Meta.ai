with open('E:/stickman-video-automation/extensions/veo-automation-with Mbmirza/src/ui/side-panel/bridge-client.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[250:370]):
    print(f"{i+251}: {line}", end='')
