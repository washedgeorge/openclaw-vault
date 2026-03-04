# 🥷 Ultra-Stealth Discord Self-Bot Configuration

## 🎯 **MAXIMUM STEALTH MODE**

This configuration prioritizes **UNDETECTED OPERATION** over speed. Your messages will be relayed slowly but with minimal risk of detection.

---

## ⏰ **Timing Behavior:**

### **Ultra-Conservative Delays:**
- **3-15 minutes** between each message relay
- **6 messages per hour maximum** (vs 20 in normal mode)
- **50 messages per day maximum** (daily safety cap)

### **Human-Like Patterns:**
- **Work hours (9 AM - 5 PM):** Longer delays (people less active on Discord)
- **Evening (6-10 PM):** Shorter delays (peak Discord usage)
- **Weekends:** 30-50% slower than weekdays
- **Meal times:** 70% chance to skip relaying during lunch/dinner hours

### **Random Idle Periods:**
- **30 minute - 2 hour** random breaks with zero activity
- **30% chance** every hour to enter idle period
- **Mimics human behavior** (bathroom breaks, meetings, meals)

---

## 🛡️ **Enhanced Safety Filters:**

### **Message Quality Requirements:**
```json
{
  "min_message_length": 20,        // Only longer, more valuable messages
  "max_message_length": 800,       // Avoid very long messages
  "max_links_per_message": 1,      // Maximum 1 link per message
  "caps_threshold": 0.5            // Reject if >50% CAPS (spam-like)
}
```

### **Content Filtering:**
- ✅ **No @mentions** (avoids notifications)
- ✅ **No bot commands** (!, /, $, etc.)
- ✅ **No ALL CAPS messages** (spam detection)
- ✅ **No link-heavy messages** (suspicious activity)
- ✅ **Engagement filter** (only relay messages with reactions)

### **Behavioral Mimicking:**
- ✅ **Meal time breaks** (12-1 PM, 6-7 PM less active)
- ✅ **Weekend slowdown** (more casual usage pattern)
- ✅ **Work hour reduction** (business hours = less Discord usage)
- ✅ **Random idle periods** (human-like breaks)

---

## 📊 **Expected Performance:**

### **Speed vs Stealth Trade-off:**
| Setting | Normal Mode | Ultra-Stealth Mode |
|---------|-------------|-------------------|
| **Messages/Hour** | 20 | 6 |
| **Delay Range** | 5-30 seconds | 3-15 minutes |
| **Daily Limit** | 200+ | 50 |
| **Detection Risk** | Medium | Very Low |
| **Response Time** | Fast | Slow |

### **Real-World Usage:**
- **Important message posted:** 3-15 minute delay before relay
- **Busy Discord server:** Only 6 best messages per hour relayed
- **Weekend activity:** 30-50% slower than weekdays
- **Meal times:** Often skipped entirely

---

## ⚙️ **Configuration Examples:**

### **Ultra-Conservative (Safest):**
```json
{
  "stealth_settings": {
    "min_delay_minutes": 5,
    "max_delay_minutes": 20,
    "messages_per_hour": 4,
    "messages_per_day": 30,
    "active_start": 10,
    "active_end": 21,
    "weekend_slower": true,
    "human_pattern": true
  }
}
```

### **Moderate Stealth (Balanced):**
```json
{
  "stealth_settings": {
    "min_delay_minutes": 3,
    "max_delay_minutes": 15,
    "messages_per_hour": 6,
    "messages_per_day": 50,
    "active_start": 9,
    "active_end": 22,
    "weekend_slower": true,
    "human_pattern": true
  }
}
```

### **Keyword-Focused (Quality over Quantity):**
```json
{
  "relays": [
    {
      "filter_keywords": ["important", "urgent", "announcement", "alert"],
      "exclude_keywords": ["test", "spam", "bot", "meme"],
      "require_engagement": true  // Only relay messages with reactions
    }
  ]
}
```

---

## 🕐 **Typical Day Timeline:**

```
09:00 - Bot becomes active
09:15 - First message relayed (if any)
09:30 - Random 45-minute idle period begins
10:15 - Idle period ends, resume monitoring
10:28 - Second message relayed
11:45 - Third message (work hours = slower)
12:00 - Lunch break behavior (70% chance to skip)
14:30 - Fourth message
15:45 - Random 1-hour idle period
18:00 - Dinner time (likely skipped)
19:15 - Fifth message (evening activity pickup)
20:45 - Sixth message
22:00 - Bot becomes inactive for the night
```

**Total:** 6 messages relayed over 13 active hours

---

## 🚨 **Monitoring & Logs:**

### **What You'll See:**
```
[INFO] Stealth delay: 8.3 minutes
[INFO] Entering idle period for 47.2 minutes  
[INFO] Meal time skip (70% chance triggered)
[INFO] Weekend slowdown active (1.4x delay multiplier)
[INFO] Work hours pattern (2.1x delay multiplier)
```

### **Success Indicators:**
- ✅ **No rate limit warnings**
- ✅ **No Discord account notifications**
- ✅ **Consistent relay activity** (not getting blocked)
- ✅ **Random timing patterns** (not predictable)

---

## 🎯 **Perfect For:**

### **Use Cases:**
- ✅ **High-value Discord servers** (you can't afford to lose access)
- ✅ **Long-term monitoring** (running for weeks/months)
- ✅ **Important-only filtering** (news, announcements, alerts)
- ✅ **Main Discord account** (too valuable to risk)

### **Not Ideal For:**
- ❌ **Real-time notifications** (3-15 minute delays)
- ❌ **High-volume servers** (only top 6 messages/hour)
- ❌ **Chat participation** (purely monitoring)
- ❌ **Time-sensitive content** (trading signals, etc.)

---

## 🔬 **Detection Avoidance Science:**

### **Why This Works:**
1. **Mimics human discord usage patterns**
2. **Random timing prevents algorithmic detection**
3. **Conservative limits stay well under Discord thresholds**
4. **Quality filtering avoids suspicious content**
5. **Idle periods simulate real human behavior**

### **Discord Detection Vectors:**
- ❌ **Predictable timing** → We use random delays
- ❌ **High message frequency** → We limit to 6/hour max
- ❌ **24/7 activity** → We have active hours + idle periods
- ❌ **Bot-like content** → We filter mentions, commands, spam
- ❌ **API usage patterns** → We simulate human reading patterns

---

## 🚀 **Ready to Deploy:**

The self-bot is pre-configured with these ultra-stealth settings. Just run:

```bash
./run_selfbot.sh
```

**Expected result:** Slow but steady, undetected message relaying that mimics natural human Discord usage patterns.

**Trade-off accepted:** Slower notifications in exchange for minimal detection risk and long-term reliability.