#!/usr/bin/env python3
"""
Setup script for Dependency Parsing Implementation
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Dependency Parsing Implementation...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    print("\n📦 Installing requirements...")
    if not run_command("pip install -r requirements.txt"):
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Download spaCy model
    print("\n🧠 Downloading spaCy English model...")
    if not run_command("python -m spacy download en_core_web_sm"):
        print("❌ Failed to download spaCy model")
        sys.exit(1)
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    os.makedirs("tests", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    print("\n🎉 Setup complete!")
    print("\nTo run the application:")
    print("  streamlit run 0107.py")
    print("\nTo run tests:")
    print("  pytest tests/")

if __name__ == "__main__":
    main()
