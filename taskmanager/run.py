import os
import sys
from uvicorn import run

# Ensure the backend package root is importable from the project root.
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8000)
