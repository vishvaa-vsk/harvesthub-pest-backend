#!/usr/bin/env python3
"""
HarvestHub FastAPI Deployment Manager
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...")
    
    # Check for required files
    required_files = [
        "main_fastapi.py",
        "app/model.py",
        "app/helpers_async.py",
        "app/schemas.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    # Check for model files
    model_files = [
        "app/data/model.h5",
        "app/data/labels.txt"
    ]
    
    missing_model_files = []
    for file in model_files:
        if not Path(file).exists():
            missing_model_files.append(file)
    
    if missing_model_files:
        print("⚠️  Missing model files (prediction will fail):")
        for file in missing_model_files:
            print(f"   - {file}")
    
    # Check for Firebase key
    if not Path("app/firebase-key.json").exists():
        print("⚠️  Firebase key not found (caching will be disabled)")
        print("   Create app/firebase-key.json with your Firebase credentials")
    
    # Check for environment variables
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("   Copy .env.template to .env and configure your settings")
    
    print("✅ Environment check completed")
    return True

def start_development_server():
    """Start development server with hot reload"""
    print("🚀 Starting development server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main_fastapi:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Development server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start development server: {e}")

def start_production_server():
    """Start production server"""
    print("🚀 Starting production server...")
    try:
        subprocess.run([sys.executable, "start_fastapi.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Production server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start production server: {e}")

def run_tests():
    """Run performance tests"""
    print("🧪 Running tests...")
    try:
        subprocess.run([sys.executable, "performance_test.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="HarvestHub FastAPI Deployment Manager")
    parser.add_argument("command", choices=[
        "install", "check", "dev", "prod", "test", "setup"
    ], help="Command to run")
    
    args = parser.parse_args()
    
    print("🌾 HarvestHub FastAPI Deployment Manager")
    print("="*50)
    
    if args.command == "install":
        install_dependencies()
    
    elif args.command == "check":
        check_environment()
    
    elif args.command == "dev":
        if check_environment():
            start_development_server()
    
    elif args.command == "prod":
        if check_environment():
            start_production_server()
    
    elif args.command == "test":
        run_tests()
    
    elif args.command == "setup":
        print("🔧 Setting up HarvestHub FastAPI...")
        if install_dependencies() and check_environment():
            print("\n✅ Setup completed successfully!")
            print("\n📋 Next steps:")
            print("   1. Configure .env file with your API keys")
            print("   2. Add Firebase credentials to app/firebase-key.json")
            print("   3. Run: python deploy.py dev")
        else:
            print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
