import re

filepath = 'E:/stickman-video-automation/studio/server/project_manager.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the try block in parseAndImportPrompts
pattern = r'  try \{\s+for \(const p of promptEntries\) \{[\s\S]*?await db\.exec\(\'COMMIT;\'\);\s+\} catch \(err\) \{'

replacement = '''  try {
    for (const p of promptEntries) {
      const promptPk = `prompt_${projectId}_${p.idStr}`;
      const qa = qaMetadataMap[p.idStr] || {};
      await db.run(`
        INSERT INTO prompts (
          id, project_id, prompt_index, prompt_id_str, prompt_text,
          status, source_span, scene_desc, characters, objects, location,
          qa_verdict, qa_details, provider, model, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, 'QUEUED', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(project_id, prompt_index) DO UPDATE SET
          id = excluded.id,
          prompt_text = excluded.prompt_text,
          prompt_id_str = excluded.prompt_id_str,
          status = 'QUEUED',
          file_path = NULL,
          file_name = NULL,
          file_size = 0,
          sha256 = NULL,
          assigned_worker_id = NULL,
          source_span = excluded.source_span,
          scene_desc = excluded.scene_desc,
          characters = excluded.characters,
          objects = excluded.objects,
          location = excluded.location,
          qa_verdict = excluded.qa_verdict,
          qa_details = excluded.qa_details,
          provider = excluded.provider,
          model = excluded.model,
          updated_at = excluded.updated_at
      `, [
        promptPk, projectId, p.index, p.idStr, p.fullLine,
        qa.source_span || null,
        qa.scene_desc || null,
        qa.characters || null,
        qa.objects || null,
        qa.location || null,
        qa.qa_verdict || 'PASS',
        qa.qa_details || null,
        qa.provider || null,
        qa.model || null,
        now, now
      ]);
    }

    // Prune excess prompts if previous count was higher than new imported count
    const maxIndex = Math.max(...promptEntries.map(p => p.index));
    await db.run(`DELETE FROM prompts WHERE project_id = ? AND prompt_index > ?`, [projectId, maxIndex]);

    // Update target count in project
    await db.run(`UPDATE projects SET target_image_count = ?, updated_at = ? WHERE id = ?`, [promptEntries.length, now, projectId]);
    await db.exec('COMMIT;');
  } catch (err) {'''

new_content = re.sub(pattern, replacement, content)
if new_content != content:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: project_manager.js patched with regex!")
else:
    print("WARNING: Regex pattern did not match!")
