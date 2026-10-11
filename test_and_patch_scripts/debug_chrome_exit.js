const { spawn } = require('child_process');

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
  '--enable-logging=stderr',
  '--v=1',
  targetUrl
];

console.log('Spawning with pipe...');
const child = spawn(chromePath, args);

child.stdout.on('data', (d) => console.log('STDOUT:', d.toString()));
child.stderr.on('data', (d) => console.log('STDERR:', d.toString()));
child.on('exit', (code, signal) => console.log('EXIT CODE:', code, signal));
