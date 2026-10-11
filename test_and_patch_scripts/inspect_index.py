with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

sub2_idx = text.find('id="subViewMode2"')
queue_idx = text.find('id="subViewQueue"')
step2_idx = text.find('id="step-2-panel"')

print(f"subViewMode2 start: {sub2_idx}")
print(f"subViewQueue start: {queue_idx}")
print(f"step-2-panel start: {step2_idx}")

# Print subViewMode2 block
print("\n--- subViewMode2 snippet ---")
print(text[sub2_idx:sub2_idx+600].encode('ascii', errors='replace').decode('ascii'))

# Print subViewQueue block
print("\n--- subViewQueue snippet ---")
print(text[queue_idx:queue_idx+600].encode('ascii', errors='replace').decode('ascii'))
