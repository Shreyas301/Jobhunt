#!/bin/bash
# JobHunter Pro - Linux/Mac Launch Script

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║           🚀 JobHunter Pro - Launcher                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found! Please install Python 3.8+"
    echo "   macOS: brew install python3"
    echo "   Linux: apt-get install python3"
    exit 1
fi

echo "✅ Python detected: $(python3 --version)"

# Check if requirements are installed
python3 -c "import streamlit; import fitz; import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed!"
fi

# Create .env if doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "🔑 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "📝 IMPORTANT: Open .env and add your Firecrawl API key!"
    echo "   Get free key at: https://firecrawl.dev"
    echo ""
    sleep 3
fi

# Launch the app
echo ""
echo "🚀 Starting JobHunter Pro..."
echo "   📍 Browser will open at: http://localhost:8501"
echo "   📱 From phone: Get your IP (ifconfig) and go to http://YOUR_IP:8501"
echo ""

streamlit run app.py
