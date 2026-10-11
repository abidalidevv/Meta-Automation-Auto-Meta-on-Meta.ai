index_path = r'E:\stickman-video-automation\studio\public\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'button type="button" class="btn btn-secondary" onclick="retryFailedPrompts()"',
    'button type="button" id="btnRetryFailedPrompts" class="btn btn-secondary" onclick="retryFailedPrompts()"'
)
c = c.replace(
    'button type="button" class="btn btn-secondary" onclick="clearFailedPrompts()"',
    'button type="button" id="btnClearFailedPrompts" class="btn btn-secondary" onclick="clearFailedPrompts()"'
)
c = c.replace(
    'button type="button" class="btn btn-secondary" onclick="clearAllPromptsQueue()"',
    'button type="button" id="btnClearAllPrompts" class="btn btn-secondary" onclick="clearAllPromptsQueue()"'
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Added explicit button IDs successfully')
