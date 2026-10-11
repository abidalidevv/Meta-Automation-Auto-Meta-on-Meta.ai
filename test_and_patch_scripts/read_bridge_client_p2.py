with open(r'E:\stickman-video-automation\extensions\meta automation\src\ui\side-panel\bridge-client.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(150, min(300, len(lines))):
    print(f"{i+1}: {lines[i]}")
