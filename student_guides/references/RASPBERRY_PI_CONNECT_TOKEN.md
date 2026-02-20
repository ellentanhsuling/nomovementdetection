# Finding Your Raspberry Pi Connect Token

## Quick Answer

The token is found in your **Raspberry Pi Connect account** on the website.

---

## Where to Find the Token

### Step 1: Go to Raspberry Pi Connect Website

1. Open web browser
2. Go to: **https://connect.raspberrypi.com**
3. Sign in with your Raspberry Pi account

### Step 2: Find Token in Account Settings

**Location options (may vary by interface):**

**Option A: Account Settings**
1. Click on your profile/account icon (top right)
2. Go to **"Account Settings"** or **"Settings"**
3. Look for **"Connect Token"** or **"Device Token"**
4. Copy the token

**Option B: Devices/My Devices**
1. Look for **"My Devices"** or **"Devices"** section
2. Click on it
3. Token may be shown there or in device details

**Option C: Security/Credentials**
1. Go to **"Security"** or **"Credentials"** section
2. Look for **"API Token"** or **"Connect Token"**
3. Copy the token

### Step 3: Copy Token to Imager

1. Copy the token (it's usually a long string of letters/numbers)
2. Paste it into Raspberry Pi Imager where it asks for token
3. Continue with setup

---

## What the Token Looks Like

**Format:**
- Usually a long string (20-40+ characters)
- Mix of letters and numbers
- May have dashes or be all one string
- Example format: `abc123def456ghi789` or `abc-123-def-456`

---

## If You Can't Find the Token

### Try These:

1. **Check if you need to generate one:**
   - Some accounts require generating a token first
   - Look for "Generate Token" or "Create Token" button
   - Click it, then copy the generated token

2. **Check email:**
   - Raspberry Pi may have sent token in welcome email
   - Search your email for "Raspberry Pi Connect"

3. **Check Imager help:**
   - In Imager, look for "Help" or "?" icon
   - May have link to get token

4. **Official documentation:**
   - Visit: https://www.raspberrypi.com/documentation/
   - Search for "Raspberry Pi Connect token"

---

## Alternative: Skip Connect for Now

**If you can't find the token:**
- **Skip Raspberry Pi Connect** (uncheck it)
- **Enable SSH instead** (check "Enable SSH")
- You can set up Connect later after Pi boots
- Or use SSH for remote access

**SSH works fine** - Connect is just more convenient!

---

## After You Get the Token

1. **Paste token into Imager**
2. **Continue with setup**
3. **Pi will connect to Connect service on first boot**
4. **Access via connect.raspberrypi.com**

---

## Troubleshooting

**Token not working?**
- Make sure you copied entire token (no spaces)
- Check if token expired (may need to generate new one)
- Verify you're signed into correct account

**Can't find account settings?**
- Try different browser
- Check if you're on correct website (connect.raspberrypi.com)
- Look for menu icon (three lines) or profile icon

---

## Quick Steps Summary

1. ✅ Sign in to connect.raspberrypi.com
2. ✅ Go to Account Settings / My Devices / Security
3. ✅ Find "Connect Token" or "Device Token"
4. ✅ Copy the token
5. ✅ Paste into Imager

---

*If you're stuck, you can always skip Connect and use SSH instead - both work!*
