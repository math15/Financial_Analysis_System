#!/usr/bin/env python3
"""
Setup script for AI-Enhanced Insurance Quote Comparison System
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old. Requires Python 3.8+")
        return False

def setup_backend():
    """Set up backend dependencies"""
    print("\n🔧 Setting up Backend...")
    
    # Check if we're in the right directory
    if not os.path.exists("backend"):
        print("❌ Backend directory not found. Run this script from the project root.")
        return False
    
    # Install backend dependencies
    if not run_command("cd backend && pip install -r requirements.txt", "Installing backend dependencies"):
        return False
    
    # Create necessary directories
    backend_dirs = ["backend/uploads", "backend/reports"]
    for directory in backend_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    return True

def setup_frontend():
    """Set up frontend dependencies"""
    print("\n🎨 Setting up Frontend...")
    
    # Check if package.json exists
    if not os.path.exists("package.json"):
        print("⚠️ package.json not found. Frontend setup skipped.")
        return True
    
    # Install frontend dependencies
    if not run_command("npm install", "Installing frontend dependencies"):
        print("⚠️ Frontend setup failed. You can set it up manually with 'npm install'")
        return True  # Don't fail the whole setup for frontend issues
    
    return True

def create_env_template():
    """Create environment template file"""
    print("\n📝 Creating environment template...")
    
    env_template = """# LLMWhisperer Configuration (Required)
LLM_API_KEY=your_llmwhisperer_api_key_here
LLM_API_URL=https://llmwhisperer-api.us-central.unstract.com/api/v2

# Optional LLM APIs for enhanced analysis
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000

# Production Domains (already configured in config.py)
# Frontend: https://mailbroker.ddns.net
# Backend: https://apimailbroker.ddns.net

# Processing Settings
USE_LLM_API=true
FALLBACK_TO_LOCAL=true
LOCAL_PROCESSING_ONLY=false

# File Upload Settings
MAX_FILE_SIZE=20971520  # 20MB
PROCESSING_TIMEOUT=300  # 5 minutes

# Logging
LLMWHISPERER_LOGGING_LEVEL=INFO
"""
    
    env_file = "backend/.env.example"
    with open(env_file, "w") as f:
        f.write(env_template)
    
    print(f"✅ Environment template created: {env_file}")
    print("   Copy this to backend/.env and configure your API keys")
    
    return True

def run_tests():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        # Import and run our test
        sys.path.append('.')
        import test_system
        test_system.test_system()
        return True
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AI-Enhanced Insurance Quote Comparison System Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    setup_frontend()  # Don't fail on frontend issues
    
    # Create environment template
    create_env_template()
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Configure API keys in backend/.env (copy from backend/.env.example)")
    print("2. Get LLMWhisperer API key from: https://unstract.com/")
    print("3. Start backend: cd backend && python main.py")
    print("4. Start frontend: npm run dev")
    print("5. Test system: python test_system.py")
    print("\n🔧 Optional LLM APIs for enhanced analysis:")
    print("   - OpenAI: https://platform.openai.com/api-keys")
    print("   - Anthropic: https://console.anthropic.com/")
    print("   - Google: https://makersuite.google.com/app/apikey")
    
    # Ask if user wants to run tests
    try:
        response = input("\n❓ Run system tests now? (y/N): ").lower()
        if response in ['y', 'yes']:
            run_tests()
    except KeyboardInterrupt:
        print("\n👋 Setup completed!")

if __name__ == "__main__":
    main() 