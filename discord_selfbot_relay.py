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
                    "min_delay_minutes": 3,      # Minimum 3 minutes between relays
                    "max_delay_minutes": 15,     # Maximum 15 minutes between relays  
                    "messages_per_hour": 6,      # Ultra-conservative: 6 messages/hour max
                    "messages_per_day": 50,      # Daily cap to avoid patterns
                    "random_delays": True,       # Add random delays
                    "typing_simulation": False,  # Never simulate typing
                    "active_hours_only": True,   # Only relay during active hours
                    "active_start": 9,           # 9 AM (avoid early morning)
                    "active_end": 22,            # 10 PM (avoid late night)
                    "idle_periods": True,        # Random periods of no activity
                    "idle_min_minutes": 30,      # Minimum idle period
                    "idle_max_minutes": 120,     # Maximum idle period (2 hours)
                    "weekend_slower": True,      # Even slower on weekends
                    "human_pattern": True        # Mimic human online patterns
                },
                "safety_filters": {
                    "min_message_length": 20,        # Longer messages only (more valuable)
                    "max_message_length": 800,       # Avoid very long messages
                    "ignore_bots": True,
                    "ignore_system": True,
                    "ignore_mentions": True,         # Don't relay @mentions (risky)
                    "ignore_commands": True,         # Don't relay bot commands
                    "ignore_links": True,            # Don't relay messages with lots of links
                    "ignore_caps": True,             # Don't relay ALL CAPS messages (spam-like)
                    "ignore_repeats": True,          # Don't relay if very similar to recent message
                    "require_engagement": True,      # Only relay messages with reactions/replies
                    "max_links_per_message": 1,      # Maximum links allowed
                    "caps_threshold": 0.5            # Max ratio of caps to total chars
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
        
        # Link filtering
        if safety.get('ignore_links', True):
            import re
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
            max_links = safety.get('max_links_per_message', 1)
            if len(links) > max_links:
                return False
        
        # Caps filter (avoid spam-like messages)
        if safety.get('ignore_caps', True):
            caps_count = sum(1 for c in message.content if c.isupper())
            total_alpha = sum(1 for c in message.content if c.isalpha())
            if total_alpha > 0:
                caps_ratio = caps_count / total_alpha
                if caps_ratio > safety.get('caps_threshold', 0.5):
                    return False
        
        # Engagement filter (only relay messages that got reactions/replies)
        if safety.get('require_engagement', False):
            if len(message.reactions) == 0:
                # Give new messages a few minutes to get reactions
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
        """Ultra-stealth rate limiting"""
        now = datetime.now()
        stealth = self.config['stealth_settings']
        
        # Check if we're in an idle period
        if self.idle_until and now < self.idle_until:
            return False
        
        # Randomly enter idle periods (human-like breaks)
        if stealth.get('idle_periods', True):
            time_since_idle_check = (now - self.last_idle_check).total_seconds()
            if time_since_idle_check > 3600:  # Check every hour
                if random.random() < 0.3:  # 30% chance of idle period
                    idle_min = stealth.get('idle_min_minutes', 30) * 60
                    idle_max = stealth.get('idle_max_minutes', 120) * 60
                    idle_duration = random.uniform(idle_min, idle_max)
                    self.idle_until = now + timedelta(seconds=idle_duration)
                    logger.info(f"Entering idle period for {idle_duration/60:.1f} minutes")
                    return False
                self.last_idle_check = now
        
        # Clean old entries (hourly and daily)
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        self.message_history = {k: v for k, v in self.message_history.items() if v > hour_ago}
        self.daily_message_count = {k: v for k, v in self.daily_message_count.items() if v > day_ago}
        
        # Check daily limit first (most restrictive)
        daily_limit = stealth.get('messages_per_day', 50)
        if len(self.daily_message_count) >= daily_limit:
            return False
        
        # Check hourly limit
        hourly_limit = stealth.get('messages_per_hour', 6)
        if len(self.message_history) >= hourly_limit:
            return False
        
        # Check minimum delay (in minutes now)
        channel_key = relay_config['source_channel_id']
        if channel_key in self.last_activity:
            time_diff = (now - self.last_activity[channel_key]).total_seconds()
            min_delay = stealth.get('min_delay_minutes', 3) * 60
            if time_diff < min_delay:
                return False
        
        # Weekend slowdown
        if stealth.get('weekend_slower', True):
            if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
                # Halve the rate limits on weekends
                if len(self.message_history) >= max(1, hourly_limit // 2):
                    return False
        
        return True
    
    def is_active_hours(self) -> bool:
        """Check if current time is within active hours"""
        stealth = self.config['stealth_settings']
        if not stealth.get('active_hours_only', True):
            return True
        
        now = datetime.now()
        current_hour = now.hour
        start_hour = stealth.get('active_start', 9)
        end_hour = stealth.get('active_end', 22)
        
        # Basic hour check
        if not (start_hour <= current_hour <= end_hour):
            return False
        
        # Human pattern: less active during lunch (12-13) and dinner (18-19)
        if stealth.get('human_pattern', True):
            if current_hour == 12 or current_hour == 18:
                # 70% chance of being inactive during meal times
                return random.random() > 0.7
        
        return True
    
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
        """Apply ultra-stealth delay (minutes, not seconds)"""
        stealth = self.config['stealth_settings']
        now = datetime.now()
        
        if stealth.get('random_delays', True):
            min_delay = stealth.get('min_delay_minutes', 3) * 60
            max_delay = stealth.get('max_delay_minutes', 15) * 60
            
            # Human pattern: longer delays during work hours, shorter during evening
            if stealth.get('human_pattern', True):
                hour = now.hour
                if 9 <= hour <= 17:  # Work hours - people check Discord less
                    delay_multiplier = random.uniform(1.5, 2.5)
                elif 18 <= hour <= 22:  # Evening - more active
                    delay_multiplier = random.uniform(0.8, 1.2)
                else:  # Late night/early morning - very slow
                    delay_multiplier = random.uniform(2.0, 3.0)
                
                min_delay *= delay_multiplier
                max_delay *= delay_multiplier
            
            # Weekend pattern - generally slower
            if stealth.get('weekend_slower', True) and now.weekday() >= 5:
                min_delay *= random.uniform(1.3, 1.8)
                max_delay *= random.uniform(1.5, 2.2)
            
            delay = random.uniform(min_delay, max_delay)
        else:
            delay = stealth.get('min_delay_minutes', 3) * 60
        
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