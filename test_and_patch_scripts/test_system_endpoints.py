import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:45450/api/v1"

def test_api():
    print("=== 1. Testing Health Endpoint ===")
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:45450/health", timeout=3)
        print("Health status:", resp.getcode(), resp.read().decode())
    except Exception as e:
        print("Health check failed:", e)

    print("\n=== 2. Testing Fleet Status Endpoint ===")
    try:
        resp = urllib.request.urlopen(f"{BASE_URL}/workers/fleet-status", timeout=5)
        data = json.loads(resp.read().decode())
        workers = data.get("workers", [])
        print(f"Total workers returned: {len(workers)}")
        for w in workers:
            print(f"  Worker: {w['id']} | Provider: {w['provider']} | Auth: {w['authenticated']} | Status: {w['status']}")
        assert len(workers) == 10, f"Expected 10 workers, got {len(workers)}"
    except Exception as e:
        print("Fleet status failed:", e)

    print("\n=== 3. Testing Worker Provider Toggle ===")
    try:
        # Test toggling W01 to meta then back to flow
        req = urllib.request.Request(
            f"{BASE_URL}/workers/W01/provider",
            data=json.dumps({"provider": "flow"}).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        res_data = json.loads(resp.read().decode())
        print("Set W01 to flow:", res_data)
        assert res_data.get("provider") == "flow"
    except Exception as e:
        print("Provider toggle failed:", e)

    print("\n=== 4. Testing Settings GET and POST ===")
    try:
        # POST settings
        req = urllib.request.Request(
            f"{BASE_URL}/settings",
            data=json.dumps({
                "groq_primary_model": "llama-3.3-70b-versatile",
                "default_fps": "60",
                "default_resolution": "3840x2160",
                "speed_preset": "ultrafast"
            }).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        print("POST settings status:", resp.getcode())

        # GET settings
        resp = urllib.request.urlopen(f"{BASE_URL}/settings", timeout=5)
        settings = json.loads(resp.read().decode())
        print("GET settings received keys:", list(settings.keys()))
        print("  groq_primary_model:", settings.get("groq_primary_model"))
        print("  default_fps:", settings.get("default_fps"))
    except Exception as e:
        print("Settings test failed:", e)

    print("\n=== 5. Testing Groq Connection Ping ===")
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/settings/test-groq",
            data=json.dumps({}).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        groq_res = json.loads(resp.read().decode())
        print("Groq test response:", groq_res)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"Groq test returned HTTP {e.code}: {err_body}")
    except Exception as e:
        print("Groq ping failed:", e)

    print("\n=== 6. Testing Raw Log File Access ===")
    try:
        resp = urllib.request.urlopen(f"{BASE_URL}/logs/raw", timeout=5)
        log_content = resp.read().decode('utf-8', errors='ignore')
        print(f"studio.log size: {len(log_content)} chars")
        log_lines = log_content.strip().splitlines()
        print(f"Last 3 log lines:")
        for line in log_lines[-3:]:
            print("  ", line)
    except Exception as e:
        print("Raw log test failed:", e)

    print("\n=== ALL TESTS FINISHED ===")

if __name__ == "__main__":
    test_api()
