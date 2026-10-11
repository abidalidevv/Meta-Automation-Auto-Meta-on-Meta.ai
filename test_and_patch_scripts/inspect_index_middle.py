with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("Around 163000 to 163200:")
print(text[163000:163250].encode('ascii', 'replace').decode('ascii'))
