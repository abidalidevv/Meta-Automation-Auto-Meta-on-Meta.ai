import re
import os

print("Starting backend patcher...")

# 1. Update ai_story_engine.js
engine_file = r'E:\stickman-video-automation\studio\server\ai_story_engine.js'
with open(engine_file, 'r', encoding='utf-8') as f:
    engine_code = f.read()

# Update DEFAULT_GROQ_MODEL
if "const FALLBACK_GROQ_MODELS" not in engine_code:
    engine_code = re.sub(
        r"const DEFAULT_GROQ_MODEL = '[^']+';",
        "const DEFAULT_GROQ_MODEL = 'llama-3.3-70b-versatile';\nconst FALLBACK_GROQ_MODELS = ['llama-3.3-70b-versatile', 'llama-3.1-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768'];",
        engine_code
    )

# Update PACING_MULTIPLIERS
engine_code = re.sub(
    r"const PACING_MULTIPLIERS = \{[^\}]+\};",
    """const PACING_MULTIPLIERS = {
  '1/4s': 0.25, // 1 image per 4 seconds
  '2/4s': 0.50, // 2 images per 4 seconds (1 per 2s, default)
  '3/4s': 0.75, // 3 images per 4 seconds
  '4/4s': 1.00, // 4 images per 4 seconds (1 per 1s)
  '5/4s': 1.25, // 5 images per 4 seconds
  'Random': 0.50, // Dynamic Anti-Template pacing (avg 1 image per 2s)
  'Custom': 0.50
};""",
    engine_code
)

# Update getCanonicalMasterPrompt
new_master_fn = """  getCanonicalMasterPrompt() {
    const candidates = [
      'e:/stickman-video-automation/Old Md files/story to prompts.md',
      'E:/stickman-video-automation/Old Md files/story to prompts.md',
      path.resolve(__dirname, '../../Old Md files/story to prompts.md'),
      CANONICAL_MASTER_PROMPT_PATH,
      path.resolve(__dirname, '../master_prompt.md')
    ];
    for (const c of candidates) {
      if (fs.existsSync(c)) {
        return fs.readFileSync(c, 'utf8');
      }
    }
    logger.warn('AI_ENGINE', 'Canonical master prompt not found, using minimal fallback');
    return '';
  }"""

engine_code = re.sub(
    r"  getCanonicalMasterPrompt\(\)\s*\{[\s\S]*?return '';\s*\}",
    new_master_fn,
    engine_code
)

# Replace broken Groq call in generateWithGroq
broken_call_pat = r"// Groq call handled with key pool above[\s\S]*?return parsed;"

replacement_groq_call = """    const pool = await this.getApiKeyPool();
    if (!pool || pool.length === 0) {
      throw new Error('Groq API Key not configured in environment or settings.');
    }

    const modelsToTry = [
      modelName || DEFAULT_GROQ_MODEL,
      ...FALLBACK_GROQ_MODELS.filter(m => m !== (modelName || DEFAULT_GROQ_MODEL))
    ];

    let lastError = null;
    for (const modelToUse of modelsToTry) {
      for (let attempt = 0; attempt < pool.length; attempt++) {
        const currentKey = pool[(this._keyCursor || 0) % pool.length];
        try {
          logger.info('AI_ENGINE', `Calling Groq API (Model: ${modelToUse}, Key Index: ${this._keyCursor || 0}) for ${targetCount} prompts...`);
          const groq = new Groq({ apiKey: currentKey });
          const chatCompletion = await groq.chat.completions.create({
            messages: [
              { role: 'system', content: systemInstruction },
              { role: 'user', content: userPrompt }
            ],
            model: modelToUse,
            temperature: 0.3,
            response_format: { type: 'json_object' }
          });

          const rawContent = chatCompletion.choices[0]?.message?.content || '{}';
          let cleanJson = rawContent.trim();
          if (cleanJson.startsWith('```')) {
            cleanJson = cleanJson.replace(/^```(?:json)?\\s*/i, '').replace(/\\s*```$/, '');
          }
          const parsed = JSON.parse(cleanJson);

          if (!parsed.prompts || !Array.isArray(parsed.prompts)) {
            throw new Error('Groq response did not contain a valid prompts array');
          }

          logger.info('AI_ENGINE', `Groq generated ${parsed.prompts.length} prompts using ${modelToUse}`);
          return parsed;
        } catch (err) {
          logger.warn('AI_ENGINE', `Groq attempt failed on model ${modelToUse}: ${err.message}`);
          lastError = err;
          this.rotateApiKey(pool.length);
        }
      }
    }

    throw new Error(`All Groq models and keys failed. Last error: ${lastError ? lastError.message : 'Unknown'}`);"""

engine_code = re.sub(broken_call_pat, lambda m: replacement_groq_call, engine_code)

# Add raw_prompts_text if not present
if "raw_prompts_text: rawPromptsText," not in engine_code:
    engine_code = engine_code.replace(
        "prompts: generationResult.prompts,",
        "prompts: generationResult.prompts,\n      raw_prompts_text: rawPromptsText,"
    )

with open(engine_file, 'w', encoding='utf-8') as f:
    f.write(engine_code)
print("Updated ai_story_engine.js!")

# 2. Update project_manager.js
pm_file = r'E:\stickman-video-automation\studio\server\project_manager.js'
with open(pm_file, 'r', encoding='utf-8') as f:
    pm_code = f.read()

pm_code = re.sub(
    r"const PACING_MULTIPLIERS = \{[^\}]+\};",
    """const PACING_MULTIPLIERS = {
  '1/4s': 0.25,
  '2/4s': 0.50,
  '3/4s': 0.75,
  '4/4s': 1.00,
  '5/4s': 1.25,
  'Random': 0.50,
  'Custom': 0.50
};""",
    pm_code
)

with open(pm_file, 'w', encoding='utf-8') as f:
    f.write(pm_code)
print("Updated project_manager.js!")

# 3. Update routes.js
routes_file = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_file, 'r', encoding='utf-8') as f:
    routes_code = f.read()

new_routes_master = """router.get('/ai/master-prompt-default', (req, res) => {
  try {
    const candidates = [
      'e:/stickman-video-automation/Old Md files/story to prompts.md',
      'E:/stickman-video-automation/Old Md files/story to prompts.md',
      path.resolve(__dirname, '../../Old Md files/story to prompts.md'),
      path.resolve(__dirname, '../../master_prompt.md'),
      path.resolve(__dirname, '../master_prompt.md')
    ];
    for (const p of candidates) {
      if (fs.existsSync(p)) {
        const text = fs.readFileSync(p, 'utf8');
        return res.json({ master_prompt: text });
      }
    }
    res.json({ master_prompt: '' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

routes_code = re.sub(
    r"router\.get\('/ai/master-prompt-default'[\s\S]*?res\.json\(\{\s*master_prompt:\s*''\s*\}\);\s*\}\s*catch\s*\(err\)[\s\S]*?\}\);",
    new_routes_master,
    routes_code
)

with open(routes_file, 'w', encoding='utf-8') as f:
    f.write(routes_code)
print("Updated routes.js!")
