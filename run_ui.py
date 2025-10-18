#!/usr/bin/env python3
"""
Universal launcher script for the Multi-Format Document RAG application.
This version supports PDF, Word, PowerPoint, Excel, CSV, JSON, HTML, Markdown, and Text files.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_database():
    """Check if the Chroma database exists"""
    chroma_path = Path("chroma")
    return chroma_path.exists() and any(chroma_path.iterdir())

def main():
    print("🚀 Starting Universal Document RAG Assistant...")
    print("📄 Supporting: PDF, Word, PowerPoint, Excel, CSV, JSON, HTML, Markdown, Text")
    
    # Check if database exists (optional for this version)
    if not check_database():
        print("ℹ️  No existing database found. You can upload documents through the web interface.")
    else:
        print("✅ Found existing database with documents.")
    
    print("🌐 The app will open in your default browser.")
    print("📝 You can also access it at: http://localhost:8501")
    print("📁 Upload your documents in various formats through the web interface!")
    print("\n" + "="*60)
    
    # Run Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
