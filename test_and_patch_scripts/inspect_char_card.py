with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

sub2_start = text.find('Character Consistency & Visual Reference Card')
if sub2_start == -1:
    sub2_start = text.find('Character')
print(text[sub2_start:sub2_start+2000].encode('ascii', 'replace').decode('ascii'))
