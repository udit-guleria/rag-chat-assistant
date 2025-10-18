#!/usr/bin/env python3
"""
Simple script to run the Streamlit UI for the RAG application.
This script ensures the database is initialized before starting the UI.
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
    print("🚀 Starting RAG Chat Assistant...")
    
    # Check if database exists
    if not check_database():
        print("❌ Database not found. Please run 'python create_database.py' first.")
        print("   This will process the documents and create the vector database.")
        sys.exit(1)
    
    print("✅ Database found. Starting web interface...")
    print("🌐 The app will open in your default browser.")
    print("📝 You can also access it at: http://localhost:8501")
    print("\n" + "="*50)
    
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

