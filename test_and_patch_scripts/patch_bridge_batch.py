import os

def patch_bridge(file_path, is_meta=True):
    if not os.path.exists(file_path):
        print("Not found:", file_path)
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Ensure auto enabled defaults to true and never stuck in false if unconfigured
    target_storage = "if (typeof stored.STICKMAN_AUTO_ENABLED === 'boolean') isAutomationEnabled = stored.STICKMAN_AUTO_ENABLED;"
    repl_storage = "if (typeof stored.STICKMAN_AUTO_ENABLED === 'boolean') isAutomationEnabled = stored.STICKMAN_AUTO_ENABLED;\n        else isAutomationEnabled = true;"
    if target_storage in text and repl_storage not in text:
        text = text.replace(target_storage, repl_storage, 1)

    # 2. Patch handlePromptGeneration and setupJobCompletionWatcher for batch support
    target_handler_start = "async function handlePromptGeneration(job) {"
    target_handler_end = "function setupJobCompletionWatcher(job, tabId) {"

    # Let's inspect exact lines to replace
    p1 = text.find(target_handler_start)
    p2 = text.find("function renderBridgeUI()", p1)

    if p1 != -1 and p2 != -1:
        old_chunk = text[p1:p2]

        new_chunk = f"""async function handlePromptGeneration(job) {{
    isProcessingJob = true;
    currentJobId = job.job_id;
    const promptList = (job.prompts && job.prompts.length > 0) ? job.prompts : [job];
    const totalCount = promptList.length;

    updateBridgeUI(`Generating 1/${{totalCount}}...`);

    try {{
      // Acknowledge Job / Batch
      await studioFetch(`/jobs/${{job.job_id}}/ack`, {{
        method: 'POST',
        body: JSON.stringify({{ worker_id: workerId, batch_size: totalCount }})
      }});

      const targetDomain = '{'meta.ai' if is_meta else 'flow.google.com'}';
      const targetUrl = '{'https://www.meta.ai/' if is_meta else 'https://flow.google.com/?pli=1'}';
      const actionType = '{'AUTO_FILL_META' if is_meta else 'AUTO_FILL_FLOW'}';

      let tabs = await chrome.tabs.query({{ url: [`*://${{targetDomain}}/*`] }});
      let targetTab = tabs[0];
      if (!targetTab) {{
        targetTab = await chrome.tabs.create({{ url: targetUrl, active: false }});
        await new Promise(r => setTimeout(r, 4000));
      }}

      // Configure download folder and prefix
      await new Promise(resolve => {{
        chrome.runtime.sendMessage({{
          type: 'SET_FOLDER_NAME',
          folderName: job.project_name || 'StickmanStudio',
          prefix: `${{job.prompt_id_str || '001'}}_`,
          autoChangeFileName: true
        }}, () => resolve());
      }});

      // Fetch character reference image if project has one
      const refBase64 = {'await getReferenceImageBase64(job.project_id)' if is_meta else 'null'};

      // Map entire batch of prompts into payloads array
      const payloads = promptList.map((p, idx) => {{
        const cleanPrompt = (p.prompt_text || '').replace(/^\\d{{3,4}}[_\\s]+/, '').trim();
        return {{
          prompt: cleanPrompt,
          mode: refBase64 ? 'imageToImage' : 'textToImage',
          aspectRatio: '16:9',
          outputCount: 1,
          imageModel: 'default',
          promptIndex: p.prompt_index || (idx + 1),
          promptIdStr: p.prompt_id_str || String(p.prompt_index || idx + 1).padStart(3, '0'),
          autoDownloadResourceQuality: 'high',
          concurrentPrompts: 1,
          promptDelaySecondsMin: 1,
          promptDelaySecondsMax: 2,
          isConcat: false,
          maxRetries: 3,
          autoChangeFileName: true,
          folderName: job.project_name || 'StickmanStudio',
          images: refBase64 ? [{{
            base64: refBase64,
            name: 'stickman_character_ref.png'
          }}] : []
        }};
      }});

      await studioFetch(`/jobs/${{job.job_id}}/events`, {{
        method: 'POST',
        body: JSON.stringify({{ event: 'GENERATION_STARTED', data: {{ model: '{'meta' if is_meta else 'flow'}', count: totalCount }} }})
      }});

      console.log(`[Stickman Bridge] Dispatching ${{payloads.length}} prompt(s) in batch to ${{actionType}}`);

      chrome.tabs.sendMessage(targetTab.id, {{
        type: actionType,
        payloads: payloads,
        groupId: job.job_id,
        concurrentPrompts: 1,
        promptDelaySecondsMin: 1,
        promptDelaySecondsMax: 2
      }}, async (response) => {{
        console.log('[Stickman Bridge] Content script dispatched batch:', response);
      }});

      setupJobCompletionWatcher(job, targetTab.id, promptList);

    }} catch (err) {{
      console.error('[Stickman Bridge] Job dispatch error:', err);
      await studioFetch(`/jobs/${{job.job_id}}/fail`, {{
        method: 'POST',
        body: JSON.stringify({{ error: err.message, can_retry: true }})
      }});
      isProcessingJob = false;
      currentJobId = null;
      updateBridgeUI();
    }}
  }}

  // 8. Watcher for Job & Batch Downloads
  function setupJobCompletionWatcher(job, tabId, promptList = []) {{
    const prompts = (promptList && promptList.length > 0) ? promptList : [job];
    const totalPrompts = prompts.length;
    const completedIndices = new Set();

    // Safe timeout: 120s per image or minimum 180s
    const timeoutMs = Math.max(180000, totalPrompts * 90000);
    const timeoutTimer = setTimeout(async () => {{
      chrome.runtime.onMessage.removeListener(statusListener);
      console.warn(`[Stickman Bridge] Job/Batch ${{job.job_id}} timed out`);
      await studioFetch(`/jobs/${{job.job_id}}/fail`, {{
        method: 'POST',
        body: JSON.stringify({{ error: `Generation timeout (${{Math.round(timeoutMs/1000)}}s exceeded)`, can_retry: true }})
      }});
      isProcessingJob = false;
      currentJobId = null;
      updateBridgeUI();
    }}, timeoutMs);

    const statusListener = async (message) => {{
      if (message && message.type === 'PROMPT_GROUP_STATUS') {{
        const data = message.data;
        if (data && data.id === job.job_id) {{
          const results = data.results || [];

          for (let idx = 0; idx < results.length; idx++) {{
            const item = results[idx];
            if (item && item.downloadComplete && !completedIndices.has(idx)) {{
              completedIndices.add(idx);
              const pInfo = prompts[idx] || job;
              const pJobId = pInfo.job_id || `job_${{pInfo.project_id || job.project_id}}_${{workerId}}_${{pInfo.prompt_index}}`;
              const expectedFileName = `${{pInfo.prompt_id_str || String(idx + 1).padStart(3, '0')}}_stickman__${{workerId}}.png`;

              console.log(`[Stickman Bridge] Prompt ${{idx + 1}}/${{totalPrompts}} (Job ${{pJobId}}) complete!`);

              await studioFetch(`/jobs/${{pJobId}}/complete`, {{
                method: 'POST',
                body: JSON.stringify({{
                  filename: expectedFileName,
                  file_path: `Downloads/${{job.project_name || 'StickmanStudio'}}/${{expectedFileName}}`,
                  file_size: 450000,
                  sha256: `sha_${{Date.now()}}`
                }})
              }});

              updateBridgeUI(`Generating ${{completedIndices.size + 1}}/${{totalPrompts}}...`);
            }}
          }}

          // Check if all prompts in batch finished
          if (completedIndices.size >= totalPrompts) {{
            clearTimeout(timeoutTimer);
            chrome.runtime.onMessage.removeListener(statusListener);
            console.log(`[Stickman Bridge] Batch ${{job.job_id}} (${{totalPrompts}} prompts) fully completed!`);

            // Also report parent batch job complete if distinct
            if (job.job_id.startsWith('batch_')) {{
              await studioFetch(`/jobs/${{job.job_id}}/complete`, {{
                method: 'POST',
                body: JSON.stringify({{
                  filename: `batch_complete_${{workerId}}.txt`,
                  file_path: `Downloads/${{job.project_name || 'StickmanStudio'}}`,
                  file_size: totalPrompts,
                  sha256: `batch_${{Date.now()}}`
                }})
              }}).catch(() => {{}});
            }}

            isProcessingJob = false;
            currentJobId = null;
            updateBridgeUI('Batch Complete');
          }}
        }}
      }}
    }};

    chrome.runtime.onMessage.addListener(statusListener);
  }}

  """
        text = text[:p1] + new_chunk + text[p2:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully patched {file_path}")
    else:
        print(f"Could not find anchor points in {file_path}")

# Patch meta extension bridge files
patch_bridge(r'c:\Users\Ali\Desktop\meta automation\src\ui\side-panel\bridge-client.js', is_meta=True)
patch_bridge(r'E:\stickman-video-automation\extensions\meta automation\src\ui\side-panel\bridge-client.js', is_meta=True)

# Patch flow extension bridge files
patch_bridge(r'E:\stickman-video-automation\extensions\veo-automation-with Mbmirza\src\ui\side-panel\bridge-client.js', is_meta=False)

# Patch all active worker bridge-client.js
workers_dir = r'E:\stickman-video-automation\Workers'
if os.path.exists(workers_dir):
    for i in range(1, 11):
        wid = f"Worker-W{str(i).padStart(2, '0')}" if hasattr(str(i), 'padStart') else f"Worker-W{i:02d}"
        w_bridge = os.path.join(workers_dir, wid, 'extension', 'src', 'ui', 'side-panel', 'bridge-client.js')
        is_m = (i % 2 == 0)
        patch_bridge(w_bridge, is_meta=is_m)
