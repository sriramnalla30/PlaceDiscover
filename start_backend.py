"""
Start Backend Server (SerpStack Only)
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting SerpStack-Only Backend...")
    print("📡 Server: http://localhost:8002")
    print("📚 Docs: http://localhost:8002/docs")
    print("="*80)
    
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8002,
        reload=False
    )
