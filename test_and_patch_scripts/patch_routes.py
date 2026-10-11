routes_path = r"E:\stickman-video-automation\studio\server\routes.js"
with open(routes_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    l = lines[i]
    if "const jobId = `job_${req.params.id}_${physicalWorkerId}_${p.prompt_index}`;" in l:
        new_lines.append(l)
        new_lines.append("        const leaseExpires = new Date(Date.now() + 300 * 1000).toISOString();\n")
        new_lines.append("        await db.run(`\n")
        new_lines.append("          INSERT OR REPLACE INTO jobs (\n")
        new_lines.append("            id, project_id, prompt_id, worker_id, provider, status,\n")
        new_lines.append("            lease_owner, lease_expires_at, created_at, updated_at\n")
        new_lines.append("          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n")
        new_lines.append("        `, [jobId, req.params.id, p.id, physicalWorkerId, provider, isBatch1 ? 'PENDING' : 'QUEUED', physicalWorkerId, leaseExpires, now, now]);\n")
        new_lines.append("        await db.run(\"UPDATE prompts SET assigned_worker_id = ?, status = 'ASSIGNED', updated_at = ? WHERE id = ?\", [physicalWorkerId, now, p.id]);\n")
        
        # Skip until the end of the previous db.run block
        i += 1
        while i < len(lines) and "UPDATE prompts SET assigned_worker_id" not in lines[i] and "`, [" not in lines[i]:
            i += 1
        # Skip the parameter line and closing bracket line
        if i < len(lines) and "`, [" in lines[i]:
            i += 1
        if i < len(lines) and "UPDATE prompts SET assigned_worker_id" in lines[i]:
            i += 1
        if i < len(lines) and ");" in lines[i]:
            i += 1
    else:
        new_lines.append(l)
        i += 1

with open(routes_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("routes.js successfully updated with lease_owner and lease_expires_at!")
