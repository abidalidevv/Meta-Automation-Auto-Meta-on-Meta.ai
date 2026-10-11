with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('</html>')
if idx != -1:
    clean_html = text[:idx + 7] + '\n'
    with open(r'E:\stickman-video-automation\studio\public\index.html', 'w', encoding='utf-8') as f:
        f.write(clean_html)
    print(f"SUCCESS: Trimmed index.html cleanly at </html>! New length: {len(clean_html):,} chars (was {len(text):,} chars)")
else:
    print("ERROR: </html> not found!")
