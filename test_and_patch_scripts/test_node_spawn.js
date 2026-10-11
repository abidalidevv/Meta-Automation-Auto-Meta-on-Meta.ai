
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const profileDir = 'E:\\stickman-video-automation\\Workers\\Worker-W01';
const extDir = 'E:\\stickman-video-automation\\Workers\\Worker-W01\\extension';

console.log('Testing Node spawn Chrome...');
const args = [
  '--user-data-dir=' + profileDir,
  '--load-extension=' + extDir,
  '--no-first-run',
  '--no-default-browser-check',
  'https://flow.google.com/?pli=1'
];

const child = spawn(chromePath, args, { detached: true, stdio: 'ignore' });
console.log('Child PID:', child.pid);

child.on('exit', (code, signal) => {
  console.log('Chrome exited with code:', code, 'signal:', signal);
});

setTimeout(() => {
  console.log('Chrome still running after 3s? Killing PID:', child.pid);
  try { process.kill(child.pid); } catch(e) {}
  process.exit(0);
}, 3000);
