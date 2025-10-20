#!/usr/bin/env python3
"""
Setup script for Universal Document RAG Assistant
This script helps users set up the project quickly and easily.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚀 Universal Document RAG Assistant - Setup")
    print("=" * 60)
    print("This script will help you set up the project quickly.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_git():
    """Check if Git is available"""
    print("🔍 Checking Git...")
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Git not found. You can still use the project without Git.")
        return False

def create_virtual_environment():
    """Create virtual environment"""
    print("🔧 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def get_activation_command():
    """Get the correct activation command for the platform"""
    if platform.system() == "Windows":
        return ".venv\\Scripts\\activate"
    else:
        return "source .venv/bin/activate"

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    # Get the correct pip path
    if platform.system() == "Windows":
        pip_path = ".venv\\Scripts\\pip"
    else:
        pip_path = ".venv/bin/pip"
    
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment_file():
    """Set up environment file"""
    print("🔑 Setting up environment file...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    print("Please enter your OpenAI API key:")
    api_key = input("OpenAI API Key: ").strip()
    
    if not api_key:
        print("⚠️  No API key provided. You'll need to set it manually later.")
        api_key = "your_openai_api_key_here"
    
    with open(".env", "w") as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
    
    print("✅ .env file created")
    return True

def create_sample_data():
    """Create sample data directory"""
    print("📁 Setting up data directories...")
    
    directories = ["data", "data/uploads", "data/books"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Data directories created")
    return True

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    try:
        # Test import of main modules
        sys.path.insert(0, str(Path.cwd()))
        
        # Test basic imports
        import streamlit
        import langchain
        import chromadb
        
        print("✅ All required modules can be imported")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print()
    print("1. Activate virtual environment:")
    print(f"   {get_activation_command()}")
    print()
    print("2. Launch the application:")
    print("   python run_ui.py")
    print("   # OR double-click start_ui.bat (Windows)")
    print()
    print("3. Open your browser to:")
    print("   http://localhost:8501")
    print()
    print("4. Upload documents and start asking questions!")
    print()
    print("📚 Documentation:")
    print("   - README.md: Quick start guide")
    print("   - PROJECT_DOCUMENTATION.md: Complete documentation")
    print("   - DEVELOPER_GUIDE.md: Developer information")
    print("   - SUPPORTED_FORMATS.md: File format details")
    print()
    print("🆘 Need help?")
    print("   - Check the documentation files")
    print("   - Open an issue on GitHub")
    print("   - Review the troubleshooting section")
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    check_git()
    
    # Setup steps
    steps = [
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment", setup_environment_file),
        ("Creating data directories", create_sample_data),
        ("Testing installation", test_installation),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔧 {step_name}...")
        if not step_func():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print_next_steps()

if __name__ == "__main__":
    main()
