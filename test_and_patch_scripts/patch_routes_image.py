routes_path = r'E:\stickman-video-automation\studio\server\routes.js'
with open(routes_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """router.get('/projects/:id/prompts', async (req, res) => {
  try {
    const prompts = await db.all(`
      SELECT * FROM prompts WHERE project_id = ? ORDER BY prompt_index ASC
    `, [req.params.id]);
    res.json(prompts);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});"""

new_code = """router.get('/projects/:id/prompts', async (req, res) => {
  try {
    const prompts = await db.all(`
      SELECT * FROM prompts WHERE project_id = ? ORDER BY prompt_index ASC
    `, [req.params.id]);
    res.json(prompts);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Realtime Prompt Image Serving & Auto-Sync from Downloads
router.get('/projects/:id/prompts/:promptIndex/image', async (req, res) => {
  try {
    const { id, promptIndex } = req.params;
    const project = await db.get('SELECT * FROM projects WHERE id = ?', [id]);
    if (!project) return res.status(404).send('Project not found');

    const promptStr = String(promptIndex).padStart(3, '0');
    const ingestionManager = require('./ingestion_manager');
    const centralDir = path.join(project.directory_path, 'central_images');

    // Check Downloads directory and subfolders first for fresh real images
    const searchDirs = [
      path.join(ingestionManager.downloadsDir, project.name),
      path.join(ingestionManager.downloadsDir, 'veo-folder-1'),
      path.join(ingestionManager.downloadsDir, 'meta-folder-1'),
      path.join(ingestionManager.downloadsDir, 'StickmanStudio'),
      ingestionManager.downloadsDir
    ];

    for (const dir of searchDirs) {
      if (fs.existsSync(dir)) {
        const files = fs.readdirSync(dir);
        const match = files.find(f => f.startsWith(`${promptStr}_`) && /\\.(jpg|jpeg|png|webp)$/i.test(f));
        if (match) {
          const dlPath = path.join(dir, match);
          if (!fs.existsSync(centralDir)) fs.mkdirSync(centralDir, { recursive: true });
          const destPath = path.join(centralDir, match);
          try { fs.copyFileSync(dlPath, destPath); } catch (e) {}

          await db.run("UPDATE prompts SET file_name = ?, file_path = ?, status = 'COMPLETED' WHERE project_id = ? AND prompt_index = ?", [match, destPath, id, parseInt(promptIndex, 10)]);
          await db.run("UPDATE timeline_items SET image_path = ? WHERE project_id = ? AND order_index = ?", [destPath, id, parseInt(promptIndex, 10)]);

          return res.sendFile(dlPath);
        }
      }
    }

    // Direct check in project central_images
    if (fs.existsSync(centralDir)) {
      const files = fs.readdirSync(centralDir);
      const match = files.find(f => f.startsWith(`${promptStr}_`) && /\\.(jpg|jpeg|png|webp)$/i.test(f));
      if (match) {
        return res.sendFile(path.join(centralDir, match));
      }
    }

    return res.status(404).send('Image not ready');
  } catch (err) {
    res.status(500).send(err.message);
  }
});"""

assert target in text, "Target not found in routes.js"
new_text = text.replace(target, new_code, 1)

with open(routes_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Successfully added prompt image serving route to routes.js")
