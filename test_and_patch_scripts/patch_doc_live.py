import os

doc_path = r'E:\stickman-video-automation\studio\public\documentation.html'
with open(doc_path, 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.rfind('</div>\n</body>')
if pos == -1:
    pos = html.rfind('</body>')

section_html = """
    <!-- LIVE HUMAN TEST & 5-POINT FLEET OPTIMIZATION -->
    <div class="card" style="margin-top: 30px; border-left: 5px solid #10b981; background: #0f172a; padding: 25px; border-radius: 8px;">
      <h2 style="color: #10b981; margin-top: 0;">⚡ Live Fleet Optimization & High-Throughput Batch Engine (Oct 2026)</h2>
      <p style="color: #cbd5e1;">Resolved 5 critical operational bottlenecks discovered during live worker fleet tests:</p>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 15px; margin-top: 15px;">
        <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
          <h4 style="color: #38bdf8; margin: 0 0 8px 0;">1. Clean Browser Launch & Session Isolation</h4>
          <p style="color: #94a3b8; font-size: 14px; margin: 0;">Chrome flags <code>--no-restore-session-state</code> and <code>Default/Sessions</code> purge prevent old tabs/crashed sessions from restoring. Extensions launch cleanly as side panel drawers.</p>
        </div>

        <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
          <h4 style="color: #38bdf8; margin: 0 0 8px 0;">2. Prompt Queue Discrepancy Resolved</h4>
          <p style="color: #94a3b8; font-size: 14px; margin: 0;">Aligned SQLite prompt status filter between <code>dispatchFleet</code> and <code>getNextJob</code> (matching <code>QUEUED</code> and <code>ASSIGNED</code>), ensuring assigned batches are picked up instantly.</p>
        </div>

        <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
          <h4 style="color: #38bdf8; margin: 0 0 8px 0;">3. Flow Settings Dropdown Cache Optimization</h4>
          <p style="color: #94a3b8; font-size: 14px; margin: 0;">Identified missing cache persistence flag in Google Flow automation (<code>c([...], !0)</code>). Once applied, Flow configures aspect ratio and model on prompt 1 and skips dropdown clicks for all subsequent prompts.</p>
        </div>

        <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
          <h4 style="color: #38bdf8; margin: 0 0 8px 0;">4. 50-Prompt Batch Dispatch Engine</h4>
          <p style="color: #94a3b8; font-size: 14px; margin: 0;">Replaced 1-by-1 prompt feeding with unified multi-prompt payloads (<code>payloads: [...]</code>). Up to 50 prompts feed into the extension simultaneously with per-item completion callbacks.</p>
        </div>

        <div style="background: #1e293b; padding: 15px; border-radius: 6px;">
          <h4 style="color: #38bdf8; margin: 0 0 8px 0;">5. Multi-Chunk Parallel Groq Whisper STT</h4>
          <p style="color: #94a3b8; font-size: 14px; margin: 0;">Voiceovers &gt; 20MB are automatically sliced into &lt; 18MB chunks via FFmpeg, dispatched in parallel across the Groq API key pool, and re-stitched with accurate word-level timestamps.</p>
        </div>
      </div>
    </div>
"""

new_html = html[:pos] + section_html + html[pos:]
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated documentation.html successfully")
