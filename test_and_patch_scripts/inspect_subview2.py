with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

sub2_start = text.find('id="subViewMode2"')
sub2_end = text.find('id="subViewPromptsQueue"')

print(text[sub2_start:sub2_start+2000].encode('ascii', 'replace').decode('ascii'))
