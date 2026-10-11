with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

sub1_start = text.find('id="subViewMode1"')
sub2_start = text.find('id="subViewMode2"')

print(text[sub1_start:sub2_start].encode('ascii', 'replace').decode('ascii'))
