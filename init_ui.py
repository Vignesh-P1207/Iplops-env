"""
Initialize environment for UI demo
"""
import requests

BASE_URL = "http://localhost:8000"

print("Initializing IPLOps-Env for UI...")

# Reset to Task 1
response = requests.post(f"{BASE_URL}/reset", json={"task_id": 1})
if response.status_code == 200:
    print("✅ Environment initialized successfully!")
    print(f"✅ UI available at: http://localhost:8000")
    print(f"✅ API Docs at: http://localhost:8000/docs")
else:
    print("❌ Failed to initialize environment")
