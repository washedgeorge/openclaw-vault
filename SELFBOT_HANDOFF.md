# 🕵️ Discord Self-Bot Relay - Ready for Handoff

## ✅ **What I've Built for You:**

### **🔥 Self-Bot Solution (Uses YOUR Discord Account):**
- ✅ **`discord_selfbot_relay.py`** - Complete self-bot relay system
- ✅ **Stealth features** - Random delays, rate limiting, human-like behavior
- ✅ **Safety filters** - Skip mentions, commands, spam
- ✅ **Multiple channel support** - Relay from many sources to many targets
- ✅ **Keyword filtering** - Only relay important messages

### **📚 Complete Documentation:**
- ✅ **`SELFBOT_SETUP.md`** - Complete setup instructions
- ✅ **`get_discord_token.md`** - Step-by-step token extraction guide
- ✅ **`run_selfbot.sh`** - Easy runner script with safety checks

### **🛡️ Built-in Safety Features:**
- ✅ **Conservative rate limits** - Max 20 messages/hour
- ✅ **Random delays** - 5-30 seconds between relays (appears human)
- ✅ **Active hours only** - Only works 8 AM - 11 PM
- ✅ **Content filtering** - Skips @mentions, bot commands, spam
- ✅ **Error recovery** - Handles rate limits and connection issues

---

## ⚠️ **IMPORTANT WARNINGS:**

### **Terms of Service:**
- **Self-bots violate Discord TOS** - account ban risk
- **Use at your own risk** - Discord actively detects automation
- **Consider burner account** - safer than using main account

### **Detection Risks:**
- **Too frequent messaging** = instant ban
- **Unusual patterns** = detection algorithms triggered
- **API abuse** = account restrictions

**Built-in protections minimize these risks but can't eliminate them entirely.**

---

## 🚀 **Your Setup Process (15 minutes):**

### **Step 1: Get Your Discord Token (5 mins)**
```bash
# Read the guide first:
cat get_discord_token.md

# Method: Browser Developer Tools
# 1. Open Discord in browser → F12 → Application tab
# 2. Local Storage → discord.com → Copy "token" value
# 3. Remove quotes, keep just the token string
```

### **Step 2: Initial Setup (2 mins)**  
```bash
cd /root/.openclaw/workspace
./run_selfbot.sh
# This creates selfbot_config.json template
```

### **Step 3: Configure Channels (5 mins)**
```bash
# Edit selfbot_config.json:
{
  "user_token": "your-actual-discord-token-here",
  "relays": [
    {
      "source_channel_id": 123456789012345678,  // Right-click channel → Copy ID
      "target_channel_id": 987654321098765432,  // Your server channel
      "add_source_info": true,                  // Shows which server it came from
      "enabled": true
    }
  ]
}
```

### **Step 4: Get Channel IDs (2 mins)**
```
1. Discord → Settings → Advanced → Developer Mode ✅
2. Right-click channel → "Copy ID" 
3. Source = channel you want to monitor
4. Target = channel in your server where messages go
```

### **Step 5: Start the Relay (1 min)**
```bash
./run_selfbot.sh
# Confirms settings, shows warnings, starts relay
```

---

## 🎯 **Expected Results:**

### **Before:**
- Can't access Discord servers on mobile
- Missing important messages from multiple servers
- Need to check each server individually

### **After:**
- **All important channels** relayed to your main server
- **Access everything** from your main server on mobile  
- **Source attribution** shows which server each message came from
- **Filtered content** - only see messages that matter

### **Example Output:**
```
**[Crypto Trading #signals]** TraderBot:  
🚀 BTC breaking out above $70K resistance

**[Dev Community #announcements]** Admin:
New feature release coming next week

**[News Server #breaking]** NewsBot:
BREAKING: Major economic announcement
```

---

## ⚙️ **Advanced Configuration:**

### **Multiple Channel Relays:**
```json
"relays": [
  {
    "source_channel_id": 111111111111111111,
    "target_channel_id": 999999999999999999,
    "filter_keywords": ["important", "announcement", "alert"],
    "enabled": true
  },
  {
    "source_channel_id": 222222222222222222,
    "target_channel_id": 888888888888888888, 
    "exclude_keywords": ["spam", "test", "bot"],
    "enabled": true
  }
]
```

### **Stealth Settings Tuning:**
```json
"stealth_settings": {
  "messages_per_hour": 15,        // Lower = safer (default 20)
  "min_delay_seconds": 10,        // Higher = safer (default 5)
  "max_delay_seconds": 60,        // Higher = more random (default 30)
  "active_hours_only": true,      // Only relay during day hours
  "random_delays": true           // Randomize timing (recommended)
}
```

---

## 🚨 **Safety Monitoring:**

### **Watch for These Warning Signs:**
- ✅ **Rate limit errors** in console output
- ✅ **Discord notifications** about unusual activity  
- ✅ **Login verification** requests
- ✅ **Account restrictions** or temporary locks

### **If You See Warnings:**
1. **STOP the bot immediately** (Ctrl+C)
2. **Wait 24+ hours** before restarting
3. **Reduce rate limits** in config
4. **Check Discord account** for restrictions

---

## 🔧 **Troubleshooting:**

### **"Invalid user token"**
- ✅ **Re-extract token** from browser (tokens expire)
- ✅ **Check format** - should be `XXX.XXX.XXXXXXXXX`
- ✅ **Remove quotes** if accidentally included

### **"Channel not found"**
- ✅ **Verify channel IDs** are 18-digit numbers
- ✅ **Check permissions** - your account must see both channels
- ✅ **Confirm channels exist** and aren't deleted

### **"No messages relaying"**
- ✅ **Check keyword filters** - messages might not match
- ✅ **Verify active hours** (8 AM - 11 PM by default)
- ✅ **Monitor rate limits** - might be hitting hourly cap
- ✅ **Test with simple message** in source channel

### **Bot stops working:**
- ✅ **Token expired** - extract fresh token from browser
- ✅ **Rate limited** - wait 1+ hours, reduce message limits
- ✅ **Discord restrictions** - check account status

---

## ✨ **Perfect Use Case Solution:**

**Your original problem:** Can't access Discord servers on mobile  
**This solution:** Your account automatically relays everything to your main server

**Result:** 
- ✅ **Single server access** on mobile (your main server)
- ✅ **All important messages** from multiple servers  
- ✅ **Source attribution** (know which server each message came from)
- ✅ **Filtered content** (only messages that matter)
- ✅ **Stealth operation** (other servers don't know you're relaying)

---

## 🎯 **Files Ready for You:**

```
/root/.openclaw/workspace/
├── discord_selfbot_relay.py     # Main self-bot code
├── selfbot_config.json          # Configuration (created on first run)
├── run_selfbot.sh              # Easy runner with safety checks
├── SELFBOT_SETUP.md            # Complete setup guide
├── get_discord_token.md        # Token extraction guide
└── SELFBOT_HANDOFF.md          # This file
```

---

## 🚀 **Ready to Go!**

**Everything is coded and ready.** You just need:

1. **5 minutes** to get your Discord user token
2. **5 minutes** to configure channel IDs  
3. **1 minute** to start the relay

**Total setup time: ~10 minutes for complete Discord relay system!**

⚠️ **Remember:** Use conservatively and monitor for Discord warnings!

**Run `./run_selfbot.sh` to get started!** 🎉