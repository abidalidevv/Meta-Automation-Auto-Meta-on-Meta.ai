with open(r'E:\stickman-video-automation\extensions\meta automation\src\ui\side-panel\bridge-client.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
print(f"Total lines: {len(lines)}")
for i in range(0, min(150, len(lines))):
    print(f"{i+1}: {lines[i]}")
