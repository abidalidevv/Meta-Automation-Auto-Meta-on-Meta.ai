import os
import sys

doc_path = r'E:\stickman-video-automation\studio\public\documentation.html'
with open(doc_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Check for Step 6 section
idx = code.find('id="step6"')
if idx == -1:
    idx = code.find('id="step-6"')

print("Step 6 section index:", idx)
if idx != -1:
    print(code[idx:idx+1500])
