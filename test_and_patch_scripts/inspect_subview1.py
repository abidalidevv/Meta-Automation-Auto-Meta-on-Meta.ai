with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

sub1_start = text.find('id="subViewMode1"')
sub2_start = text.find('id="subViewMode2"')
subQ_start = text.find('id="subViewPromptsQueue"')

print('--- SUBVIEW MODE 1 (CLEAN PROMPT LIST IMPORTER) ---')
print(text[sub1_start:sub1_start+1500].encode('ascii', 'replace').decode('ascii'))
