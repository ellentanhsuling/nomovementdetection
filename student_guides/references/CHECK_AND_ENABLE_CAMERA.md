# Check and Enable Camera in Config

## You Have Both Config Files

- `/boot/config.txt` - older location (91 bytes)
- `/boot/firmware/config.txt` - **This is the one used on Pi 5!** (1247 bytes)

**We need to edit `/boot/firmware/config.txt`**

---

## Step 1: Check Current Camera Settings

```bash
cat /boot/firmware/config.txt | grep -i camera
```

This shows if camera is already enabled or commented out.

---

## Step 2: Edit the Config File

```bash
sudo nano /boot/firmware/config.txt
```

---

## Step 3: Look For Camera Settings

**Look for any of these lines:**
- `#camera_auto_detect=1` (commented out - remove the #)
- `camera_auto_detect=1` (already enabled - good!)
- No camera line at all (need to add it)

---

## Step 4: Enable Camera

**If you see `#camera_auto_detect=1`:**
- Remove the `#` to make it: `camera_auto_detect=1`

**If you don't see any camera line:**
- Add this line anywhere in the file: `camera_auto_detect=1`

---

## Step 5: Save and Reboot

- Press `Ctrl+X`
- Press `Y` to save
- Press `Enter` to confirm

Then reboot:
```bash
sudo reboot
```

---

## Quick Check Command

**Before editing, see what's there:**
```bash
cat /boot/firmware/config.txt | grep -i camera
```

**If nothing shows, camera isn't enabled yet.**
