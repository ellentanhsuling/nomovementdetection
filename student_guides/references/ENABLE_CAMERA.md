# Enable Camera on Raspberry Pi

## Problem: Camera Not Showing in raspi-config

If you can't see the camera option in raspi-config, let's check and enable it manually.

---

## Step 1: Check if Camera is Detected

**In your SSH terminal (on the Pi), run:**

```bash
vcgencmd get_camera
```

**What you should see:**
- `supported=1 detected=1` = Camera is detected! ✅
- `supported=1 detected=0` = Camera hardware supported but not detected (connection issue)
- `supported=0 detected=0` = Camera not supported or not detected

---

## Step 2: Check Camera Connection

**If you see `detected=0`, the camera might not be properly connected:**

1. **Check the cable:**
   - Make sure ribbon cable is fully inserted into CSI connector
   - Latch should be down and locked
   - Cable should be straight (not bent)

2. **Check the connector:**
   - On Pi 5, the CSI connector is near the GPIO pins
   - Make sure cable is inserted the right way (connector has a specific orientation)

3. **Power cycle:**
   - Unplug Pi power
   - Wait 10 seconds
   - Plug back in
   - Wait 1 minute
   - Check again: `vcgencmd get_camera`

---

## Step 3: Enable Camera Manually (If Not in raspi-config)

**If camera is detected but not showing in raspi-config, enable it manually:**

### Method 1: Edit config.txt

1. **Edit the config file:**
   ```bash
   sudo nano /boot/firmware/config.txt
   ```
   
   (Note: On newer Pi OS, it might be `/boot/config.txt` instead)

2. **Look for this line:**
   ```
   camera_auto_detect=1
   ```
   
   **OR add this line if it doesn't exist:**
   ```
   camera_auto_detect=1
   ```

3. **Also check for (and uncomment if needed):**
   ```
   #camera_auto_detect=1
   ```
   Remove the `#` to uncomment it:
   ```
   camera_auto_detect=1
   ```

4. **Save and exit:**
   - Press `Ctrl+X`
   - Press `Y` to save
   - Press `Enter` to confirm

5. **Reboot:**
   ```bash
   sudo reboot
   ```

6. **Wait 1 minute, SSH back in, and check:**
   ```bash
   vcgencmd get_camera
   ```

### Method 2: Check Which Config File Exists

**On Pi 5 with newer OS, the config might be in a different location:**

```bash
# Check which config file exists:
ls -la /boot/firmware/config.txt
ls -la /boot/config.txt
```

**Edit whichever one exists!**

---

## Step 4: Test Camera After Enabling

**Once camera is enabled, test it:**

1. **Check detection:**
   ```bash
   vcgencmd get_camera
   ```
   Should show: `supported=1 detected=1`

2. **List cameras:**
   ```bash
   libcamera-hello --list-cameras
   ```
   Should list your camera

3. **Take a test photo:**
   ```bash
   libcamera-jpeg -o test.jpg
   ```
   
4. **Check if photo was created:**
   ```bash
   ls -lh test.jpg
   ```
   Should show file size > 0

---

## Troubleshooting

### "vcgencmd: command not found"
**Install it:**
```bash
sudo apt update
sudo apt install -y libraspberrypi-bin
```

### Camera still not detected after enabling
1. **Double-check physical connection:**
   - Cable fully inserted?
   - Latch locked?
   - Cable not damaged?

2. **Try different camera port** (if Pi has multiple):
   - Some Pi models have multiple camera connectors
   - Check which one you're using

3. **Check camera module compatibility:**
   - Is it Raspberry Pi Camera Module 3?
   - Or older module? (might need different config)

### "detected=0" but cable looks connected
- **Try reseating the cable:**
  1. Power off Pi
  2. Unlock latch
  3. Remove cable
  4. Re-insert cable (make sure it's straight)
  5. Lock latch
  6. Power on
  7. Check again

---

## Quick Checklist

- [ ] Camera cable is physically connected
- [ ] Cable latch is locked
- [ ] Ran `vcgencmd get_camera` to check status
- [ ] Edited config.txt to enable camera
- [ ] Rebooted Pi
- [ ] Checked again: `vcgencmd get_camera`
- [ ] Tested camera: `libcamera-hello --list-cameras`

---

## Next Steps

Once camera is enabled and detected:
- Continue with Step 6 in `SETUP_STEP_BY_STEP.md`
- Install camera libraries: `sudo apt install -y libcamera-dev python3-libcamera`
- Test camera functionality

---

**Start by running `vcgencmd get_camera` to see what the Pi detects!**
