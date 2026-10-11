import os
import re

with open(r'E:\stickman-video-automation\studio\public\index.html', 'r', encoding='utf-8') as f:
    code = f.read()

matches = re.findall(r'id=["\'](fleet[^"\']*)["\']', code)
print('Fleet IDs in index.html:', matches)
