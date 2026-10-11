import re

filepath = 'E:/stickman-video-automation/studio/server/ai_story_engine.js'
with open(filepath, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update DEFAULT_GROQ_MODEL and PACING_MULTIPLIERS
code = code.replace(
    "const DEFAULT_GROQ_MODEL = 'openai/gpt-oss-120b';",
    "const DEFAULT_GROQ_MODEL = 'llama-3.3-70b-versatile';"
)

old_pacing = """const PACING_MULTIPLIERS = {
  '1/4s': 0.25, // 1 image per 4 seconds
  '2/4s': 0.50, // 2 images per 4 seconds (1 per 2s, default)
  '3/4s': 0.75, // 3 images per 4 seconds
  '4/4s': 1.00, // 4 images per 4 seconds (1 per 1s)
  '5/4s': 1.25, // 5 images per 4 seconds
  'Custom': 0.50
};"""

new_pacing = """const PACING_MULTIPLIERS = {
  'Random': 0.50, // Dynamic Anti-Template YouTube Pacing (1.5s - 3.0s variable rhythm, avg ~2.0s)
  '3/4s': 0.75,   // 3 images per 4 seconds (1.33s/image - Dynamic Story)
  '2/4s': 0.50,   // 2 images per 4 seconds (2.00s/image - YouTube Standard)
  '1/4s': 0.25,   // 1 image per 4 seconds (4.00s/image - Relaxed / Cinematic)
  '4/4s': 1.00,   // 4 images per 4 seconds (1.00s/image - Fast Action)
  '5/4s': 1.25,   // 5 images per 4 seconds (0.80s/image - Hyper Energetic)
  'Custom': 0.50
};"""
code = code.replace(old_pacing, new_pacing)

# 2. Update getCanonicalMasterPrompt
old_master_fn = """  getCanonicalMasterPrompt() {
    if (fs.existsSync(CANONICAL_MASTER_PROMPT_PATH)) {
      return fs.readFileSync(CANONICAL_MASTER_PROMPT_PATH, 'utf8');
    }
    // Fallback search in parent directory
    const altPath = path.resolve(__dirname, '../master_prompt.md');
    if (fs.existsSync(altPath)) {
      return fs.readFileSync(altPath, 'utf8');
    }
    logger.warn('AI_ENGINE', `Canonical master_prompt.md not found at ${CANONICAL_MASTER_PROMPT_PATH}`);
    return '';
  }"""

new_master_fn = """  getCanonicalMasterPrompt() {
    const candidatePaths = [
      path.resolve(__dirname, '../../Old Md files/story to prompts.md'),
      path.resolve(__dirname, '../../story to prompts.md'),
      path.resolve(__dirname, '../../master_prompt.md'),
      CANONICAL_MASTER_PROMPT_PATH,
      path.resolve(__dirname, '../master_prompt.md')
    ];

    for (const p of candidatePaths) {
      if (fs.existsSync(p)) {
        logger.info('AI_ENGINE', `Loaded Master Directive V7 from: ${p}`);
        return fs.readFileSync(p, 'utf8');
      }
    }
    logger.warn('AI_ENGINE', 'No master prompt directive file found in candidate paths.');
    return '';
  }"""
code = code.replace(old_master_fn, new_master_fn)

# 3. Fix generateWithGroq implementation
pattern_groq = r'  async generateWithGroq\(\{[\s\S]*?return parsed;\s+\}'

replacement_groq = '''  async generateWithGroq({
    scriptText,
    targetCount,
    modelName = DEFAULT_GROQ_MODEL,
    videoTitle = null,
    masterPrompt = null,
    characterReference = null,
    visualElements = null
  }) {
    const apiKey = await this.getApiKey();
    if (!apiKey) {
      throw new Error('Groq API Key not configured in environment or settings.');
    }

    // Use user-supplied master prompt if present, otherwise load canonical master_prompt.md
    let systemInstruction = (masterPrompt && masterPrompt.trim()) ? masterPrompt.trim() : this.getCanonicalMasterPrompt();
    if (!systemInstruction) {
      systemInstruction = 'You are the Lead Visual Director for Stickman Studio. Output 2D stickman sketch prompts as pure JSON.';
    }

    let userPrompt = '';
    if (videoTitle && videoTitle.trim()) {
      userPrompt += `VIDEO TITLE:\\n"${videoTitle.trim()}"\\n\\n`;
    }
    if (characterReference && characterReference.trim()) {
      userPrompt += `CHARACTER REFERENCE / PROTAGONIST:\\n"${characterReference.trim()}"\\n\\n`;
    }
    if (visualElements && visualElements.trim()) {
      userPrompt += `RECURRING VISUAL ELEMENTS / MOTIFS:\\n"${visualElements.trim()}"\\n\\n`;
    }

    userPrompt += `VOICEOVER SCRIPT:
\"\"\"
${scriptText}
\"\"\"

TARGET IMAGE COUNT: Exactly ${targetCount} prompts.
Pacing: Generate precisely ${targetCount} sequential prompts numbered from 001 to ${String(targetCount).padStart(3, '0')}.
Ensure each prompt begins with its 3-digit prefix (e.g., "001_...", "002_...").
Translate all script narration into visual stickman scenes adhering strictly to the visual laws in the Master Prompt.
Output pure JSON with the keys:
{
  "story_bible": {
    "protagonist": "Description",
    "setting": "Description",
    "recurring_elements": []
  },
  "prompts": [
    {
      "index": 1,
      "id_str": "001",
      "prompt_text": "001_Clean premium 2D educational stickman illustration, matching the supplied reference style: simple white/light-cream background, thin hand-drawn black outlines, round white stickman head, very expressive eyes and face, extremely simple thin black body/limbs, flat muted blue, green, tan and pale yellow accents, minimal objects, subtle clean shadows, no gradients, no photorealism, no text, no labels, no watermark, consistent character proportions and line weight, cinematic 16:9 composition, clear readable silhouette, professional YouTube documentary visual. Scene: ...",
      "visual_beat": "Beat description",
      "character_action": "Action description"
    }
  ]
}`;

    const modelsToTry = [
      modelName,
      'llama-3.3-70b-versatile',
      'llama-3.1-70b-versatile',
      'llama-3.1-8b-instant',
      'mixtral-8x7b-32768'
    ].filter(Boolean);
    const uniqueModels = [...new Set(modelsToTry)];

    const keyPool = await this.getApiKeyPool();
    const keysToTry = keyPool.length > 0 ? keyPool : [apiKey];

    let rawContent = null;
    let lastErr = null;
    let usedModel = uniqueModels[0];

    for (const key of keysToTry) {
      const client = new Groq({ apiKey: key });
      for (const m of uniqueModels) {
        try {
          logger.info('AI_ENGINE', `Calling Groq (${m}) with key ${key.slice(0, 8)}... for ${targetCount} prompts...`);
          const completion = await client.chat.completions.create({
            messages: [
              { role: 'system', content: systemInstruction },
              { role: 'user', content: userPrompt }
            ],
            model: m,
            response_format: { type: 'json_object' },
            temperature: 0.7,
            max_tokens: 8192
          });

          rawContent = completion.choices[0]?.message?.content;
          if (rawContent) {
            usedModel = m;
            break;
          }
        } catch (err) {
          logger.warn('AI_ENGINE', `Model ${m} failed: ${err.message}`);
          lastErr = err;
        }
      }
      if (rawContent) break;
    }

    if (!rawContent) {
      throw new Error(`All Groq models and keys failed. Last error: ${lastErr ? lastErr.message : 'Unknown'}`);
    }

    const parsed = JSON.parse(rawContent);
    if (!parsed.prompts || !Array.isArray(parsed.prompts)) {
      throw new Error('Groq response did not contain a valid prompts array');
    }

    parsed.modelUsed = usedModel;
    return parsed;
  }'''

code = re.sub(pattern_groq, replacement_groq, code)

# 4. Add raw_prompts_text to return object in generateScriptPrompts
old_return = """    return {
      success: true,
      provider: providerUsed,
      model: modelName,"""

new_return = """    return {
      success: true,
      provider: providerUsed,
      model: modelName,
      raw_prompts_text: rawPromptsText,"""
code = code.replace(old_return, new_return)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: ai_story_engine.js patched cleanly!")
