# ⚖️ Balanced Stealth Discord Self-Bot Configuration

## 🎯 **BALANCED APPROACH: Stealth + Usability**

This configuration balances **REASONABLE STEALTH** with **PRACTICAL USABILITY** - messages relay in 1-5 minutes instead of 15+ minutes.

---

## ⏰ **Timing Behavior:**

### **Practical Delays:**
- **1-5 minutes** between each message relay
- **15 messages per hour maximum** (reasonable rate)
- **120 messages per day maximum** (daily safety cap)

### **Simple Pattern:**
- **Active hours:** 8 AM - 11 PM (consistent)
- **No complex idle periods** or meal breaks
- **Same speed weekdays and weekends**
- **Random delays** within 1-5 minute range

---

## 🛡️ **Safety Features:**

### **Rate Limiting:**
```json
{
  "messages_per_hour": 15,        // 4x per minute average
  "messages_per_day": 120,        // Daily safety cap
  "min_delay_minutes": 1,         // Minimum 1 minute wait
  "max_delay_minutes": 5          // Maximum 5 minute wait
}
```

### **Content Filtering:**
- ✅ **No @mentions** (avoids notifications)
- ✅ **No bot commands** (!, /, $, etc.)
- ✅ **No system messages** (joins, leaves, etc.)
- ✅ **Message length limits** (10-1500 characters)
- ❌ **No engagement requirements** (relay all messages)
- ❌ **No link restrictions** (up to 3 links allowed)
- ❌ **No caps filtering** (allow ALL CAPS messages)

---

## 📊 **Performance Comparison:**

| Setting | Ultra-Stealth | **Balanced** | Fast |
|---------|---------------|-------------|------|
| **Messages/Hour** | 6 | **15** | 20+ |
| **Delay Range** | 3-15 min | **1-5 min** | 5-30 sec |
| **Daily Limit** | 50 | **120** | 200+ |
| **Detection Risk** | Very Low | **Low** | Medium |
| **Usability** | Poor | **Good** | Excellent |

### **Expected Timeline:**
```
08:00 - Bot becomes active
08:03 - First message relayed (3 min delay)
08:07 - Second message (4 min delay)  
08:11 - Third message (4 min delay)
08:13 - Fourth message (2 min delay)
08:18 - Fifth message (5 min delay)
...continues throughout day...
23:00 - Bot becomes inactive
```

**Average:** ~15 messages relayed per hour with 1-5 minute delays

---

## ⚙️ **Configuration Examples:**

### **Default Balanced (Recommended):**
```json
{
  "stealth_settings": {
    "min_delay_minutes": 1,
    "max_delay_minutes": 5,
    "messages_per_hour": 15,
    "messages_per_day": 120,
    "active_hours_only": true,
    "active_start": 8,
    "active_end": 23
  }
}
```

### **More Conservative:**
```json
{
  "stealth_settings": {
    "min_delay_minutes": 2,
    "max_delay_minutes": 8,
    "messages_per_hour": 10,
    "messages_per_day": 80
  }
}
```

### **Less Conservative (Higher Risk):**
```json
{
  "stealth_settings": {
    "min_delay_minutes": 1,
    "max_delay_minutes": 3,
    "messages_per_hour": 20,
    "messages_per_day": 150
  }
}
```

---

## 🕐 **Typical Day Timeline:**

```
08:00 - Bot starts monitoring
08:03 - Message 1 (3min delay)
08:07 - Message 2 (4min delay)  
08:11 - Message 3 (4min delay)
08:13 - Message 4 (2min delay)
09:00 - Hour 1: 4 messages relayed
10:00 - Hour 2: 4 messages relayed
11:00 - Hour 3: 3 messages relayed
12:00 - Hour 4: 4 messages relayed (no lunch break)
...continues consistently...
22:00 - Hour 14: 3 messages relayed  
23:00 - Bot stops for the night

Total: ~210 messages over 15 active hours (14/hour average)
Actual limit: 120/day, so busiest channels get priority
```

---

## 🚨 **What You'll See in Logs:**

```
[INFO] Stealth delay: 3.2 minutes
[INFO] Relayed message from Crypto Signals #alerts
[INFO] Stealth delay: 1.8 minutes  
[INFO] Relayed message from Dev Community #announcements
[INFO] Stealth delay: 4.7 minutes
[INFO] Rate limit check: 8/15 messages this hour
```

**No complex idle periods, meal breaks, or weekend slowdowns**

---

## 🎯 **Perfect For:**

### **Use Cases:**
- ✅ **Semi-active monitoring** (important messages within ~5 minutes)
- ✅ **Multiple Discord servers** (reasonable coverage)
- ✅ **Daily use** (consistent, predictable behavior)
- ✅ **Balance of speed and safety**

### **Not Ideal For:**
- ❌ **Real-time trading signals** (1-5 minute delays)
- ❌ **Ultra-high security paranoia** (use Ultra-Stealth instead)
- ❌ **Very busy servers** (15/hour limit may miss some)
- ❌ **Time-critical notifications** (use official Discord mobile)

---

## 🔬 **Why This Works:**

### **Detection Avoidance:**
1. **Random timing** prevents algorithmic detection
2. **Reasonable limits** stay well under Discord thresholds
3. **No suspicious patterns** (consistent behavior)
4. **Standard content filtering** avoids risky messages
5. **Active hours only** mimics normal user behavior

### **Usability Benefits:**
1. **Fast enough** for practical monitoring
2. **Consistent behavior** (no surprise idle periods)
3. **Good message coverage** (15/hour catches most important stuff)
4. **Simple configuration** (no complex pattern settings)

---

## 🚀 **Ready to Use:**

This is now the **default configuration** in the self-bot. 

```bash
./run_selfbot.sh
```

**Expected result:** Messages relay within 1-5 minutes with good coverage and low detection risk.

**Sweet spot:** Fast enough to be useful, slow enough to stay safe! ⚖️