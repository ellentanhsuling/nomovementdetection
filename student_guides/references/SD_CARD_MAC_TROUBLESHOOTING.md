# SD Card Detection on Mac - Troubleshooting Guide

## Quick Steps to Detect SD Card on Mac

### Step 1: Check Physical Connection

1. **Unplug and replug the card reader**
   - Remove USB cable from Mac
   - Wait 5 seconds
   - Plug back in

2. **Try different USB port**
   - Mac has multiple USB ports
   - Try a different one
   - Some ports may be faulty

3. **Check card reader**
   - Is it properly connected?
   - Try wiggling the connection
   - Check if reader has power light (if applicable)

**✅ Verification:** Card reader is properly connected

---

### Step 2: Check if Mac Sees the Card

**Method 1: Finder**
1. Open **Finder**
2. Look in **sidebar** under "Devices"
3. SD card should appear there
4. Click on it to see contents

**Method 2: Disk Utility**
1. Open **Disk Utility**:
   - Press `Cmd + Space` (Spotlight)
   - Type "Disk Utility"
   - Press Enter
2. Look in **left sidebar**
3. SD card should appear (may show as "NO NAME" or have a name)
4. If you see it but it's grayed out, it may need mounting

**Method 3: Terminal**
```bash
diskutil list
```
- Shows all connected disks
- Look for your SD card in the list
- Note the disk identifier (like `/dev/disk2`)

**✅ Verification:** SD card appears in one of these places

---

### Step 3: If Card Doesn't Appear

**Try these solutions:**

#### Solution 1: Eject and Re-insert Card
1. If card appears in Finder, **eject it** (drag to trash or right-click → Eject)
2. **Remove card from reader**
3. **Wait 10 seconds**
4. **Re-insert card** into reader
5. Wait for Mac to recognize it

#### Solution 2: Check Card Lock Switch
1. **Look at SD card**
2. **Find small switch on side** (write-protect switch)
3. **Make sure switch is UP** (unlocked position)
4. If it's down, slide it up
5. Re-insert card

#### Solution 3: Try Different Card Reader
- If you have another card reader, try it
- Some readers are faulty
- USB-C vs USB-A readers work differently

#### Solution 4: Check System Information
1. Click **Apple menu** → **About This Mac**
2. Click **System Report**
3. Go to **USB** section
4. Look for your card reader
5. If reader doesn't appear, it's a hardware issue

---

### Step 4: If Card Appears But Can't Read

**Card might be corrupted or need formatting:**

#### Check in Disk Utility:
1. Open **Disk Utility**
2. Select SD card in sidebar
3. Click **"First Aid"** button
4. Click **"Run"**
5. Let it check and repair

**⚠️ Warning:** If you run First Aid, it may ask to repair - this is OK if card is just for Pi setup (will be erased anyway)

#### If Card is Unreadable:
- **This is OK for your use case!**
- Raspberry Pi Imager will format it anyway
- Just proceed with Imager - it will handle it

---

### Step 5: Force Mount (If Card Appears But Not Mounted)

**In Terminal:**
```bash
# List all disks
diskutil list

# Find your SD card (look for size matching your card)
# Note the disk identifier (e.g., /dev/disk2)

# Mount it (replace disk2 with your disk)
diskutil mountDisk /dev/disk2
```

**Or in Disk Utility:**
1. Select unmounted card
2. Click **"Mount"** button

---

### Step 6: Check Card Health

**If card keeps failing:**

1. **Card might be damaged:**
   - Old cards fail over time
   - Physical damage
   - Too many write cycles

2. **Test with another card** (if available):
   - See if problem is card or reader
   - If another card works, original card is bad

3. **Check card capacity:**
   - Very old/small cards may have issues
   - 32GB+ recommended for Pi 5

---

## Common Issues and Solutions

### Issue: "Card not recognized"
**Solutions:**
- Try different USB port
- Try different card reader
- Check card lock switch
- Restart Mac (sometimes helps)

### Issue: "Card appears then disappears"
**Solutions:**
- Card reader connection loose
- USB port issue
- Card reader faulty
- Try different port/reader

### Issue: "Card shows but can't access"
**Solutions:**
- Run First Aid in Disk Utility
- Or just use Imager (will format anyway)
- Card might be corrupted (OK, will be erased)

### Issue: "Card locked"
**Solutions:**
- Check physical lock switch on card
- Slide switch to unlock position
- Re-insert card

---

## For Your Specific Situation

**Since you're preparing card for Raspberry Pi:**

**Option 1: Card appears in Imager**
- ✅ Just use Imager
- Imager will format it anyway
- Don't worry about reading contents

**Option 2: Card doesn't appear anywhere**
- Check physical connections
- Try different reader/port
- Check if card is damaged
- May need new SD card

**Option 3: Card appears but can't read**
- This is fine!
- Proceed with Imager
- Imager will erase and format it

---

## Quick Checklist

- [ ] Card reader properly connected to Mac
- [ ] Tried different USB port
- [ ] Card lock switch is unlocked
- [ ] Card appears in Finder or Disk Utility
- [ ] If not, tried ejecting and re-inserting
- [ ] Checked System Information for reader

---

## Next Steps

**If card appears in Imager:**
- ✅ Proceed with writing OS
- Don't worry about reading it first

**If card doesn't appear anywhere:**
- Try solutions above
- May need new SD card
- Or different card reader

---

*Most important: Can Imager see the card? That's what matters for setup!*
