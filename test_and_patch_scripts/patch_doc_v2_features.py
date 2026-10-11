doc_path = r'E:\stickman-video-automation\studio\public\documentation.html'
with open(doc_path, 'r', encoding='utf-8') as f:
    html = f.read()

new_card = """
<!-- 1-CLICK FLEET LAUNCH, REAL IMAGE THUMBNAIL SERVING & DEFAULT CAPTIONS TAB -->
<div class="card" style="margin-top: 30px; border-left: 5px solid #00f0ff; background: #0f172a; padding: 25px; border-radius: 8px;">
  <h2 style="color: #00f0ff; margin-top: 0;">🚀 1-Click Fleet Launch, Live Image Thumbnail Serving &amp; Default Captions View</h2>
  <p style="color: #cbd5e1;">Resolved usability and visual fidelity requirements identified during live testing of Mode 1 &amp; CapCut studio editor:</p>
  
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 15px; margin-top: 20px;">
    <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
      <h4 style="color: #38bdf8; margin: 0 0 8px 0;">1. 1-Click "Start Generating" Automation</h4>
      <p style="color: #94a3b8; font-size: 14px; margin: 0;">
        Replaced the previous manual multi-step workflow. Users simply paste or upload prompts and click the emerald <strong>🚀 Start Generating (1-Click Fleet Launch)</strong> button. The system validates &amp; imports prompts, calculates worker quota partitions, dispatches jobs, auto-spawns worker browser instances (<code>auto_launch: true</code>), and transitions the interface directly to Step 3 (Worker Farm) with live polling enabled.
      </p>
    </div>

    <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
      <h4 style="color: #38bdf8; margin: 0 0 8px 0;">2. Live Image Thumbnail Serving &amp; Auto-Sync</h4>
      <p style="color: #94a3b8; font-size: 14px; margin: 0;">
        Fixed the issue where generated media displayed random/solid color placeholder boxes. Purged old test synthetic files and deployed <code>GET /api/v1/projects/:id/prompts/:promptIndex/image</code>, which detects newly downloaded <code>.jpg</code> / <code>.png</code> / <code>.webp</code> illustrations directly from browser download directories, auto-syncs them to project storage, and streams binary image data with 200 OK headers. Updated <code>resolveMediaUrl</code> with prompt context.
      </p>
    </div>

    <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
      <h4 style="color: #38bdf8; margin: 0 0 8px 0;">3. Default Video Preview Tab: Captions</h4>
      <p style="color: #38bdf8; margin: 0 0 8px 0;">
        In Step 4 (Video Preview / CapCut Editor), swapped the default active sub-tab from Effects to <strong>Captions</strong> (<code>#toolTab-captions</code> active, <code>#tabContent-captions</code> flex). Added programmatic auto-selection in <code>goToStep(4)</code> so the synchronized subtitles and caption styling controls are immediately accessible upon navigating to the editor.
      </p>
    </div>
  </div>
</div>
"""

assert "</body>" in html, "</body> not found in documentation.html"
html = html.replace("</body>", new_card + "\n</body>")

with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated documentation.html with new operational enhancements!")
