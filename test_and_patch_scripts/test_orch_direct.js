const db = require('E:/stickman-video-automation/studio/server/db');
const orchestrator = require('E:/stickman-video-automation/studio/server/worker_orchestrator');

async function test() {
  await db.init();
  const res = await orchestrator.getNextJob('W01');
  console.log('Result from orchestrator.getNextJob directly:', JSON.stringify(res, null, 2));
}

test().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
