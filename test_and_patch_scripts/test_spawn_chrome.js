const { spawn } = require('child_process');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const profileDir = 'E:\\stickman-video-automation\\Workers\\Worker-W01';
const extensionPath = 'E:\\stickman-video-automation\\Workers\\Worker-W01\\extension';
const targetUrl = 'https://www.meta.ai/';

const args = [
  `--user-data-dir=${profileDir}`,
  `--load-extension=${extensionPath}`,
  '--no-first-run',
  '--no-default-browser-check',
  '--no-restore-session-state',
  '--disable-session-crashed-bubble',
  '--restore-last-session=0',
  '--hide-crash-restore-bubble',
  '--disable-background-networking',
  '--disable-default-apps',
  '--disable-sync',
  targetUrl
];

console.log('Spawning Chrome for Worker-W01...');
const child = spawn(chromePath, args, {
  detached: true,
  stdio: 'ignore'
});

child.unref();
console.log('Spawned with PID:', child.pid);
