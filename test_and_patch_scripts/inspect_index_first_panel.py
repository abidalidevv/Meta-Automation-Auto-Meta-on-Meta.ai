with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("Around 34700 to 35000:")
print(text[34700:35000].encode('ascii', 'replace').decode('ascii'))
