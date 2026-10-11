with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('lightboxModal')
print(f"Index of lightboxModal: {idx}")
if idx != -1:
    print("Snippet:")
    print(text[max(0, idx-100):min(len(text), idx+400)])
