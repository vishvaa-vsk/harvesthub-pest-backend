#!/usr/bin/env python3
"""
Production startup script for HarvestHub FastAPI server
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def start_server():
    """Start the FastAPI server with production configuration"""
      # Configuration
    config = {
        "app": "main:app",
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT", 8000)),
        "workers": int(os.getenv("WORKERS", 4)),
        "log_level": os.getenv("LOG_LEVEL", "info"),
        "reload": os.getenv("RELOAD", "false").lower() == "true",
        "access_log": True,
        "timeout_keep_alive": 120,
        "limit_max_requests": 1000,
    }
    
    print("🚀 Starting HarvestHub FastAPI Server")
    print(f"   Host: {config['host']}")
    print(f"   Port: {config['port']}")
    print(f"   Workers: {config['workers']}")
    print(f"   Log Level: {config['log_level']}")
    print(f"   Reload: {config['reload']}")
    print("="*50)
    
    # Start server
    uvicorn.run(
        config["app"],
        host=config["host"],
        port=config["port"],
        workers=config["workers"] if not config["reload"] else 1,
        log_level=config["log_level"],
        reload=config["reload"],
        access_log=config["access_log"],
        timeout_keep_alive=config["timeout_keep_alive"],
        limit_max_requests=config["limit_max_requests"]
    )

if __name__ == "__main__":
    start_server()
