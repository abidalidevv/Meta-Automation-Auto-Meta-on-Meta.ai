bridge_path = r'c:\Users\Ali\Desktop\meta automation\src\ui\side-panel\bridge-client.js'
with open(bridge_path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function pollNextJob()')
if pos == -1:
    pos = text.find('pollNextJob')
print(text[pos-100:pos+1200])
