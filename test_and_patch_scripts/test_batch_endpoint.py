import requests

BASE_URL = 'http://127.0.0.1:45450/api/v1'

print("--- 1. Testing Worker Registration ---")
reg_res = requests.post(f"{BASE_URL}/workers/register", json={"id": "W01", "provider": "flow"})
print("W01 Register:", reg_res.status_code, reg_res.json())

print("\n--- 2. Testing Job Polling (Batch Check) ---")
job_res = requests.get(f"{BASE_URL}/workers/W01/job")
print("W01 Job Status:", job_res.status_code)
job_data = job_res.json()
if job_data and job_data.get('job'):
    j = job_data['job']
    print(f"Received job type: {j.get('type')}")
    print(f"Total prompts in batch: {j.get('total_prompts')}")
    print(f"Job ID: {j.get('job_id')}")
    prompts = j.get('prompts', [])
    print(f"Prompts count: {len(prompts)}")
    for p in prompts[:3]:
        print("  Sample prompt:", p)
else:
    print("Job Response:", job_data)
