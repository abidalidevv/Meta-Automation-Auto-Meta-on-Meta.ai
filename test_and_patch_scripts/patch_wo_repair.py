wo_path = r'E:\stickman-video-automation\studio\server\worker_orchestrator.js'
with open(wo_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """  // 2. High-Priority Repair Queue check (scoped to target project)
  let repairQuery = `
    SELECT p.*, pr.name as project_name, pr.directory_path, pr.character_id
    FROM prompts p
    JOIN projects pr ON p.project_id = pr.id
    WHERE p.status = 'REPAIR_PENDING' AND pr.status = 'ACTIVE'
  `;
  const repairParams = [];
  if (targetProjectId) {
    repairQuery += ` AND p.project_id = ? `;
    repairParams.push(targetProjectId);
  }"""

replacement = """  // 2. High-Priority Repair Queue check (scoped to target worker & project)
  let repairQuery = `
    SELECT p.*, pr.name as project_name, pr.directory_path, pr.character_id
    FROM prompts p
    JOIN projects pr ON p.project_id = pr.id
    WHERE p.status = 'REPAIR_PENDING' AND (p.assigned_worker_id = ? OR p.assigned_worker_id IS NULL OR p.assigned_worker_id = '') AND pr.status = 'ACTIVE'
  `;
  const repairParams = [id];
  if (targetProjectId) {
    repairQuery += ` AND p.project_id = ? `;
    repairParams.push(targetProjectId);
  }"""

assert target in text, "Target not found in worker_orchestrator.js"
new_text = text.replace(target, replacement, 1)

with open(wo_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Successfully updated repairQuery in worker_orchestrator.js")
