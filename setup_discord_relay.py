#!/usr/bin/env python3
"""
Quick setup script for Discord Relay Bot
"""

import json
import os
import sys

def create_sample_config():
    """Create a sample configuration file with explanations"""
    
    config = {
        "bot_token": "YOUR_BOT_TOKEN_HERE",
        "_comment_token": "Get this from https://discord.com/developers/applications -> Your Bot -> Bot -> Token",
        
        "relays": [
            {
                "source_channel_id": 0,
                "target_channel_id": 0,
                "_comment_ids": "Right-click channel in Discord -> Copy ID (need Developer Mode enabled)",
                
                "filter_keywords": [],
                "_comment_filter": "Only relay messages containing these words (empty = relay all)",
                
                "exclude_keywords": ["spam", "test"],
                "_comment_exclude": "Don't relay messages containing these words",
                
                "relay_embeds": True,
                "relay_attachments": True,
                "add_source_info": True,
                "_comment_options": "What to include in relayed messages"
            }
        ],
        
        "rate_limits": {
            "messages_per_minute": 30,
            "_comment_rate": "Stay well under Discord's rate limits"
        },
        
        "filters": {
            "min_message_length": 5,
            "ignore_bots": True,
            "ignore_system": True,
            "_comment_filters": "Global filters applied to all relays"
        }
    }
    
    with open('relay_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created relay_config.json")
    return config

def get_channel_id_help():
    """Show instructions for getting channel IDs"""
    print("""
🔍 HOW TO GET CHANNEL IDs:

1. Enable Developer Mode:
   Discord → Settings → Advanced → Developer Mode ✅

2. Get Channel ID:
   Right-click any channel → "Copy ID"

3. The ID looks like: 123456789012345678 (18 digits)

Examples:
- Source channel (you want to monitor): 123456789012345678
- Target channel (where messages go): 987654321098765432
""")

def setup_bot_instructions():
    """Show bot creation instructions"""
    print("""
🤖 DISCORD BOT SETUP:

1. Go to: https://discord.com/developers/applications
2. Click: "New Application" 
3. Give it a name like "Channel Relay Bot"
4. Go to "Bot" section → "Add Bot"
5. Copy the Bot Token (keep this secret!)
6. Enable these Intents:
   - Message Content Intent ✅
   - Server Members Intent ✅

7. Go to OAuth2 → URL Generator:
   - Scopes: bot ✅
   - Bot Permissions:
     • Read Messages ✅
     • Send Messages ✅  
     • Read Message History ✅
     • Embed Links ✅

8. Copy the generated OAuth URL
9. Use it to add the bot to your servers
""")

def validate_config(config):
    """Check if configuration looks valid"""
    issues = []
    
    if config.get('bot_token') == 'YOUR_BOT_TOKEN_HERE':
        issues.append("❌ Bot token not set")
    
    if not config.get('relays'):
        issues.append("❌ No relays configured")
    else:
        for i, relay in enumerate(config['relays']):
            if not relay.get('source_channel_id'):
                issues.append(f"❌ Relay {i+1}: Missing source channel ID")
            if not relay.get('target_channel_id'):
                issues.append(f"❌ Relay {i+1}: Missing target channel ID")
    
    if issues:
        print("\n🚨 CONFIGURATION ISSUES:")
        for issue in issues:
            print(f"  {issue}")
        return False
    
    print("\n✅ Configuration looks good!")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    
    try:
        import discord
        print("✅ discord.py already installed")
    except ImportError:
        print("Installing discord.py...")
        os.system(f"{sys.executable} -m pip install discord.py")
    
    try:
        import aiohttp
        print("✅ aiohttp already installed")
    except ImportError:
        print("Installing aiohttp...")
        os.system(f"{sys.executable} -m pip install aiohttp")

def main():
    print("🔧 DISCORD RELAY BOT SETUP")
    print("=" * 30)
    
    # Check if config exists
    if os.path.exists('relay_config.json'):
        print("📁 Found existing relay_config.json")
        
        try:
            with open('relay_config.json', 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"❌ Error reading config: {e}")
            config = create_sample_config()
    else:
        print("📝 Creating new configuration...")
        config = create_sample_config()
    
    # Show setup instructions
    print("\n" + "=" * 50)
    setup_bot_instructions()
    
    print("\n" + "=" * 50)
    get_channel_id_help()
    
    # Validate current config
    print("\n" + "=" * 50)
    print("🔍 CHECKING CURRENT CONFIGURATION:")
    validate_config(config)
    
    # Install dependencies
    print("\n" + "=" * 50)
    install_dependencies()
    
    # Final instructions
    print("\n" + "=" * 50)
    print("🚀 NEXT STEPS:")
    print()
    print("1. Edit relay_config.json with your bot token and channel IDs")
    print("2. Run: python3 discord_relay_bot.py")
    print()
    print("📋 Quick Checklist:")
    print("  □ Created Discord bot application")
    print("  □ Added bot to source and target servers") 
    print("  □ Copied bot token to relay_config.json")
    print("  □ Added channel IDs to relay_config.json")
    print("  □ Tested with a few messages")
    print()
    print("⚠️  Remember: You need admin permissions in both servers")
    print("   or ask server admins to add your bot!")

if __name__ == "__main__":
    main()