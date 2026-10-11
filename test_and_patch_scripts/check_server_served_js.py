import urllib.request

resp = urllib.request.urlopen("http://127.0.0.1:45450/app_v2.js?v=2.2")
content = resp.read().decode('utf-8')
lines = content.splitlines()
print(f"Total lines returned by server for app_v2.js: {len(lines)}")
for i in range(185, 205):
    print(f"{i+1}: {repr(lines[i])}")
