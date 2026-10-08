"""
GREENRIDE - Application Runner
Runs Uvicorn web server serving both REST API and Frontend SPA on port 8000.
"""

import sys
import os

# Fix Windows console UTF-8 output if possible
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import uvicorn

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
        
    print("=================================================================")
    print(" [GREENRIDE] Sustainable Community Mobility Server")
    print(" [URL] Serving Web Application at: http://localhost:8000")
    print(" [API] Interactive Swagger API Docs at: http://localhost:8000/docs")
    print(" [DEMO] Technofest Demo Accounts Ready (Passenger, Driver, Owner, Admin)")
    print("=================================================================")
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)

