import urllib.request

resp = urllib.request.urlopen("http://127.0.0.1:45450/")
html = resp.read().decode('utf-8')
print("Length of HTML served by server:", len(html))

idx = html.find('app_v2.js')
print("Script tag in served HTML:", html[idx-30:idx+50])
