# Frequently Asked Questions (FAQ) and Troubleshooting Guide

This comprehensive guide consolidates all common issues and solutions encountered during the Raspberry Pi 5 monitoring system setup.

---

## Table of Contents

1. [Camera Issues](#camera-issues)
2. [SSL Certificate Errors](#ssl-certificate-errors)
3. [System Date and Time Issues](#system-date-and-time-issues)
4. [Virtual Environment Issues](#virtual-environment-issues)
5. [File Transfer Issues](#file-transfer-issues)
6. [Python Import Errors](#python-import-errors)
7. [Alert Configuration Issues](#alert-configuration-issues)
8. [ThingSpeak Integration Issues](#thingspeak-integration-issues)
9. [Discord Webhook Issues](#discord-webhook-issues)
10. [Network and SSH Issues](#network-and-ssh-issues)
11. [SD Card Issues](#sd-card-issues)
12. [General Setup Questions](#general-setup-questions)

---

## Camera Issues

### Problem: `vcgencmd get_camera` returns "Command not registered"

**Error Message:**
```
vc_gencmd_read_response returned -1 error=1 error_msg="Command not registered"
```

**Cause:** This command is deprecated on Raspberry Pi 5 and newer OS versions.

**Solution:** Use modern camera commands instead:

```bash
# Method 1: Use rpicam (recommended for Pi 5)
rpicam-hello --list-cameras

# Method 2: Use libcamera (if rpicam not available)
libcamera-hello --list-cameras
```

**Reference:** See `references/CAMERA_CHECK_PI5.md` for detailed camera checking methods.

---

### Problem: `libcamera-hello: command not found`

**Error Message:**
```
libcamera-hello: command not found
```

**Cause:** The command name changed in newer Pi OS versions, or package not installed.

**Solution:**

1. **Try the new command name:**
   ```bash
   rpicam-hello --list-cameras
   ```

2. **If that doesn't work, install camera apps:**
   ```bash
   sudo apt update
   sudo apt install -y libcamera-apps
   ```

3. **Check what commands are available:**
   ```bash
   ls /usr/bin/libcamera*
   ls /usr/bin/rpicam*
   ```

**Reference:** See `references/FIX_LIBCAMERA.md` for more details.

---

### Problem: Camera shows "No cameras available!" but `/dev/video*` exists

**Error Message:**
```
No cameras available!
```

**But:**
```bash
ls /dev/video*
# Shows: /dev/video0 /dev/video1
```

**Cause:** Camera hardware is detected, but not enabled in config file.

**Solution:**

1. **Enable camera in config file:**
   ```bash
   sudo nano /boot/firmware/config.txt
   ```
   (Or `/boot/config.txt` if that file exists)

2. **Add or uncomment this line:**
   ```
   camera_auto_detect=1
   ```

3. **Save and reboot:**
   ```bash
   sudo reboot
   ```

4. **After reboot, test again:**
   ```bash
   rpicam-hello --list-cameras
   ```

**Reference:** See `references/ENABLE_CAMERA_CONFIG.md` and `references/CHECK_AND_ENABLE_CAMERA.md`.

---

### Problem: Camera timeout error

**Error Message:**
```
ERROR: Device timeout detected, attempting a restart!!!
```

**Cause:** Physical connection issue - camera cable not properly seated.

**Solution:**

1. **Power off the Pi:**
   ```bash
   sudo shutdown -h now
   ```

2. **Wait for shutdown, then unplug power**

3. **Reseat the camera cable:**
   - Gently lift the CSI connector latch
   - Remove the ribbon cable
   - Re-insert the cable firmly (connector facing away from Ethernet port)
   - Push latch down to lock

4. **Power on and test:**
   ```bash
   rpicam-jpeg -o test.jpg
   ```

**Reference:** See `references/CAMERA_PHYSICAL_TROUBLESHOOTING.md` and `references/CAMERA_TIMEOUT_FIX.md`.

---

### Problem: Camera not detected in raspi-config

**Symptom:** Camera option doesn't appear in Interface Options.

**Solution:**

1. **Enable camera manually in config file:**
   ```bash
   sudo nano /boot/firmware/config.txt
   ```

2. **Add:**
   ```
   camera_auto_detect=1
   ```

3. **Reboot:**
   ```bash
   sudo reboot
   ```

**Reference:** See `references/ENABLE_CAMERA.md`.

---

## SSL Certificate Errors

### Problem: SSL certificate verification failed when installing packages

**Error Message:**
```
SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate is not yet valid (_ssl.c:1029)'))
```

**OR:**

```
SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1029)'))
```

**Cause:** System date/time is incorrect, causing SSL certificates to appear invalid.

**Solution:**

1. **Check current system date:**
   ```bash
   date
   ```

2. **If date is wrong, set it manually:**
   ```bash
   sudo date -s "2024-01-15 14:30:00"
   ```
   (Replace with current date/time)

3. **Enable NTP (Network Time Protocol) for automatic sync:**
   ```bash
   sudo timedatectl set-ntp true
   ```

4. **Verify time sync:**
   ```bash
   timedatectl status
   ```

5. **Now try pip install again:**
   ```bash
   pip install --upgrade pip
   ```

**Alternative (if date fix doesn't work):**

Use trusted hosts for pip (temporary workaround):
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package-name>
```

---

### Problem: SSL certificate verification failed when connecting to ThingSpeak/Discord

**Error Message:**
```
SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed'))
```

**When:** Connecting to ThingSpeak API or Discord webhook.

**Solution:**

This is handled in the code with `verify=False` in requests. If you're still seeing errors:

1. **Check system date is correct:**
   ```bash
   date
   sudo timedatectl set-ntp true
   ```

2. **The code should already have:**
   ```python
   import urllib3
   urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
   requests.get(url, verify=False)
   ```

3. **If errors persist, check your code has these workarounds.**

**Note:** `verify=False` is a workaround for development. For production, fix the system date/time instead.

---

## System Date and Time Issues

### Problem: System date is wrong (shows old date)

**Symptom:**
```bash
date
# Shows: Mon Jan  1 00:00:00 UTC 2020  (wrong!)
```

**Cause:** Raspberry Pi doesn't have a battery-backed clock. If it boots without internet, date resets.

**Solution:**

1. **Set date manually:**
   ```bash
   sudo date -s "2024-01-15 14:30:00"
   ```
   (Use current date/time)

2. **Enable automatic time sync:**
   ```bash
   sudo timedatectl set-ntp true
   ```

3. **Verify:**
   ```bash
   timedatectl status
   date
   ```

**Important:** Always ensure Pi has internet connection on boot for automatic time sync.

---

## Virtual Environment Issues

### Problem: Module not found even though installed

**Error Message:**
```
ModuleNotFoundError: No module named 'shared'
```

**Cause:** Running Python script from wrong directory, or virtual environment not activated.

**Solution:**

1. **Always activate virtual environment first:**
   ```bash
   cd ~/raspberry
   source venv/bin/activate
   ```

2. **Run from project directory:**
   ```bash
   cd ~/raspberry/non_movement
   python main.py
   ```

3. **If still errors, check Python path:**
   ```python
   # In your script, add at the top:
   import sys
   sys.path.insert(0, "..")  # Adds parent directory to path
   ```

---

### Problem: Can't access system-installed packages (like libcamera) in venv

**Error Message:**
```
ModuleNotFoundError: No module named 'libcamera'
```

**Cause:** Virtual environment doesn't have access to system packages.

**Solution:**

**Recreate venv with system site packages:**
```bash
cd ~/raspberry
rm -rf venv
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

**Then reinstall your packages:**
```bash
pip install pyyaml python-dotenv requests numpy opencv-python Pillow python-dateutil
```

**Important:** Always specify the full path when creating venv:
```bash
cd ~/raspberry  # Be in the raspberry directory
python3 -m venv venv  # Creates venv in current directory
```

---

### Problem: Virtual environment not activating

**Error Message:**
```
bash: venv/bin/activate: No such file or directory
```

**Cause:** Not in the right directory, or venv not created.

**Solution:**

1. **Check you're in the right directory:**
   ```bash
   pwd
   # Should show: /home/pi/raspberry
   ```

2. **Check venv exists:**
   ```bash
   ls -la venv
   ```

3. **If venv doesn't exist, create it:**
   ```bash
   cd ~/raspberry
   python3 -m venv venv
   source venv/bin/activate
   ```

---

## File Transfer Issues

### Problem: Files corrupted or empty after SCP transfer

**Symptom:** File shows as empty or has syntax errors after transfer.

**Solution:**

1. **Transfer entire directory structure:**
   ```bash
   # From your computer:
   cd ~/Documents/raspberry
   scp -r non_movement pi@<pi-ip>:/home/pi/raspberry/
   scp -r shared pi@<pi-ip>:/home/pi/raspberry/
   ```

2. **Verify files on Pi:**
   ```bash
   # On Pi:
   cd ~/raspberry/non_movement
   ls -la
   cat main.py | head -20  # Check file has content
   ```

3. **If files are corrupted, re-transfer:**
   ```bash
   # Delete on Pi first:
   rm -rf ~/raspberry/non_movement
   rm -rf ~/raspberry/shared
   
   # Re-transfer from computer
   ```

**Reference:** See `references/TRANSFER_PROJECT_SCP.md` for detailed SCP instructions.

---

### Problem: Directory doesn't exist error during SCP

**Error Message:**
```
scp: dest open "/home/pi/raspberry/shared/data/thingspeak_logger.py": No such file or directory
```

**Cause:** Directory structure doesn't exist on Pi.

**Solution:**

1. **Create directory structure on Pi first:**
   ```bash
   # On Pi:
   mkdir -p ~/raspberry/shared/data
   mkdir -p ~/raspberry/shared/alerts
   mkdir -p ~/raspberry/shared/utils
   mkdir -p ~/raspberry/shared/base
   mkdir -p ~/raspberry/non_movement
   ```

2. **Then transfer files:**
   ```bash
   # From your computer:
   scp -r shared pi@<pi-ip>:/home/pi/raspberry/
   ```

**Better approach:** Transfer entire directories at once:
```bash
scp -r raspberry pi@<pi-ip>:/home/pi/
```

---

## Python Import Errors

### Problem: `NameError: name 'Optional' is not defined`

**Error Message:**
```
NameError: name 'Optional' is not defined
```

**Cause:** Missing import statement.

**Solution:**

Add import at top of file:
```python
from typing import Optional
```

**Location:** Check `shared/alerts/logger.py` and any file using `Optional`.

---

### Problem: Configuration validation error - "At least one sensor must be configured"

**Error Message:**
```
Configuration errors: - At least one sensor (PIR or Ultrasonic) must be configured
```

**Cause:** Config validator requires PIR or Ultrasonic, but you're using camera-only setup.

**Solution:**

This should already be fixed in `shared/utils/config_loader.py`. If you see this error:

1. **Check config file allows camera-only:**
   ```yaml
   sensors:
     camera:
       enabled: true
   ```

2. **Verify `config_loader.py` allows camera-only configuration.**

---

## Alert Configuration Issues

### Problem: Discord alerts not showing up

**Symptom:** System logs show "CONCERNING status detected" but no Discord message.

**Cause:** Alert escalation configuration issue.

**Solution:**

1. **Check `config.yaml`:**
   ```yaml
   alerts:
     escalation:
       enabled: false  # Disable for simple alerts
   
     webhook:
       enabled: true
       type: "discord"
       webhook_urls:
         - "https://discord.com/api/webhooks/YOUR_URL"
   ```

2. **If escalation is enabled, make sure webhook is in escalation levels:**
   ```yaml
   alerts:
     escalation:
       enabled: true
       levels:
         - channels: ["webhook"]  # Include webhook!
           delay_minutes: 0
   ```

3. **Test webhook directly:**
   ```bash
   cd ~/raspberry/non_movement
   source ../venv/bin/activate
   python test_discord_alert.py
   ```

**Reference:** See alert configuration in `non_movement/config.yaml`.

---

### Problem: Alerts sending to wrong channels

**Symptom:** Alerts going to email instead of Discord.

**Solution:**

1. **Check `config.yaml` escalation levels:**
   ```yaml
   alerts:
     escalation:
       levels:
         - channels: ["webhook"]  # Should include webhook
   ```

2. **Disable escalation if you want simple alerts:**
   ```yaml
   alerts:
     escalation:
       enabled: false
   ```

---

## ThingSpeak Integration Issues

### Problem: ThingSpeak rate limit exceeded

**Error Message:**
```
Rate limit exceeded
```

**Cause:** ThingSpeak free tier allows 3 messages per 15 seconds.

**Solution:**

1. **Check your code sends data at appropriate intervals:**
   ```python
   # Don't send every cycle - batch or throttle
   if time.time() - last_send > 15:  # Wait 15 seconds between sends
       thingspeak_logger.send_data(...)
   ```

2. **Reduce data frequency in config:**
   ```yaml
   system:
     check_interval: 30  # Check every 30 seconds, not every second
   ```

**Reference:** ThingSpeak limits: 3 messages/15 seconds, 8,200/day.

---

### Problem: ThingSpeak data not showing up

**Symptom:** Code runs without errors, but no data in ThingSpeak dashboard.

**Solution:**

1. **Verify API key is correct:**
   ```yaml
   data_logging:
     thingspeak:
       write_api_key: "YOUR_KEY_HERE"  # Check this is correct
   ```

2. **Check ThingSpeak channel ID matches:**
   ```yaml
   data_logging:
     thingspeak:
       channel_id: "YOUR_CHANNEL_ID"
   ```

3. **Test with curl:**
   ```bash
   curl "https://api.thingspeak.com/update?api_key=YOUR_KEY&field1=1"
   ```

4. **Check ThingSpeak dashboard - data may take 15 seconds to appear.**

---

## Discord Webhook Issues

### Problem: Discord webhook returns 404

**Error Message:**
```
404 Not Found
```

**Cause:** Webhook URL is incorrect or webhook was deleted.

**Solution:**

1. **Create new webhook in Discord:**
   - Server Settings → Integrations → Webhooks
   - Create new webhook
   - Copy the webhook URL

2. **Update `config.yaml`:**
   ```yaml
   alerts:
     webhook:
       webhook_urls:
         - "https://discord.com/api/webhooks/NEW_URL_HERE"
   ```

3. **Test webhook:**
   ```bash
   curl -X POST "YOUR_WEBHOOK_URL" -H "Content-Type: application/json" -d '{"content":"Test"}'
   ```

---

### Problem: Discord webhook returns 401 Unauthorized

**Error Message:**
```
401 Unauthorized
```

**Cause:** Webhook was deleted or URL is invalid.

**Solution:** Create a new webhook and update the URL in config.

---

## Network and SSH Issues

### Problem: Can't find Pi's IP address

**Symptom:** Need to SSH but don't know Pi's IP.

**Solution:**

1. **Check router admin page:**
   - Log into router (usually http://192.168.1.1)
   - Look for "Connected Devices" or "DHCP Clients"
   - Find "raspberrypi" or "Raspberry Pi"

2. **Use network scanner:**
   ```bash
   # On Mac/Linux:
   arp -a | grep -i raspberry
   
   # Or use find_pi.sh script:
   ./find_pi.sh
   ```

3. **Use mDNS (if available):**
   ```bash
   ssh pi@raspberrypi.local
   ```

4. **Use Raspberry Pi Connect:**
   - If enabled in Imager
   - Check connect.raspberrypi.com dashboard

**Reference:** See `references/FIND_PI_NOW.md` for detailed instructions.

---

### Problem: Can't connect via SSH

**Error Message:**
```
ssh: connect to host <ip> port 22: Connection refused
```

**Solution:**

1. **Verify SSH is enabled:**
   - Check `/boot/ssh` file exists (or was created in Imager)
   - If not, create it: `touch /boot/ssh` (on SD card from computer)

2. **Check Pi is on network:**
   ```bash
   ping <pi-ip>
   ```

3. **Check SSH service is running (if you can access Pi another way):**
   ```bash
   sudo systemctl status ssh
   ```

4. **Enable SSH:**
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

---

## SD Card Issues

### Problem: SD card not detected on Mac

**Symptom:** SD card doesn't appear in Finder or Disk Utility.

**Solution:**

1. **Check card reader connection:**
   - Try different USB port
   - Try different card reader

2. **Check card orientation:**
   - Flip card over (contacts face down usually)
   - See `references/SD_CARD_ORIENTATION.md`

3. **Use Terminal to check:**
   ```bash
   diskutil list
   ```

4. **Check if card is locked:**
   - Small switch on side of SD card
   - Make sure it's unlocked

**Reference:** See `references/SD_CARD_MAC_TROUBLESHOOTING.md` for detailed Mac troubleshooting.

---

### Problem: SD card shows as "bootfs" in Imager

**Symptom:** Imager shows "bootfs" instead of full card size.

**Solution:**

1. **Select the main card entry** (showing full size like "32 GB")
2. **Don't select individual partitions**
3. **If "exclude system files" option appears, leave it unchecked**

**Reference:** See `references/SD_CARD_BOOTFS_PARTITION.md` and `references/IMAGER_SD_CARD_SELECTION.md`.

---

## General Setup Questions

### Q: Do I need to reformat a previously used SD card?

**A:** No! Raspberry Pi Imager automatically erases and formats the card. Just select it and write the OS.

**Reference:** See `references/SD_CARD_PREVIOUSLY_USED.md`.

---

### Q: Which way does the SD card go in?

**A:** Gold contacts (teeth) face **DOWN** (towards the Pi board) when inserting into the Pi. For card readers, check the reader - contacts must touch the pins inside.

**Reference:** See `references/SD_CARD_ORIENTATION.md`.

---

### Q: Can I change WiFi after initial setup?

**A:** Yes! You can:
- Edit `/etc/wpa_supplicant/wpa_supplicant.conf` on Pi
- Or use `raspi-config` → Network Options → WiFi
- Or use Raspberry Pi Imager to set WiFi initially

**Reference:** See `references/WIFI_CONFIGURATION_GUIDE.md`.

---

### Q: What is Raspberry Pi Connect?

**A:** A free service that lets you access your Pi remotely without knowing its IP address. Optional - you can use SSH instead.

**Reference:** See `references/RASPBERRY_PI_CONNECT_GUIDE.md` and `references/RASPBERRY_PI_CONNECT_TOKEN.md`.

---

### Q: Do I need HDMI/monitor?

**A:** No! This project uses SSH only. Everything can be done remotely.

**Reference:** See `references/SETUP_STEP_BY_STEP.md` - all steps are SSH-based.

---

### Q: Where should I run commands - in raspberry folder or non_movement folder?

**A:** 
- **Virtual environment setup:** `~/raspberry` (root project folder)
- **Running the project:** `~/raspberry/non_movement` (project folder)
- **Installing packages:** `~/raspberry` (with venv activated)

**Always specify the full path in instructions!**

---

### Q: How do I know if the Pi is booting without a monitor?

**A:** 
- **Red LED:** Power is on (should stay on)
- **Green LED:** SD card activity (flashes during boot, then occasional flashes)
- **After 30-60 seconds:** Pi should be ready for SSH

---

## Quick Diagnostic Commands

**Run these to check system status:**

```bash
# Check system date
date

# Check camera
rpicam-hello --list-cameras

# Check Python version
python3 --version

# Check virtual environment
which python  # Should show venv path when activated

# Check network
ifconfig

# Check disk space
df -h

# Check system temperature
vcgencmd measure_temp
```

---

## Getting More Help

1. **Check specific guides:**
   - Camera: `references/CAMERA_CHECK_PI5.md`, `references/FIX_LIBCAMERA.md`
   - Setup: `references/SETUP_STEP_BY_STEP.md`
   - Transfer: `references/TRANSFER_PROJECT_SCP.md`
   - Services: `references/FREE_SERVICES_SETUP.md`

2. **Official Raspberry Pi documentation:**
   - https://www.raspberrypi.com/documentation/

3. **Check logs:**
   ```bash
   tail -f ~/raspberry/logs/monitoring.log
   ```

---

**Last Updated:** Based on actual setup experience with Raspberry Pi 5, Camera Module 3, and full system integration.
