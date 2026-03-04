#!/usr/bin/env python3
"""
Discord Channel Relay Bot - Safe Implementation
Relays messages from source channels to target channels
"""

import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordRelayBot(commands.Bot):
    def __init__(self, config_file='relay_config.json'):
        # Use proper bot intents (not self-bot)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(command_prefix='!relay_', intents=intents)
        
        self.config_file = config_file
        self.relay_config = self.load_config()
        self.message_cache = {}  # Prevent duplicate relaying
        
    def load_config(self):
        """Load relay configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default config
            return {
                "relays": [
                    {
                        "source_channel_id": 0,  # Channel to monitor
                        "target_channel_id": 0,  # Channel to send to  
                        "filter_keywords": [],   # Optional: only relay if contains keywords
                        "exclude_keywords": [],  # Optional: don't relay if contains keywords
                        "relay_embeds": True,    # Relay embed messages
                        "relay_attachments": True, # Relay file attachments
                        "add_source_info": True  # Add source channel info
                    }
                ],
                "rate_limits": {
                    "messages_per_minute": 30,  # Stay well under Discord limits
                    "burst_limit": 5            # Max messages in quick succession
                },
                "filters": {
                    "min_message_length": 10,   # Ignore very short messages
                    "ignore_bots": True,        # Don't relay bot messages
                    "ignore_system": True       # Don't relay system messages
                }
            }
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.relay_config, f, indent=2)
    
    async def on_ready(self):
        """Bot startup"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} servers')
        
        # Validate relay configurations
        await self.validate_relays()
    
    async def validate_relays(self):
        """Check if all configured channels are accessible"""
        for relay in self.relay_config['relays']:
            source_channel = self.get_channel(relay['source_channel_id'])
            target_channel = self.get_channel(relay['target_channel_id'])
            
            if not source_channel:
                logger.warning(f"Cannot access source channel {relay['source_channel_id']}")
            if not target_channel:
                logger.warning(f"Cannot access target channel {relay['target_channel_id']}")
            
            if source_channel and target_channel:
                logger.info(f"Relay active: {source_channel.guild.name}#{source_channel.name} → {target_channel.guild.name}#{target_channel.name}")
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore own messages to prevent loops
        if message.author == self.user:
            return
        
        # Check if message is from a monitored channel
        for relay in self.relay_config['relays']:
            if message.channel.id == relay['source_channel_id']:
                await self.relay_message(message, relay)
        
        # Process commands
        await self.process_commands(message)
    
    async def relay_message(self, message, relay_config):
        """Relay a message to target channel"""
        try:
            # Apply filters
            if not self.should_relay_message(message, relay_config):
                return
            
            # Check rate limits
            if not await self.check_rate_limits():
                logger.warning("Rate limit hit, skipping message")
                return
            
            # Get target channel
            target_channel = self.get_channel(relay_config['target_channel_id'])
            if not target_channel:
                logger.error(f"Target channel {relay_config['target_channel_id']} not found")
                return
            
            # Build relay message
            relay_content = await self.build_relay_message(message, relay_config)
            
            # Send to target channel
            await target_channel.send(**relay_content)
            
            # Log successful relay
            logger.info(f"Relayed message from {message.channel.guild.name}#{message.channel.name}")
            
        except discord.HTTPException as e:
            logger.error(f"Failed to relay message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error relaying message: {e}")
    
    def should_relay_message(self, message, config):
        """Check if message should be relayed based on filters"""
        filters = self.relay_config['filters']
        
        # Ignore bot messages if configured
        if filters.get('ignore_bots', True) and message.author.bot:
            return False
        
        # Ignore system messages if configured
        if filters.get('ignore_system', True) and message.type != discord.MessageType.default:
            return False
        
        # Check minimum message length
        if len(message.content) < filters.get('min_message_length', 0):
            return False
        
        # Check keyword filters
        if config.get('filter_keywords'):
            if not any(keyword.lower() in message.content.lower() for keyword in config['filter_keywords']):
                return False
        
        # Check exclude keywords
        if config.get('exclude_keywords'):
            if any(keyword.lower() in message.content.lower() for keyword in config['exclude_keywords']):
                return False
        
        return True
    
    async def build_relay_message(self, message, config):
        """Build the message to send to target channel"""
        relay_data = {}
        
        # Base content
        content = message.content
        
        # Add source info if configured
        if config.get('add_source_info', True):
            source_info = f"**[{message.guild.name} #{message.channel.name}]** {message.author.display_name}:\n"
            content = source_info + content
        
        relay_data['content'] = content[:2000]  # Discord character limit
        
        # Handle embeds
        if config.get('relay_embeds', True) and message.embeds:
            relay_data['embeds'] = message.embeds[:1]  # Relay first embed
        
        # Handle attachments (as URLs, since we can't re-upload)
        if config.get('relay_attachments', True) and message.attachments:
            attachment_urls = '\n'.join([att.url for att in message.attachments])
            relay_data['content'] += f"\n📎 Attachments:\n{attachment_urls}"
        
        return relay_data
    
    async def check_rate_limits(self):
        """Simple rate limiting to avoid hitting Discord limits"""
        current_time = datetime.now()
        
        # Clean old entries from cache
        cutoff_time = current_time - timedelta(minutes=1)
        self.message_cache = {k: v for k, v in self.message_cache.items() if v > cutoff_time}
        
        # Check if we're under rate limit
        if len(self.message_cache) >= self.relay_config['rate_limits']['messages_per_minute']:
            return False
        
        # Add current message to cache
        self.message_cache[current_time.timestamp()] = current_time
        return True
    
    @commands.command(name='add_relay')
    @commands.has_permissions(administrator=True)
    async def add_relay(self, ctx, source_channel_id: int, target_channel_id: int):
        """Add a new relay configuration"""
        new_relay = {
            "source_channel_id": source_channel_id,
            "target_channel_id": target_channel_id,
            "filter_keywords": [],
            "exclude_keywords": [],
            "relay_embeds": True,
            "relay_attachments": True,
            "add_source_info": True
        }
        
        self.relay_config['relays'].append(new_relay)
        self.save_config()
        
        await ctx.send(f"✅ Added relay: <#{source_channel_id}> → <#{target_channel_id}>")
    
    @commands.command(name='list_relays')
    @commands.has_permissions(administrator=True)
    async def list_relays(self, ctx):
        """List all active relays"""
        if not self.relay_config['relays']:
            await ctx.send("No relays configured.")
            return
        
        relay_list = []
        for i, relay in enumerate(self.relay_config['relays']):
            source_ch = self.get_channel(relay['source_channel_id'])
            target_ch = self.get_channel(relay['target_channel_id'])
            
            source_name = f"{source_ch.guild.name}#{source_ch.name}" if source_ch else "Unknown"
            target_name = f"{target_ch.guild.name}#{target_ch.name}" if target_ch else "Unknown"
            
            relay_list.append(f"{i+1}. {source_name} → {target_name}")
        
        await ctx.send("**Active Relays:**\n" + '\n'.join(relay_list))


def create_config_file():
    """Create a sample configuration file"""
    config = {
        "bot_token": "YOUR_BOT_TOKEN_HERE",
        "relays": [
            {
                "source_channel_id": 123456789012345678,  # Replace with actual channel ID
                "target_channel_id": 876543210987654321,  # Replace with actual channel ID
                "filter_keywords": [],
                "exclude_keywords": ["spam", "test"],
                "relay_embeds": True,
                "relay_attachments": True,
                "add_source_info": True
            }
        ],
        "rate_limits": {
            "messages_per_minute": 30,
            "burst_limit": 5
        },
        "filters": {
            "min_message_length": 10,
            "ignore_bots": True,
            "ignore_system": True
        }
    }
    
    with open('relay_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Created relay_config.json - Please edit with your bot token and channel IDs")

async def main():
    """Run the bot"""
    # Load bot token from config
    try:
        with open('relay_config.json', 'r') as f:
            config = json.load(f)
            token = config.get('bot_token')
    except FileNotFoundError:
        print("Configuration file not found. Creating sample config...")
        create_config_file()
        return
    
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("Please set your bot token in relay_config.json")
        return
    
    # Create and run bot
    bot = DiscordRelayBot()
    
    try:
        await bot.start(token)
    except discord.LoginFailure:
        print("Invalid bot token. Please check your configuration.")
    except KeyboardInterrupt:
        print("Bot stopped.")
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())