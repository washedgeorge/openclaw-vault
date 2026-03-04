# Discord Self-Bot Relay Setup

## ⚠️ **CRITICAL WARNINGS**

### **Terms of Service Violation:**
- **Self-bots violate Discord TOS** - your account could be banned
- **Use at your own risk** - Discord actively detects self-bots
- **Consider using a burner account** instead of your main Discord account

### **Detection Risks:**
- **Rate limiting triggers** - too many messages = ban
- **Pattern recognition** - repeated behavior = ban  
- **API usage patterns** - self-bots have different signatures than normal users

---

## 🛡️ **Safety Features Built-In:**

### **Stealth Mode:**
- ✅ **Conservative rate limits** - Max 20 messages/hour  
- ✅ **Random delays** - 5-30 seconds between relays
- ✅ **Active hours only** - Only relay 8 AM - 11 PM
- ✅ **Human-like patterns** - Avoid detection signatures

### **Content Filtering:**
- ✅ **No @mentions** - Avoids triggering notifications
- ✅ **No bot commands** - Skips messages starting with !, /, etc
- ✅ **Length limits** - Only relay reasonable messages
- ✅ **Keyword filtering** - Include/exclude specific content

---

## 🔧 **Setup Process:**

### **Step 1: Get Your Discord User Token** ⚠️

**METHOD 1: Browser Developer Tools (Easier)**
1. **Open Discord in browser** (discord.com)
2. **Log in** to your account
3. **Press F12** (open developer tools)
4. **Go to Application tab** (Chrome) or Storage tab (Firefox)
5. **Find Local Storage** → discord.com
6. **Look for "token"** key
7. **Copy the value** (long string in quotes)

**METHOD 2: Network Tab (More Reliable)**
1. **Open Discord in browser**
2. **Press F12** → **Network tab**
3. **Refresh the page** or send a message
4. **Look for API requests** to discord.com/api
5. **Click on any request** → **Headers**
6. **Find Authorization header** → Copy token after "Bearer "

### **Step 2: Create Configuration**

```bash
python3 discord_selfbot_relay.py
```

This creates `selfbot_config.json` - edit it with:

```json
{
  "user_token": "YOUR_ACTUAL_USER_TOKEN_HERE",
  "relays": [
    {
      "source_channel_id": 123456789012345678,  // Channel to monitor
      "target_channel_id": 987654321098765432,  // Your channel to relay to
      "filter_keywords": [],                     // Only relay messages with these words
      "exclude_keywords": ["@everyone", "@here"], // Never relay these
      "add_source_info": true,                   // Show which server it came from
      "enabled": true
    }
  ]
}
```

### **Step 3: Get Channel IDs**

1. **Enable Developer Mode:** Discord Settings → Advanced → Developer Mode ✅
2. **Right-click channels** → "Copy ID"
3. **Source channel:** The channel you want to monitor
4. **Target channel:** Channel in your server where messages go

### **Step 4: Configure Safety Settings**

**In selfbot_config.json:**
```json
{
  "stealth_settings": {
    "messages_per_hour": 20,      // Very conservative (default)
    "min_delay_seconds": 5,       // Minimum wait between relays
    "max_delay_seconds": 30,      // Maximum wait between relays
    "active_hours_only": true,    // Only relay 8 AM - 11 PM
    "random_delays": true         // Randomize timing (more human-like)
  }
}
```

### **Step 5: Run the Self-Bot**

```bash
python3 discord_selfbot_relay.py
```

---

## 🎯 **Expected Behavior:**

### **Normal Operation:**
- **Monitors specified channels** using your Discord account
- **Relays interesting messages** to your target channels
- **Adds random delays** to appear human-like
- **Respects rate limits** to avoid detection

### **What You'll See:**
- **Source:** `[Server A #general] Username: Original message`
- **Relayed to:** Your specified target channel
- **Delays:** 5-30 seconds between each relay
- **Filtering:** Only messages that pass your filters

---

## ⚠️ **Safety Guidelines:**

### **DO:**
- ✅ **Use conservative rate limits** (20 msgs/hour max)
- ✅ **Monitor for Discord warnings** (rate limit notices)
- ✅ **Use keyword filtering** (only relay important stuff)
- ✅ **Consider using burner account** (not your main)
- ✅ **Stop immediately** if you get any warnings

### **DON'T:**
- ❌ **Relay @everyone/@here mentions** (triggers notifications)
- ❌ **Relay bot commands** (suspicious activity)
- ❌ **Run 24/7** (use active hours only)
- ❌ **Relay too frequently** (increases detection risk)
- ❌ **Share your user token** (full account access)

---

## 🚨 **Warning Signs to Stop:**

### **Discord Warnings:**
- **Rate limit messages** appearing in Discord
- **Unusual login notifications**  
- **Account verification requests**
- **Temporary restrictions** on your account

### **Technical Issues:**  
- **HTTP 429 errors** (rate limited)
- **Login failures** or token expiration
- **Messages not being sent**

**If you see ANY of these - STOP IMMEDIATELY**

---

## 🔧 **Advanced Configuration:**

### **Multiple Channel Relays:**
```json
"relays": [
  {
    "source_channel_id": 111111111111111111,
    "target_channel_id": 999999999999999999,
    "filter_keywords": ["important", "announcement"],
    "enabled": true
  },
  {
    "source_channel_id": 222222222222222222, 
    "target_channel_id": 888888888888888888,
    "exclude_keywords": ["spam", "test"],
    "enabled": true
  }
]
```

### **Keyword-Based Filtering:**
```json
{
  "filter_keywords": ["bitcoin", "crypto", "trading"],  // Only these topics
  "exclude_keywords": ["spam", "test", "bot", "@here"]  // Never these
}
```

---

## 📞 **Troubleshooting:**

### **"Invalid user token"**
- ✅ Re-copy token from browser (tokens expire)
- ✅ Make sure you copied the full token
- ✅ Remove quotes if you accidentally included them

### **"Channel not found"**  
- ✅ Verify channel IDs are 18-digit numbers
- ✅ Make sure your account has access to both channels
- ✅ Check that channels aren't deleted/private

### **"No messages being relayed"**
- ✅ Check if messages match your keyword filters
- ✅ Verify you're within active hours (8 AM - 11 PM)
- ✅ Make sure source channel has recent activity
- ✅ Check rate limits aren't blocking relays

### **"Rate limited"**
- ✅ **STOP the bot immediately**
- ✅ Wait 1+ hours before restarting
- ✅ Reduce messages_per_hour setting
- ✅ Increase min_delay_seconds

---

## 🚀 **Final Reminder:**

**This solution violates Discord TOS.** Use responsibly:

1. **Conservative settings only** (20 msgs/hour max)
2. **Monitor for warnings** and stop if issues occur
3. **Consider burner account** instead of main account
4. **Understand the risks** - account could be banned

**Alternative:** Create a second Discord account just for this purpose - if it gets banned, your main account is safe.