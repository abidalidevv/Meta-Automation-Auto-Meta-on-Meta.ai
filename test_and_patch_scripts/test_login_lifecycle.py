import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:45450/api/v1"

def test_login_lifecycle():
    print("=== Testing Worker W01 Login Assistant Launch ===")
    req = urllib.request.Request(
        f"{BASE_URL}/workers/login-assistant",
        data=json.dumps({"worker_id": "W01"}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read().decode())
    print("Launch response:", data)
    assert data.get("success") == True, "Failed to launch worker W01"
    
    details = data.get("details", {})
    print("Target URL:", details.get("targetUrl"))
    print("Extension Path:", details.get("extensionPath"))
    print("PID:", details.get("pid"))
    assert details.get("targetUrl") == "https://flow.google.com/?pli=1"
    assert "veo-automation" in details.get("extensionPath")

    print("\nVerifying worker is running in fleet status...")
    resp = urllib.request.urlopen(f"{BASE_URL}/workers/fleet-status", timeout=5)
    fleet = json.loads(resp.read().decode())
    w01 = next(w for w in fleet["workers"] if w["id"] == "W01")
    print(f"Worker W01 status: {w01['status']}, is_running: {w01['is_running']}, PID: {w01['pid']}")
    assert w01["is_running"] == True

    print("\nStopping worker W01 via stop-all...")
    req = urllib.request.Request(
        f"{BASE_URL}/workers/stop-all",
        data=json.dumps({}).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req, timeout=5)
    stop_data = json.loads(resp.read().decode())
    print("Stop response:", stop_data)

    time.sleep(1)
    resp = urllib.request.urlopen(f"{BASE_URL}/workers/fleet-status", timeout=5)
    fleet = json.loads(resp.read().decode())
    w01 = next(w for w in fleet["workers"] if w["id"] == "W01")
    print(f"Worker W01 after stop: is_running={w01['is_running']}")
    assert w01["is_running"] == False

    print("\n=== Worker W01 Login Lifecycle Passed Successfully! ===")

if __name__ == "__main__":
    test_login_lifecycle()
