import os

ts_path = r'E:\stickman-video-automation\studio\server\transcription_service.js'
with open(ts_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header/requires with FFMPEG and FFPROBE
header_target = """const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const { Groq } = require('groq-sdk');
const db = require('./db');
const logger = require('./logger');"""

header_replacement = """const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');
const { Groq } = require('groq-sdk');
const db = require('./db');
const logger = require('./logger');

const FFMPEG_PATH = path.resolve('E:/stickman-video-automation/studio/bin/ffmpeg.exe');
const FFPROBE_PATH = path.resolve('E:/stickman-video-automation/studio/bin/ffprobe.exe');"""

assert header_target in text, "Header target not found"
text = text.replace(header_target, header_replacement, 1)

# Now replace transcribeAudio and getApiKey with pool-aware and chunking-aware version
target_methods = """  async getApiKey() {
    if (process.env.GROQ_API_KEY) {
      return process.env.GROQ_API_KEY;
    }
    const row = await db.get("SELECT value FROM settings WHERE key = 'groq_api_key'");
    return row ? row.value : null;
  }

  /**
   * Transcribe audio file with word-level timestamps
   */
  async transcribeAudio(projectId, audioFilePath) {"""

new_methods = """  async getApiKey() {
    if (process.env.GROQ_API_KEY) {
      return process.env.GROQ_API_KEY;
    }
    const row = await db.get("SELECT value FROM settings WHERE key = 'groq_api_key'");
    return row ? row.value : null;
  }

  /**
   * Get all active Groq API keys from pool, single setting, and environment
   */
  async getApiKeyPool() {
    const keys = [];

    // Check pool setting
    const poolRow = await db.get("SELECT value FROM settings WHERE key = 'groq_api_keys_pool'");
    if (poolRow && poolRow.value) {
      try {
        const parsed = JSON.parse(poolRow.value);
        if (Array.isArray(parsed)) {
          parsed.forEach(k => {
            if (k && typeof k === 'string' && k.trim()) keys.push(k.trim());
          });
        }
      } catch (e) {
        poolRow.value.split(/[,\\r\\n]+/).forEach(k => {
          const clean = k.trim();
          if (clean && clean.startsWith('gsk_')) keys.push(clean);
        });
      }
    }

    // Check single key setting
    const singleRow = await db.get("SELECT value FROM settings WHERE key = 'groq_api_key'");
    if (singleRow && singleRow.value && singleRow.value.trim()) {
      const single = singleRow.value.trim();
      if (!keys.includes(single)) keys.push(single);
    }

    // Check environment
    if (process.env.GROQ_API_KEY && process.env.GROQ_API_KEY.trim()) {
      const envKey = process.env.GROQ_API_KEY.trim();
      if (!keys.includes(envKey)) keys.push(envKey);
    }

    return keys;
  }

  /**
   * Probe audio duration in seconds via FFprobe
   */
  async getAudioDuration(filePath) {
    return new Promise((resolve) => {
      execFile(FFPROBE_PATH, [
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        filePath
      ], (err, stdout) => {
        if (err || !stdout) {
          resolve(0);
        } else {
          const dur = parseFloat(stdout.trim());
          resolve(isNaN(dur) ? 0 : dur);
        }
      });
    });
  }

  /**
   * Slice audio into chunk via FFmpeg
   */
  async sliceAudio(src, dest, startSec, durationSec) {
    return new Promise((resolve, reject) => {
      execFile(FFMPEG_PATH, [
        '-y',
        '-ss', String(startSec),
        '-t', String(durationSec),
        '-i', src,
        '-c:a', 'libmp3lame',
        '-b:a', '128k',
        dest
      ], (err) => {
        if (err) return reject(err);
        resolve();
      });
    });
  }

  /**
   * Transcribe audio file with word-level timestamps
   * Automatically detects files > 20MB, chunks them, and transcribes in parallel across Groq API key pool!
   */
  async transcribeAudio(projectId, audioFilePath) {"""

assert target_methods in text, "Target methods not found"
text = text.replace(target_methods, new_methods, 1)

# Now update the inside of transcribeAudio to handle chunking
chunk_logic_target = """    const groq = new Groq({ apiKey });

    try {
      logger.info('TRANSCRIPTION', `Sending audio to Groq Whisper: ${path.basename(audioFilePath)}`);
      const fileStream = fs.createReadStream(audioFilePath);

      const transcription = await groq.audio.transcriptions.create({
        file: fileStream,
        model: 'whisper-large-v3',
        response_format: 'verbose_json',
        timestamp_granularities: ['word', 'segment']
      });

      const words = transcription.words || [];
      const segments = transcription.segments || [];"""

chunk_logic_replacement = """    const keyPool = await this.getApiKeyPool();
    const activeKeys = keyPool.length > 0 ? keyPool : [apiKey];

    const stats = fs.statSync(audioFilePath);
    const sizeBytes = stats.size;
    const isLargeAudio = sizeBytes > 20 * 1024 * 1024; // > 20MB Groq limit safeguard

    try {
      let words = [];
      let segments = [];

      if (isLargeAudio) {
        // Multi-chunk parallel Groq transcription
        const totalDuration = await this.getAudioDuration(audioFilePath);
        const numChunks = Math.max(2, Math.ceil(sizeBytes / (18 * 1024 * 1024)));
        const chunkDuration = totalDuration > 0 ? (totalDuration / numChunks) : 300;

        logger.info('TRANSCRIPTION', `Large audio detected (${(sizeBytes / (1024 * 1024)).toFixed(1)}MB). Splitting into ${numChunks} chunks for parallel Groq Whisper processing.`);

        const tempDir = path.join(path.dirname(audioFilePath), `chunks_${Date.now()}`);
        if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir, { recursive: true });

        const chunks = [];
        for (let i = 0; i < numChunks; i++) {
          const startSec = i * chunkDuration;
          const chunkPath = path.join(tempDir, `chunk_${i}.mp3`);
          await this.sliceAudio(audioFilePath, chunkPath, startSec, chunkDuration);
          chunks.push({ index: i, path: chunkPath, startSec });
        }

        logger.info('TRANSCRIPTION', `Dispatching ${numChunks} chunks in parallel across ${activeKeys.length} Groq API key(s)`);

        const chunkResults = await Promise.all(chunks.map(async (chk, idx) => {
          const keyForChunk = activeKeys[idx % activeKeys.length];
          const client = new Groq({ apiKey: keyForChunk });
          const stream = fs.createReadStream(chk.path);
          const res = await client.audio.transcriptions.create({
            file: stream,
            model: 'whisper-large-v3',
            response_format: 'verbose_json',
            timestamp_granularities: ['word', 'segment']
          });
          return {
            index: chk.index,
            offset: chk.startSec,
            words: res.words || [],
            segments: res.segments || []
          };
        }));

        // Sort by chunk index
        chunkResults.sort((a, b) => a.index - b.index);

        for (const cRes of chunkResults) {
          for (const w of cRes.words) {
            words.push({
              word: w.word,
              start: +(w.start + cRes.offset).toFixed(3),
              end: +(w.end + cRes.offset).toFixed(3)
            });
          }
          for (const s of cRes.segments) {
            segments.push({
              text: s.text,
              start: +(s.start + cRes.offset).toFixed(3),
              end: +(s.end + cRes.offset).toFixed(3)
            });
          }
        }

        // Clean up temporary chunks
        try { fs.rmSync(tempDir, { recursive: true, force: true }); } catch (e) {}

      } else {
        // Standard single audio transcription
        logger.info('TRANSCRIPTION', `Sending audio to Groq Whisper: ${path.basename(audioFilePath)}`);
        const groq = new Groq({ apiKey });
        const fileStream = fs.createReadStream(audioFilePath);

        const transcription = await groq.audio.transcriptions.create({
          file: fileStream,
          model: 'whisper-large-v3',
          response_format: 'verbose_json',
          timestamp_granularities: ['word', 'segment']
        });

        words = transcription.words || [];
        segments = transcription.segments || [];
      }"""

assert chunk_logic_target in text, "Chunk logic target not found"
text = text.replace(chunk_logic_target, chunk_logic_replacement, 1)

with open(ts_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated transcription_service.js with large audio chunking and parallel Groq key dispatch")
