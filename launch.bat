@echo off
REM JobStream Pro - Windows Launch Script

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║           🚀 JobStream Pro - Launcher                 ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    echo    Download from: https://www.python.org
    pause
    exit /b 1
)

echo ✅ Python detected

REM Check if requirements are installed
python -c "import streamlit; import fitz; import requests" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed!
)

REM Create .env if doesn't exist
if not exist ".env" (
    echo.
    echo 🔑 Creating .env file...
    copy .env.example .env >nul
    echo ✅ .env file created
    echo.
    echo 📝 IMPORTANT: Open .env and add your Firecrawl API key!
    echo    Get free key at: https://firecrawl.dev
    echo.
    timeout /t 3 >nul
)

REM Launch the app
echo.
echo 🚀 Starting JobStream Pro...
echo    📍 Browser will open at: http://localhost:8501
echo    📱 From phone: Get your IP and go to http://YOUR_IP:8501
echo.

python -m streamlit run app.py

pause
