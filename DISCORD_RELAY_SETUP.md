# Safe Discord Channel Relay Setup

## 🚫 **Why This Approach Won't Get You Banned:**

### **Using Proper Discord Bot (Not Self-Bot):**
- ✅ **Official Discord Bot API** - Completely allowed by TOS
- ✅ **Rate limiting built-in** - Stays under Discord limits
- ✅ **Proper permissions** - Uses bot permissions, not user account
- ❌ **NOT a self-bot** - Self-bots violate TOS and get banned

### **Key Safety Features:**
- **Rate limiting:** Max 30 messages/minute (well under limits)
- **Message filtering:** Ignore spam, system messages, bots
- **Error handling:** Won't crash or spam if something goes wrong
- **Audit logging:** Track what's being relayed

---

## 🛠️ **Setup Process:**

### **Step 1: Create Discord Bot Application**

1. **Go to:** https://discord.com/developers/applications
2. **Click:** "New Application" 
3. **Name it:** "Channel Relay Bot" (or whatever you want)
4. **Go to:** "Bot" section in left sidebar
5. **Click:** "Add Bot"
6. **Copy the bot token** (keep this secret!)

### **Step 2: Bot Permissions**

**In the Bot section, enable these intents:**
- ✅ Message Content Intent
- ✅ Server Members Intent (optional)

**In OAuth2 → URL Generator:**
- **Scopes:** `bot`
- **Bot Permissions:** 
  - Read Messages
  - Send Messages  
  - Read Message History
  - Embed Links
  - Attach Files

**Copy the generated URL** - you'll use this to add the bot to servers.

### **Step 3: Add Bot to Servers**

**For each server you want to relay FROM/TO:**
1. **Use the OAuth URL** from Step 2
2. **Select the server** from dropdown
3. **Authorize** with required permissions

**Important:** You need admin permissions in both source and target servers, OR the server admins need to add your bot.

### **Step 4: Configure the Bot**

1. **Run the Python script** to create config file:
```bash
python3 discord_relay_bot.py
```

2. **Edit `relay_config.json`** with your settings:
```json
{
  "bot_token": "YOUR_BOT_TOKEN_FROM_STEP_1",
  "relays": [
    {
      "source_channel_id": 123456789012345678,
      "target_channel_id": 987654321098765432,
      "filter_keywords": [],
      "exclude_keywords": ["spam", "test"],
      "relay_embeds": true,
      "relay_attachments": true,
      "add_source_info": true
    }
  ]
}
```

3. **Get Channel IDs:**
   - Enable Developer Mode in Discord (User Settings → Advanced)
   - Right-click any channel → "Copy ID"

### **Step 5: Run the Bot**

```bash
pip install discord.py
python3 discord_relay_bot.py
```

---

## 🎯 **Your Specific Use Case:**

### **Problem:** Can't access certain servers on mobile
### **Solution:** 
1. **Add the bot** to both your main server and the servers you can't access on mobile
2. **Configure relays** from interesting channels → your main server
3. **Monitor everything** from your main server

### **Example Configuration:**
```json
{
  "relays": [
    {
      "source_channel_id": 123456789012345678,  // #general from server you can't access
      "target_channel_id": 987654321098765432,  // #relayed-general in your main server
      "filter_keywords": [],                     // Relay everything
      "add_source_info": true                   // Shows which server it came from
    },
    {
      "source_channel_id": 111222333444555666,  // #announcements from another server  
      "target_channel_id": 777888999000111222,  // #relayed-announcements in your server
      "filter_keywords": ["important", "update"], // Only relay important messages
      "add_source_info": true
    }
  ]
}
```

---

## ⚠️ **Important Notes:**

### **Permissions Required:**
- **Source servers:** Bot needs "Read Messages" and "Read Message History"
- **Target server:** Bot needs "Send Messages" and "Embed Links"
- **You need admin** in your main server to add the bot
- **Source servers need to allow** the bot (admin approval required)

### **Rate Limits:**
- **Built-in protection** against Discord rate limits
- **Max 30 messages/minute** per relay
- **Automatic backoff** if limits are hit

### **Privacy Considerations:**
- **Bot can see all messages** in channels it has access to
- **Only relays what you configure** - doesn't store or log everything
- **Respects channel permissions** - won't relay from private channels unless explicitly configured

---

## 🔧 **Advanced Features:**

### **Keyword Filtering:**
```json
"filter_keywords": ["bitcoin", "crypto", "trading"]  // Only relay messages containing these words
"exclude_keywords": ["spam", "test", "bot"]         // Don't relay messages with these words
```

### **Multiple Relays:**
```json
"relays": [
  {
    "source_channel_id": 123,
    "target_channel_id": 456,
    "filter_keywords": ["important"]
  },
  {
    "source_channel_id": 789,  
    "target_channel_id": 456,  // Same target, different source
    "exclude_keywords": ["noise"]
  }
]
```

### **Bot Commands** (in your server):
- `!relay_add_relay [source_id] [target_id]` - Add new relay
- `!relay_list_relays` - Show all active relays

---

## 🚀 **Next Steps:**

1. **Create the bot application** (5 minutes)
2. **Add bot to your servers** (ask admins if needed)
3. **Configure the relay channels** 
4. **Test with a few messages**
5. **Scale up** once it's working

This approach is **100% TOS compliant** and much more reliable than trying to use self-bots or other risky methods!