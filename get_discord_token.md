# How to Get Your Discord User Token

## ⚠️ **SECURITY WARNING:**
- **Never share your token** - it gives full access to your Discord account
- **Use at your own risk** - Self-bots violate Discord TOS
- **Consider using a burner account** instead of your main account

---

## 📱 **Method 1: Browser Developer Tools (Easiest)**

### **Chrome/Edge:**
1. **Open Discord** in your browser: https://discord.com/app
2. **Log in** to your account
3. **Press F12** (opens Developer Tools)
4. **Click "Application" tab** at the top
5. **In left sidebar:** Storage → Local Storage → https://discord.com
6. **Find the "token" key** in the list
7. **Copy the value** (long string in quotes - remove the quotes)

### **Firefox:**
1. **Open Discord** in browser and log in
2. **Press F12** (Developer Tools)  
3. **Click "Storage" tab**
4. **Local Storage** → discord.com
5. **Find "token"** → copy the value (remove quotes)

### **Safari:**
1. **Enable Developer menu:** Safari → Preferences → Advanced → "Show Develop menu"
2. **Open Discord** and log in
3. **Develop → Show Web Inspector** 
4. **Storage tab** → Local Storage → discord.com
5. **Copy token value**

---

## 🌐 **Method 2: Network Tab (More Reliable)**

1. **Open Discord in browser** and log in
2. **Press F12** → **Network tab**
3. **Send a message** in any channel (this creates network requests)
4. **Look for requests** to discord.com/api
5. **Click on any API request**
6. **Headers section** → find "Authorization: Bearer [your-token]"
7. **Copy everything after "Bearer "**

---

## 📱 **Method 3: Mobile App (Advanced)**

**Android (Requires Root):**
1. **Root your device** (voids warranty, advanced users only)
2. **Install file manager** with root access
3. **Navigate to:** `/data/data/com.discord/shared_prefs/`
4. **Open:** `com.discord_preferences.xml`
5. **Find:** `STORE_TOKEN` key

**iOS (Requires Jailbreak):**  
1. **Jailbreak your device** (voids warranty, advanced users only)
2. **SSH into device** or use file manager
3. **Navigate to Discord app data**
4. **Extract token from app preferences**

**Note:** Mobile methods are complex and not recommended.

---

## 🔍 **What Your Token Looks Like:**

### **Valid Token Format:**
```
MzYyMTI3NDQ5MTc5MjgzNDU3.YcKd1Q.example-rest-of-token-here
```

### **Token Structure:**
- **First part:** Base64 encoded user ID
- **Second part:** Timestamp  
- **Third part:** HMAC signature
- **Length:** Usually 59+ characters
- **Format:** `XXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXX`

### **Invalid Examples:**
```
❌ "token"                    (placeholder text)
❌ YOUR_TOKEN_HERE            (placeholder text)  
❌ 123456789                  (too short)
❌ password123                (not a token)
```

---

## 🛡️ **Security Best Practices:**

### **Token Safety:**
- ✅ **Never share your token** with anyone
- ✅ **Don't paste it in Discord** (will be auto-deleted)
- ✅ **Store it securely** in your config file only
- ✅ **Use a burner account** if possible

### **If Your Token is Compromised:**
1. **Change your Discord password immediately**
2. **Enable 2FA** if not already enabled
3. **Check for unauthorized activity** in your account
4. **Revoke all sessions** in Discord settings

---

## 🔧 **Adding Token to Config:**

### **Edit selfbot_config.json:**
```json
{
  "user_token": "MzYyMTI3NDQ5MTc5MjgzNDU3.YcKd1Q.your-actual-token-here",
  "relays": [
    ...
  ]
}
```

### **Common Mistakes:**
- ❌ **Leaving quotes:** `"token"` → `token`
- ❌ **Adding Bearer:** Don't include "Bearer " prefix  
- ❌ **Spaces:** Remove any extra spaces
- ❌ **Incomplete:** Make sure you copied the full token

---

## 🚨 **Troubleshooting:**

### **"Invalid user token" Error:**
- ✅ **Re-extract token** (they expire periodically)
- ✅ **Check format** (should be 3 parts separated by dots)
- ✅ **Remove quotes** if you accidentally included them
- ✅ **Try different browser** (sometimes caching issues)

### **"Login failure" Error:**
- ✅ **Token expired** - get a fresh one
- ✅ **Account locked/restricted** - check Discord for notifications
- ✅ **Rate limited** - wait an hour and try again

### **Token Changes Frequently:**
- **Normal behavior** - Discord rotates tokens for security
- **Solution:** Re-extract token when it stops working
- **Automation:** Some tools can auto-refresh (advanced)

---

## ⚡ **Quick Test:**

### **Verify Your Token Works:**
1. **Open browser console** (F12 → Console)
2. **Paste this code:**
```javascript
fetch('https://discord.com/api/v9/users/@me', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN_HERE'
  }
})
.then(response => response.json())
.then(data => console.log(data.username));
```
3. **Replace YOUR_TOKEN_HERE** with your actual token
4. **Press Enter** - should show your username

If it shows your username, the token works! ✅  
If it shows an error, the token is invalid ❌

---

## 📞 **Still Having Issues?**

### **Common Problems:**
1. **Token format wrong** - should be `XXX.XXX.XXX` format
2. **Copied incomplete token** - make sure you got all parts
3. **Browser cache issues** - try private/incognito mode
4. **Account restrictions** - Discord may have limited your account

### **Alternative Approach:**
**Create a new Discord account** just for this purpose:
1. **Less risk** to your main account
2. **Easier to replace** if banned
3. **Can join same servers** with invite links