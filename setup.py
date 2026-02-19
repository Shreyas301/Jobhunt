#!/usr/bin/env python3
"""
JobHunter Pro - Setup and Utility Helper Script
This script helps with initial setup and provides useful utilities
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                 🚀 JobHunter Pro Setup                   ║
    ║        CV-Based Job Discovery Application               ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_env_file():
    """Create .env file if doesn't exist"""
    if not os.path.exists(".env"):
        print("\n🔑 Setting up environment variables...")
        print("   - Copy .env.example to .env")
        print("   - Add your Firecrawl API key")
        subprocess.run([
            "copy" if sys.platform == "win32" else "cp",
            ".env.example",
            ".env"
        ], shell=True if sys.platform == "win32" else False)
        print("✅ .env file created! (Update with your API key)")
        
        with open(".env", "r") as f:
            content = f.read()
            if "your_api_key_here" in content:
                print("📝 Instructions:")
                print("   1. Open .env file")
                print("   2. Replace 'your_api_key_here' with your actual Firecrawl API key")
                print("   3. Save the file")
                print("   4. Restart the app")
    else:
        print("✅ .env file already exists")

def run_app():
    """Run the Streamlit app"""
    print("\n🚀 Launching JobHunter Pro...")
    print("   - Opening http://localhost:8501")
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it first:")
        print("   pip install streamlit")

def show_mobile_instructions():
    """Show instructions for accessing app on mobile"""
    print("\n📱 Access on Mobile/Other Devices:")
    print("   1. Get your IP address:")
    if sys.platform == "win32":
        print("      - Run: ipconfig")
        print("      - Look for 'IPv4 Address'")
    else:
        print("      - Run: ifconfig or hostname -I")
    print("   2. In phone browser, go to: http://<YOUR_IP>:8501")
    print("   Example: http://192.168.1.100:8501")

def main():
    """Main setup flow"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_env_file()
    
    # Show instructions
    show_mobile_instructions()
    
    # Ask to continue
    print("\n" + "="*60)
    response = input("Ready to launch app? (y/n): ").strip().lower()
    
    if response == 'y':
        run_app()
    else:
        print("✅ Setup complete! To run later, use: streamlit run app.py")

if __name__ == "__main__":
    main()
