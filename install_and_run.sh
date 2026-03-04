#!/bin/bash

# Discord Relay Bot Installation and Run Script
echo "🤖 Discord Relay Bot Setup"
echo "========================="

# Check if running on correct system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✅ Linux detected"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ macOS detected"  
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "✅ Windows detected"
else
    echo "⚠️ Unknown OS: $OSTYPE"
fi

# Install system packages if needed (Ubuntu/Debian)
if command -v apt >/dev/null 2>&1; then
    echo "📦 Installing Python venv support..."
    sudo apt update
    sudo apt install -y python3-venv python3-pip
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "discord_relay_env" ]; then
    python3 -m venv discord_relay_env
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install packages
echo "📦 Installing Discord.py..."
source discord_relay_env/bin/activate
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 TO RUN THE BOT:"
echo "1. Edit relay_config.json with your bot token and channel IDs"
echo "2. Run: ./run_bot.sh"
echo ""
echo "📋 Don't forget to:"
echo "  - Create Discord bot at https://discord.com/developers/applications"
echo "  - Add bot to your servers with proper permissions"
echo "  - Get channel IDs (enable Developer Mode in Discord)"