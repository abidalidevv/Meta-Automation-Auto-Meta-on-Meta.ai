import os

# Paths to update
meta_dirs = [
    'C:/Users/Ali/Desktop/meta automation',
    'E:/stickman-video-automation/extensions/meta automation'
]

flow_dirs = [
    'E:/stickman-video-automation/extensions/veo-automation-with Mbmirza'
]

# 1. New Service Worker Loader for Meta (Side panel drawer, NO extra tab)
meta_sw_content = """import './assets/index.ts-BqblPwcc.js';

// Configure Chrome Side Panel Drawer behavior (Native side drawer, NO separate tab!)
const setupSidePanel = async () => {
  try {
    if (chrome.sidePanel && chrome.sidePanel.setPanelBehavior) {
      await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
    }
  } catch (e) {
    console.warn('[ServiceWorker] setPanelBehavior error:', e);
  }
};

chrome.runtime.onStartup.addListener(setupSidePanel);
chrome.runtime.onInstalled.addListener(setupSidePanel);
setupSidePanel();

// Automatically open the native side panel drawer when a new window is created
if (typeof chrome.windows !== 'undefined' && chrome.windows.onCreated) {
  chrome.windows.onCreated.addListener(async (win) => {
    try {
      if (chrome.sidePanel && chrome.sidePanel.open && win && win.id) {
        setTimeout(async () => {
          try {
            await chrome.sidePanel.open({ windowId: win.id });
          } catch (err) {}
        }, 1200);
      }
    } catch (e) {}
  });
}
"""

# 2. New Service Worker Loader for Flow (Side panel drawer, NO extra tab)
flow_sw_content = """import './assets/index.ts-BNvXgTH3.js';

// Configure Chrome Side Panel Drawer behavior (Native side drawer, NO separate tab!)
const setupSidePanel = async () => {
  try {
    if (chrome.sidePanel && chrome.sidePanel.setPanelBehavior) {
      await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
    }
  } catch (e) {
    console.warn('[ServiceWorker] setPanelBehavior error:', e);
  }
};

chrome.runtime.onStartup.addListener(setupSidePanel);
chrome.runtime.onInstalled.addListener(setupSidePanel);
setupSidePanel();

// Automatically open the native side panel drawer when a new window is created
if (typeof chrome.windows !== 'undefined' && chrome.windows.onCreated) {
  chrome.windows.onCreated.addListener(async (win) => {
    try {
      if (chrome.sidePanel && chrome.sidePanel.open && win && win.id) {
        setTimeout(async () => {
          try {
            await chrome.sidePanel.open({ windowId: win.id });
          } catch (err) {}
        }, 1200);
      }
    } catch (e) {}
  });
}
"""

for d in meta_dirs:
    p = os.path.join(d, 'service-worker-loader.js')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(meta_sw_content)
    print(f"Updated {p}")

for d in flow_dirs:
    p = os.path.join(d, 'service-worker-loader.js')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(flow_sw_content)
    print(f"Updated {p}")
