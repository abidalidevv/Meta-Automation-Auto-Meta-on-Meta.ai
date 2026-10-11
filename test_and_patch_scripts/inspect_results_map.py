with open(r'c:\Users\Ali\Desktop\meta automation\assets\index.ts-BdeTBz9V.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('results:e.results.map')
print(text[pos:pos+300])
