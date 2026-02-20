# Check Camera on Raspberry Pi 5

## The `vcgencmd get_camera` Command Doesn't Work

On newer Raspberry Pi OS versions (especially Pi 5), the old `vcgencmd get_camera` command may not be available. Let's use modern methods instead.

---

## Method 1: Use libcamera (Modern Method)

**This is the recommended way for Pi 5:**

```bash
libcamera-hello --list-cameras
```

**What you should see:**
- List of detected cameras
- Camera name/model
- Available resolutions

**If you see your camera listed:** ✅ Camera is detected and working!

**If you get an error:** Camera might not be detected or libraries not installed.

---

## Method 2: Check if Camera Libraries are Installed

**First, check if libcamera is installed:**

```bash
which libcamera-hello
```

**If command not found, install it:**

```bash
sudo apt update
sudo apt install -y libcamera-apps
```

**Then try again:**
```bash
libcamera-hello --list-cameras
```

---

## Method 3: Check Camera in Device Tree

**Check if camera is detected at hardware level:**

```bash
ls -la /dev/video*
```

**What you should see:**
- `/dev/video0` or `/dev/video1` (camera device)
- If you see video devices, camera hardware is detected

**Also check:**
```bash
v4l2-ctl --list-devices
```

(If `v4l2-ctl` not found, install: `sudo apt install -y v4l-utils`)

---

## Method 4: Check Config File

**Check if camera is enabled in config:**

```bash
cat /boot/firmware/config.txt | grep -i camera
```

**OR:**

```bash
cat /boot/config.txt | grep -i camera
```

**Look for:**
- `camera_auto_detect=1` (should be uncommented)
- Any camera-related settings

---

## Method 5: Take a Test Photo

**The best test - try to actually use the camera:**

```bash
libcamera-jpeg -o test.jpg
```

**If this works:**
- ✅ Camera is working!
- File `test.jpg` will be created
- Check it: `ls -lh test.jpg`

**If this fails:**
- Camera might not be detected
- Or libraries not installed
- Or camera not enabled

---

## Quick Diagnostic Commands

**Run these in order:**

1. **Check OS version:**
   ```bash
   cat /etc/os-release
   ```

2. **Check Pi model:**
   ```bash
   cat /proc/device-tree/model
   ```

3. **List cameras:**
   ```bash
   libcamera-hello --list-cameras
   ```

4. **Check video devices:**
   ```bash
   ls -la /dev/video*
   ```

5. **Try taking photo:**
   ```bash
   libcamera-jpeg -o test.jpg && echo "SUCCESS!" || echo "FAILED"
   ```

---

## Enable Camera if Not Working

**If camera isn't detected, enable it:**

1. **Edit config file:**
   ```bash
   sudo nano /boot/firmware/config.txt
   ```
   (Or `/boot/config.txt` if that doesn't exist)

2. **Add or uncomment:**
   ```
   camera_auto_detect=1
   ```

3. **Save and reboot:**
   ```bash
   sudo reboot
   ```

4. **After reboot, test again:**
   ```bash
   libcamera-hello --list-cameras
   ```

---

## Troubleshooting

### "libcamera-hello: command not found"
**Install camera apps:**
```bash
sudo apt update
sudo apt install -y libcamera-apps libcamera-dev
```

### "No cameras available"
**Possible causes:**
1. Camera not physically connected properly
2. Camera not enabled in config
3. Camera module incompatible

**Check:**
- Physical connection (cable, latch)
- Config file has `camera_auto_detect=1`
- Power cycle Pi

### Camera detected but can't take photos
**Check permissions:**
```bash
groups
```
Should include `video` group. If not:
```bash
sudo usermod -a -G video $USER
```
Then log out and back in (or reboot).

---

## For Your Project

**Once camera is working, you'll need:**

1. **Install Python camera library:**
   ```bash
   pip3 install picamera2
   ```

2. **Test Python access:**
   ```python
   python3 -c "from picamera2 import Picamera2; cam = Picamera2(); print('Camera OK!')"
   ```

---

## Next Steps

1. **Run:** `libcamera-hello --list-cameras`
2. **If camera listed:** ✅ You're good! Continue setup.
3. **If not listed:** Check physical connection and config file.
4. **Install libraries:** `sudo apt install -y libcamera-apps libcamera-dev`

---

**Start with: `libcamera-hello --list-cameras` - this is the modern way to check cameras on Pi 5!**
