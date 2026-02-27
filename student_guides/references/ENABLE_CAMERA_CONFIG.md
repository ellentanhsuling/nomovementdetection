# Enable Camera in Config File

## Problem: "no cameras available"

Even though video devices exist, the camera needs to be explicitly enabled in the config file.

---

## Step 1: Check Current Config

```bash
cat /boot/firmware/config.txt | grep -i camera
```

OR if that file doesn't exist:

```bash
cat /boot/config.txt | grep -i camera
```

---

## Step 2: Enable Camera in Config

### For Pi 5 (newer OS):

```bash
sudo nano /boot/firmware/config.txt
```

**OR if that doesn't exist:**

```bash
sudo nano /boot/config.txt
```

### Add or Uncomment This Line:

Look for:
```
#camera_auto_detect=1
```

**Remove the `#` to uncomment:**
```
camera_auto_detect=1
```

**OR if it doesn't exist, add it:**
```
camera_auto_detect=1
```

### Save and Exit:
- Press `Ctrl+X`
- Press `Y` to save
- Press `Enter` to confirm

---

## Step 3: Reboot

```bash
sudo reboot
```

**Wait 1-2 minutes for Pi to boot, then SSH back in.**

---

## Step 4: Test Again

After reboot:

```bash
rpicam-hello --list-cameras
```

Should now show your camera!

OR try taking a photo:

```bash
rpicam-jpeg -o test.jpg
```

---

## Alternative: Check Physical Connection

If enabling in config doesn't work:

1. **Power off Pi**
2. **Check camera cable:**
   - Is it fully inserted?
   - Is the latch down and locked?
   - Is the cable straight (not bent)?

3. **Reseat the cable:**
   - Unlock latch
   - Remove cable
   - Re-insert cable (make sure it's straight)
   - Lock latch

4. **Power on and test again**

---

## Troubleshooting

### Still "no cameras available" after enabling?

1. **Check config file was saved:**
   ```bash
   cat /boot/firmware/config.txt | grep camera
   ```
   Should show: `camera_auto_detect=1` (without #)

2. **Check camera module compatibility:**
   - Is it Raspberry Pi Camera Module 3?
   - Or older module? (might need different config)

3. **Check dmesg for errors:**
   ```bash
   dmesg | grep -i camera
   ```
   Look for error messages

4. **Try different camera connector** (if Pi has multiple)

---

## Quick Fix Command

**One-liner to enable camera:**

```bash
# Check which config file exists
if [ -f /boot/firmware/config.txt ]; then
    sudo sed -i 's/#camera_auto_detect=1/camera_auto_detect=1/' /boot/firmware/config.txt
    grep -q "camera_auto_detect=1" /boot/firmware/config.txt || echo "camera_auto_detect=1" | sudo tee -a /boot/firmware/config.txt
elif [ -f /boot/config.txt ]; then
    sudo sed -i 's/#camera_auto_detect=1/camera_auto_detect=1/' /boot/config.txt
    grep -q "camera_auto_detect=1" /boot/config.txt || echo "camera_auto_detect=1" | sudo tee -a /boot/config.txt
fi
```

Then reboot: `sudo reboot`
