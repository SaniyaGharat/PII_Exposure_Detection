"""
Runner script to launch the PII Exposure Detection FastAPI Backend Server.
Usage:
    python run_backend.py [--port 8000] [--host 0.0.0.0]
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start PII Exposure Detection Backend API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    parser.add_argument("--reload", action="store_true", default=True, help="Enable auto-reload on code change")
    args = parser.parse_args()

    print("\n" + "=" * 65)
    print("  PII EXPOSURE DETECTION & BLOCKCHAIN AUDIT BACKEND")
    print(f"  Server URL:    http://localhost:{args.port}")
    print(f"  API Docs:      http://localhost:{args.port}/docs")
    print(f"  Samples API:   http://localhost:{args.port}/api/samples")
    print("=" * 65 + "\n")

    uvicorn.run("backend.main:app", host=args.host, port=args.port, reload=args.reload)
