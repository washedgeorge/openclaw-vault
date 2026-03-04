#!/usr/bin/env python3
"""
Discord Self-Bot Relay - STEALTH VERSION
Uses your Discord account to relay messages between channels
⚠️ WARNING: Self-bots violate Discord TOS - use at your own risk
"""

import discord
import asyncio
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configure logging to be minimal (avoid detection)
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class StealthDiscordRelay:
    def __init__(self, config_file='selfbot_config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        self.client = None
        self.message_history = {}
        self.daily_message_count = {}
        self.last_activity = {}
        self.session_start = datetime.now()
        self.idle_until = None  # Track idle periods
        self.last_idle_check = datetime.now()
        
    def load_config(self):
        """Load configuration with stealth defaults"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "user_token": "YOUR_USER_TOKEN_HERE",
                "relays": [
                    {
                        "source_channel_id": 0,
                        "target_channel_id": 0,
                        "filter_keywords": [],
                        "exclude_keywords": ["@everyone", "@here"],
                        "relay_embeds": False,  # Safer to avoid
                        "relay_attachments": False,  # Safer to avoid
                        "add_source_info": True,
                        "enabled": True
                    }
                ],
                "stealth_settings": {
                    "min_delay_minutes": 1,      # Minimum 1 minute between relays
                    "max_delay_minutes": 5,      # Maximum 5 minutes between relays  
                    "messages_per_hour": 15,     # Reasonable: 15 messages/hour max
                    "messages_per_day": 120,     # Daily cap to avoid patterns
                    "random_delays": True,       # Add random delays
                    "typing_simulation": False,  # Never simulate typing
                    "active_hours_only": True,   # Only relay during active hours
                    "active_start": 8,           # 8 AM start
                    "active_end": 23,            # 11 PM end
                    "idle_periods": False,       # No long idle periods
                    "idle_min_minutes": 10,      # Shorter idle periods if enabled
                    "idle_max_minutes": 30,      # Max 30 min idle (not 2 hours)
                    "weekend_slower": False,     # Same speed on weekends
                    "human_pattern": False       # Consistent timing pattern
                },
                "safety_filters": {
                    "min_message_length": 10,        # Minimum message length
                    "max_message_length": 1500,      # Maximum message length  
                    "ignore_bots": True,
                    "ignore_system": True,
                    "ignore_mentions": True,         # Don't relay @mentions (risky)
                    "ignore_commands": True,         # Don't relay bot commands
                    "ignore_links": False,           # Allow links
                    "ignore_caps": False,            # Allow caps messages
                    "ignore_repeats": False,         # Allow similar messages
                    "require_engagement": False,     # Don't require reactions
                    "max_links_per_message": 3,      # Allow up to 3 links
                    "caps_threshold": 0.8            # Allow more caps (80% threshold)
                }
            }
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    async def setup_client(self):
        """Initialize Discord client as user account"""
        self.client = discord.Client()
        
        @self.client.event
        async def on_ready():
            logger.info(f'Selfbot logged in as {self.client.user}')
            print(f'🤖 Stealth relay active for {self.client.user.name}')
            
        @self.client.event  
        async def on_message(message):
            await self.handle_message(message)
    
    async def handle_message(self, message):
        """Process incoming messages for potential relay"""
        try:
            # Ignore own messages
            if message.author.id == self.client.user.id:
                return
            
            # Check if message is from a monitored channel
            for relay in self.config['relays']:
                if not relay.get('enabled', True):
                    continue
                    
                if message.channel.id == relay['source_channel_id']:
                    await self.relay_message(message, relay)
                    
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def should_relay_message(self, message, relay_config) -> bool:
        """Determine if message should be relayed (with safety checks)"""
        safety = self.config['safety_filters']
        
        # Basic safety filters
        if safety.get('ignore_bots', True) and message.author.bot:
            return False
            
        if safety.get('ignore_system', True) and message.type != discord.MessageType.default:
            return False
        
        # Length filters
        content_length = len(message.content)
        if content_length < safety.get('min_message_length', 0):
            return False
        if content_length > safety.get('max_message_length', 2000):
            return False
        
        # Mention filters (avoid triggering notifications)
        if safety.get('ignore_mentions', True):
            if '@everyone' in message.content or '@here' in message.content:
                return False
            if len(message.mentions) > 0 or len(message.role_mentions) > 0:
                return False
        
        # Command filters
        if safety.get('ignore_commands', True):
            if message.content.startswith(('!', '/', '?', '$', '.', '-', '+', '=')):
                return False
        
        # Link filtering (if enabled)
        if safety.get('ignore_links', False):
            import re
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
            max_links = safety.get('max_links_per_message', 3)
            if len(links) > max_links:
                return False
        
        # Caps filter (if enabled)
        if safety.get('ignore_caps', False):
            caps_count = sum(1 for c in message.content if c.isupper())
            total_alpha = sum(1 for c in message.content if c.isalpha())
            if total_alpha > 0:
                caps_ratio = caps_count / total_alpha
                if caps_ratio > safety.get('caps_threshold', 0.8):
                    return False
        
        # Engagement filter (if enabled)
        if safety.get('require_engagement', False):
            if len(message.reactions) == 0:
                message_age = (datetime.now() - message.created_at.replace(tzinfo=None)).total_seconds()
                if message_age > 300:  # 5 minutes old with no engagement
                    return False
        
        # Keyword filters
        if relay_config.get('filter_keywords'):
            if not any(kw.lower() in message.content.lower() for kw in relay_config['filter_keywords']):
                return False
        
        if relay_config.get('exclude_keywords'):
            if any(kw.lower() in message.content.lower() for kw in relay_config['exclude_keywords']):
                return False
        
        # Rate limiting check
        if not await self.check_rate_limits(relay_config):
            return False
        
        # Active hours check
        if not self.is_active_hours():
            return False
        
        return True
    
    async def check_rate_limits(self, relay_config) -> bool:
        """Balanced rate limiting - 1-5 minute delays"""
        now = datetime.now()
        stealth = self.config['stealth_settings']
        
        # Clean old entries (hourly and daily)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        self.message_history = {k: v for k, v in self.message_history.items() if v > hour_ago}
        self.daily_message_count = {k: v for k, v in self.daily_message_count.items() if v > day_ago}
        
        # Check daily limit
        daily_limit = stealth.get('messages_per_day', 120)
        if len(self.daily_message_count) >= daily_limit:
            return False
        
        # Check hourly limit
        hourly_limit = stealth.get('messages_per_hour', 15)
        if len(self.message_history) >= hourly_limit:
            return False
        
        # Check minimum delay between messages
        channel_key = relay_config['source_channel_id']
        if channel_key in self.last_activity:
            time_diff = (now - self.last_activity[channel_key]).total_seconds()
            min_delay = stealth.get('min_delay_minutes', 1) * 60
            if time_diff < min_delay:
                return False
        
        return True
    
    def is_active_hours(self) -> bool:
        """Check if current time is within active hours"""
        stealth = self.config['stealth_settings']
        if not stealth.get('active_hours_only', True):
            return True
        
        current_hour = datetime.now().hour
        start_hour = stealth.get('active_start', 8)
        end_hour = stealth.get('active_end', 23)
        
        return start_hour <= current_hour <= end_hour
    
    async def relay_message(self, message, relay_config):
        """Relay message with stealth features"""
        try:
            if not await self.should_relay_message(message, relay_config):
                return
            
            # Get target channel
            target_channel = self.client.get_channel(relay_config['target_channel_id'])
            if not target_channel:
                logger.error(f"Target channel {relay_config['target_channel_id']} not found")
                return
            
            # Build relay content
            content = await self.build_relay_content(message, relay_config)
            if not content:
                return
            
            # Apply stealth delay
            await self.apply_stealth_delay()
            
            # Optional typing simulation (risky!)
            if self.config['stealth_settings'].get('typing_simulation', False):
                async with target_channel.typing():
                    typing_delay = random.uniform(1, 3)
                    await asyncio.sleep(typing_delay)
            
            # Send the message
            await target_channel.send(content[:2000])  # Discord char limit
            
            # Update tracking
            now = datetime.now()
            self.message_history[now.timestamp()] = now
            self.daily_message_count[now.timestamp()] = now
            self.last_activity[relay_config['source_channel_id']] = now
            
            logger.info(f"Relayed message from {message.channel.guild.name}#{message.channel.name}")
            
        except discord.HTTPException as e:
            if "rate limited" in str(e).lower():
                logger.warning("Rate limited - pausing relay")
                await asyncio.sleep(300)  # 5 minute pause
            else:
                logger.error(f"HTTP error: {e}")
        except Exception as e:
            logger.error(f"Relay error: {e}")
    
    async def build_relay_content(self, message, config) -> Optional[str]:
        """Build the content to relay"""
        try:
            content = message.content
            if not content.strip():
                return None
            
            # Add source info if enabled
            if config.get('add_source_info', True):
                server_name = message.guild.name if message.guild else "DM"
                channel_name = message.channel.name if hasattr(message.channel, 'name') else "Unknown"
                author_name = message.author.display_name
                
                source_info = f"**[{server_name} #{channel_name}]** {author_name}:\n"
                content = source_info + content
            
            return content
            
        except Exception as e:
            logger.error(f"Error building relay content: {e}")
            return None
    
    async def apply_stealth_delay(self):
        """Apply balanced stealth delay (1-5 minutes)"""
        stealth = self.config['stealth_settings']
        
        if stealth.get('random_delays', True):
            min_delay = stealth.get('min_delay_minutes', 1) * 60
            max_delay = stealth.get('max_delay_minutes', 5) * 60
            delay = random.uniform(min_delay, max_delay)
        else:
            delay = stealth.get('min_delay_minutes', 1) * 60
        
        # Log the delay for transparency
        delay_minutes = delay / 60
        logger.info(f"Stealth delay: {delay_minutes:.1f} minutes")
        
        await asyncio.sleep(delay)
    
    def create_sample_config(self):
        """Create sample configuration file"""
        self.save_config()
        print(f"Created {self.config_file}")
        print("⚠️  IMPORTANT: Add your Discord user token to run the relay")
        print("   To get your token: https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs")
    
    async def start_relay(self):
        """Start the self-bot relay"""
        if self.config['user_token'] == "YOUR_USER_TOKEN_HERE":
            print("❌ Please set your Discord user token in selfbot_config.json")
            return
        
        await self.setup_client()
        
        try:
            await self.client.start(self.config['user_token'], bot=False)  # bot=False for user accounts
        except discord.LoginFailure:
            print("❌ Invalid user token. Check your configuration.")
        except Exception as e:
            print(f"❌ Connection error: {e}")

def create_config():
    """Create initial configuration"""
    relay = StealthDiscordRelay()
    relay.create_sample_config()

async def main():
    """Main entry point"""
    print("🕵️ Discord Self-Bot Relay (STEALTH MODE)")
    print("⚠️  WARNING: Self-bots violate Discord TOS")
    print("=" * 50)
    
    relay = StealthDiscordRelay()
    
    if not relay.config or relay.config.get('user_token') == "YOUR_USER_TOKEN_HERE":
        print("Creating configuration file...")
        create_config()
        return
    
    await relay.start_relay()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Self-bot stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")