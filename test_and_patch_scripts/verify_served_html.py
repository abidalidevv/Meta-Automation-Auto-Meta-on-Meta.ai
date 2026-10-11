import urllib.request

html = urllib.request.urlopen('http://127.0.0.1:45450/index.html').read().decode('utf-8', errors='ignore')
checks = {
    'Mode 1 character reference box added': 'step1M1CharThumbBox' in html,
    'Simple new project modal added': 'newProjNameSimple' in html,
    'No trailing junk after html': html.count('</html>') == 1,
    'Single step-2-panel': html.count('id="step-2-panel"') == 1
}

for k, v in checks.items():
    print(f"[{'PASS' if v else 'FAIL'}] {k}")
