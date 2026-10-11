import os
import sys

doc_path = r'E:\stickman-video-automation\studio\public\documentation.html'
with open(doc_path, 'r', encoding='utf-8') as f:
    html = f.read()

s6_idx = html.find('<section id="step6" class="doc-section">')
s6_end = html.find('</section>', s6_idx)

new_doc_step6 = """<section id="step6" class="doc-section">
      <h2>Step 6: AI API Keys Vault & 10-Worker Isolated Login Assistant</h2>
      <p>
        Stickman Studio V2 features an enterprise-grade API key vault and a robust 10-worker browser farm architecture.
        Every browser worker is strictly isolated to <strong>one extension and one service</strong> (either Meta AI or Google Flow).
      </p>

      <h3>1. Dedicated 1-Worker-1-Extension Architecture</h3>
      <div style="background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 8px; padding: 16px; margin: 16px 0;">
        <strong style="color: #fff; font-size: 14px;">Key Architectural Rule: Strict Single-Service Isolation</strong>
        <p style="margin-top: 6px; font-size: 13px; color: var(--text-dim); line-height: 1.6;">
          Dual tabs and dual extensions inside a single browser instance cause session conflicts, memory bloat, and cookie crossover.
          In Studio V2:
        </p>
        <ul style="margin: 8px 0 0 20px; font-size: 13px; color: var(--text-dim); line-height: 1.7;">
          <li><strong>Flow Workers (W01, W03, W05, W07, W09 by default):</strong> Open strictly <code>https://flow.google.com/?pli=1</code> and load only the <code>Veo Flow Automation</code> extension with isolated config (<code>WORKER_ID: Wnn, PROVIDER: flow</code>).</li>
          <li><strong>Meta Workers (W02, W04, W06, W08, W10 by default):</strong> Open strictly <code>https://www.meta.ai/</code> and load only the <code>Meta Automation</code> extension with isolated config (<code>WORKER_ID: Wnn, PROVIDER: meta</code>).</li>
          <li><strong>Provider Toggle:</strong> Any worker can be switched between Flow and Meta instantly with the <code>⇄ Switch</code> button or <code>POST /api/v1/workers/:id/provider</code>.</li>
        </ul>
      </div>

      <h3>2. 10-Worker One-Time Login Assistant Workflow</h3>
      <p>
        To automate prompt generation across all 10 workers without continuous login re-prompts:
      </p>
      <ol style="margin-left: 20px; line-height: 1.8; color: var(--text-dim);">
        <li>Click <strong>🚀 Launch All 10 Worker Profiles for One-Time Login</strong> (or launch an individual worker).</li>
        <li>Studio V2 safely cleans orphan processes, unlocks stale lockfiles, provisions isolated extensions, and launches dedicated Chrome instances staggered by 1.2s.</li>
        <li>Log in once by hand in each window (sign into Google Flow in Flow windows, sign into Meta AI in Meta windows).</li>
        <li>Chrome permanently commits authentication tokens and session cookies to <code>Workers/Worker-Wnn/Default/Network/Cookies</code>.</li>
        <li>Close the windows. Future automated batch dispatches in Step 2 run non-stop with persistent authentication!</li>
      </ol>

      <h3>3. Multi-Provider Cloud API Keys Vault</h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin: 16px 0;">
        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px;">
          <h4 style="color: var(--cyan); margin-bottom: 6px;">⚡ Groq Cloud AI</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom: 8px;">Lightning-fast LLaMA 3.3 70B & 8B story engines. Supports multi-key rotation pool for unlimited free generation and real-time latency ping testing.</p>
          <a href="https://console.groq.com/keys" target="_blank" style="font-size: 12px; color: var(--cyan);">console.groq.com &rarr;</a>
        </div>

        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px;">
          <h4 style="color: var(--violet); margin-bottom: 6px;">🎙️ ElevenLabs AI</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom: 8px;">Ultra-realistic narration voiceovers with custom Voice ID support (e.g. Rachel, Adam, Domi) for broadcast-quality audio.</p>
          <a href="https://elevenlabs.io" target="_blank" style="font-size: 12px; color: var(--violet);">elevenlabs.io &rarr;</a>
        </div>

        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px;">
          <h4 style="color: var(--emerald); margin-bottom: 6px;">🤖 OpenAI / Whisper</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom: 8px;">GPT-4o script generation and high-accuracy Whisper speech-to-text audio alignment fallback.</p>
          <a href="https://platform.openai.com/api-keys" target="_blank" style="font-size: 12px; color: var(--emerald);">openai.com &rarr;</a>
        </div>

        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px;">
          <h4 style="color: var(--amber); margin-bottom: 6px;">🎨 Stability AI & Stock Media</h4>
          <p style="font-size: 12px; color: var(--text-dim); margin-bottom: 8px;">SDXL image generation fallback and Pexels stock video footage integration for dynamic B-roll clips.</p>
          <a href="https://platform.stability.ai" target="_blank" style="font-size: 12px; color: var(--amber);">stability.ai &rarr;</a>
        </div>
      </div>

      <h3>4. Human-Readable Logging & Live Telemetry</h3>
      <p>
        All system actions, FFmpeg render runs, Chrome spawn arguments, and worker API heartbeats are logged with millisecond timestamps to <code>studio/logs/studio.log</code>.
        View the live event stream directly on Step 6 or click <strong>View studio.log</strong> to open the full raw file.
      </p>
    </section>"""

if s6_idx != -1 and s6_end != -1:
    html = html[:s6_idx] + new_doc_step6 + html[s6_end + len('</section>'):]
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('documentation.html Step 6 section updated successfully!')
else:
    print('Could not find step6 in documentation.html: s6_idx =', s6_idx)
