#!/bin/bash

# Discord Self-Bot Relay Runner
echo "🕵️ Starting Discord Self-Bot Relay..."
echo "⚠️  WARNING: Self-bots violate Discord TOS"

# Check if config exists
if [ ! -f "selfbot_config.json" ]; then
    echo "📝 Creating initial configuration..."
    python3 discord_selfbot_relay.py
    echo ""
    echo "✅ Configuration created!"
    echo "📋 Next steps:"
    echo "   1. Get your Discord user token (see SELFBOT_SETUP.md)"
    echo "   2. Edit selfbot_config.json with your token and channel IDs"
    echo "   3. Run this script again"
    exit 0
fi

# Check if token is configured
if grep -q "YOUR_USER_TOKEN_HERE" selfbot_config.json; then
    echo "❌ User token not configured in selfbot_config.json"
    echo "   Follow instructions in SELFBOT_SETUP.md to get your Discord token"
    exit 1
fi

# Check if channel IDs are configured
if grep -q '"source_channel_id": 0' selfbot_config.json; then
    echo "❌ Channel IDs not configured in selfbot_config.json"
    echo "   Add your source and target channel IDs"
    exit 1
fi

# Final warning
echo ""
echo "🚨 FINAL WARNING:"
echo "   Self-bots violate Discord Terms of Service"
echo "   Your account could be banned if detected"
echo "   Use conservative settings and monitor for warnings"
echo ""
read -p "Continue anyway? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Install dependencies if needed
if ! python3 -c "import discord" 2>/dev/null; then
    echo "📦 Installing discord.py..."
    pip3 install discord.py --user --quiet
fi

# Run the self-bot
echo ""
echo "🚀 Starting self-bot relay..."
echo "   Press Ctrl+C to stop"
echo "   Monitor for any Discord warnings!"
echo ""

python3 discord_selfbot_relay.py