with open(r'E:\stickman-video-automation\studio\server\routes.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """router.get('/projects/:id/character-reference', async (req, res) => {
  try {
    const char = await db.get(`SELECT * FROM character_references WHERE project_id = ? ORDER BY created_at DESC LIMIT 1`, [req.params.id]);
    if (!char || !char.image_path || !fs.existsSync(char.image_path)) {
      return res.status(404).send('Character reference image not found');
    }
    res.sendFile(path.resolve(char.image_path));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

replacement = """router.get('/projects/:id/character-reference', async (req, res) => {
  try {
    const char = await db.get(`SELECT * FROM character_references WHERE project_id = ? ORDER BY created_at DESC LIMIT 1`, [req.params.id]);
    if (!char || !char.image_path || !fs.existsSync(char.image_path)) {
      return res.status(404).send('Character reference image not found');
    }
    res.sendFile(path.resolve(char.image_path));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/projects/:id/character-reference', async (req, res) => {
  try {
    const { character_name, character_description, image_base64 } = req.body;
    const project = await db.get('SELECT * FROM projects WHERE id = ?', [req.params.id]);
    if (!project) return res.status(404).json({ error: 'Project not found' });

    let imagePath = '';
    const now = new Date().toISOString();
    const charName = character_name || 'Main Stickman';
    const charRefId = `char_${Date.now()}`;

    if (image_base64) {
      const cleanB64 = image_base64.includes(',') ? image_base64.split(',')[1] : image_base64;
      const imgBuffer = Buffer.from(cleanB64, 'base64');
      const safeName = charName.replace(/[^a-zA-Z0-9_-]/g, '_');
      const charDir = path.join(project.directory_path, 'characters', safeName);
      fs.mkdirSync(charDir, { recursive: true });
      imagePath = path.join(charDir, 'reference.png');
      fs.writeFileSync(imagePath, imgBuffer);
    }

    await db.run(`
      INSERT INTO character_references (
        id, project_id, character_name, image_path, version, status, description, created_at, updated_at
      ) VALUES (?, ?, ?, ?, 1, 'READY', ?, ?, ?)
    `, [charRefId, req.params.id, charName, imagePath || '', character_description || '', now, now]);

    logger.info('ROUTES', `Updated character reference for project ${req.params.id}: ${charName} (image: ${imagePath ? 'yes' : 'no'})`);
    res.json({ success: true, character_id: charRefId, image_path: imagePath });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

if target in text:
    text = text.replace(target, replacement)
    with open(r'E:\stickman-video-automation\studio\server\routes.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Added POST /projects/:id/character-reference to routes.js!")
else:
    print("TARGET NOT FOUND in routes.js!")
