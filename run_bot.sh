#!/bin/bash

# Activate virtual environment and run the Discord relay bot
echo "🤖 Starting Discord Relay Bot..."

if [ ! -d "discord_relay_env" ]; then
    echo "❌ Virtual environment not found. Run ./install_and_run.sh first"
    exit 1
fi

# Check if config file exists and is configured
if [ ! -f "relay_config.json" ]; then
    echo "❌ relay_config.json not found. Run setup first."
    exit 1
fi

# Check if bot token is configured
if grep -q "YOUR_BOT_TOKEN_HERE" relay_config.json; then
    echo "❌ Bot token not configured in relay_config.json"
    echo "   Edit the file and add your Discord bot token"
    exit 1
fi

# Activate virtual environment and run bot
source discord_relay_env/bin/activate
python3 discord_relay_bot.py