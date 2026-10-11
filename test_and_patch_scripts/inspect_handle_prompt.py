bridge_path = r'c:\Users\Ali\Desktop\meta automation\src\ui\side-panel\bridge-client.js'
with open(bridge_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function handlePromptGeneration(job)')
print(text[pos:pos+2200])
