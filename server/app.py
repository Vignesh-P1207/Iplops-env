import sys
import os
from pathlib import Path

# Add the parent directory to sys.path so 'app.main' can be found
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app

def run():
    import uvicorn
    print("Starting server from server/app.py...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run()
