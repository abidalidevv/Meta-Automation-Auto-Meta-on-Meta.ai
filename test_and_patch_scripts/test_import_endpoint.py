import urllib.request
import json

base = 'http://127.0.0.1:45450/api/v1'

# Case A: Only prompt 001 (as seen in the screenshot)
text_case_a = "001_Clean premium 2D educational stickman illustration, matching the supplied reference style: simple white/light-cream background, thin hand-drawn black outlines, round white stickman head, very expressive eyes and face, extremely simple thin black body/limbs, flat muted blue, green, tan and pale yellow accents, minimal objects, subtle clean shadows, no gradients, no photorealism, no text, no labels, no watermark, consistent character proportions and line weight, cinematic 16:9 composition, clear readable silhouette, professional YouTube documentary visual. Scene: A person standing on a freezing high-Andes plateau at roughly 4,000 meters, vast rocky mountains behind him, visibly thin air."

req = urllib.request.Request(
    f"{base}/projects/proj_1790606377967_16ls/prompts/import",
    data=json.dumps({"raw_prompts": text_case_a}).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)

try:
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('utf-8'))
    print("Case A result:", data)
except urllib.error.HTTPError as e:
    err_body = e.read().decode('utf-8')
    print("Case A error status:", e.code, "Body:", err_body)
except Exception as ex:
    print("Case A exception:", ex)
