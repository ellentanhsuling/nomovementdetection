# Fix Camera Timeout Error

## Error Message
```
ERROR: Camera frontend has timed out!
Please check that your camera sensor connector is attached securely.
```

## Problem
Camera is detected but connection is unstable - cable might be loose or not fully seated.

---

## Solution: Reseat Camera Cable

### Step 1: Power Off Pi
```bash
sudo shutdown -h now
```
Wait for Pi to fully shut down (red LED off).

### Step 2: Check Physical Connection

**On Raspberry Pi 5:**

1. **Locate CSI connector:**
   - Small connector near GPIO pins
   - Has a plastic latch

2. **Check current state:**
   - Is latch down and locked?
   - Is cable fully inserted?
   - Is cable straight (not bent)?

3. **Unlock latch:**
   - Gently lift the latch
   - Don't force it

4. **Remove cable:**
   - Pull cable straight out
   - Don't bend or twist it

5. **Inspect cable:**
   - Check contacts (should be clean)
   - Check for damage or bends
   - Make sure cable is straight

6. **Re-insert cable:**
   - Check orientation (connector has specific side)
   - Push in **firmly** until it stops
   - Should go in about 1-2mm
   - **Important:** Push it in all the way!

7. **Lock latch:**
   - Push latch down firmly
   - Should click/lock into place
   - Cable should be secure (no movement)

8. **Double-check:**
   - Latch is locked
   - Cable is fully inserted
   - No visible gaps
   - Cable is straight

### Step 3: Power On and Test

1. **Power on Pi**
2. **Wait 1-2 minutes** for boot
3. **SSH back in:**
   ```bash
   ssh pi@172.20.83.63
   ```

4. **Test camera detection:**
   ```bash
   rpicam-hello --list-cameras
   ```

5. **Try taking photo:**
   ```bash
   rpicam-jpeg -o test.jpg
   ```

---

## Alternative: Try Lower Resolution

If reseating doesn't work, try a lower resolution:

```bash
rpicam-jpeg --width 2304 --height 1296 -o test.jpg
```

OR

```bash
rpicam-jpeg --width 1536 --height 864 -o test.jpg
```

Lower resolutions are more stable if there's a connection issue.

---

## Check for Other Issues

### Check Power Supply
Camera needs good power. Make sure:
- Using official Pi 5 power supply (5V/5A)
- Power supply is adequate
- No under-voltage warnings

Check for power issues:
```bash
vcgencmd get_throttled
```

Should show `throttled=0x0` (no throttling).

### Check Temperature
```bash
vcgencmd measure_temp
```

High temperature can cause issues.

### Check System Messages
```bash
dmesg | grep -i camera | tail -20
```

Look for connection errors.

---

## Common Causes

1. **Cable not fully inserted** (most common)
   - Push cable in all the way
   - Latch must be locked

2. **Loose connection**
   - Cable moves slightly
   - Latch not fully locked

3. **Bent or damaged cable**
   - Check for visible damage
   - Cable should be straight

4. **Insufficient power**
   - Use proper power supply
   - Check for under-voltage

5. **Cable orientation wrong**
   - Check connector orientation
   - Don't force it

---

## If Still Not Working

1. **Try different cable** (if available)
2. **Check camera module** (might be faulty)
3. **Try different CSI port** (if Pi has multiple)
4. **Check for firmware updates:**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

---

## Quick Checklist

- [ ] Pi powered off before reseating
- [ ] Cable fully removed
- [ ] Cable inspected (clean, straight, no damage)
- [ ] Cable re-inserted firmly (all the way in)
- [ ] Latch locked down
- [ ] No visible gaps
- [ ] Cable is straight
- [ ] Pi powered on and tested

---

**Most likely fix: Reseat the cable and make sure it's pushed in ALL THE WAY with the latch locked!**
