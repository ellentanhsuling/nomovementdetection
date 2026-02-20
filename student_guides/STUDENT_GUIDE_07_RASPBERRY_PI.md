# Student Build Guide - Step 7: Deploy to Raspberry Pi

## What You're Doing

Moving your code to Raspberry Pi 5 and connecting the real camera.

---

## Prerequisites

- Raspberry Pi 5
- Raspberry Pi Camera Module 3
- MicroSD card (64GB recommended)
- Power supply (5V/5A for Pi 5)
- Case with cooling

---

## Part 1: Set Up Raspberry Pi OS

**⚠️ Important:** This guide uses **SSH only** - no HDMI/monitor needed!

**Steps:**

1. **Download Raspberry Pi Imager**
   - Go to: https://www.raspberrypi.com/software/
   - Download Raspberry Pi Imager for your computer
   - Install it

2. **Insert SD Card into Computer**
   - Insert SD card into card reader
   - **Note:** Gold contacts (teeth) usually face **DOWN** when inserting
   - Card may show as "Untitled" or "NO NAME" - this is normal!
   - **📖 Help:** See `references/SD_CARD_ORIENTATION.md` and `references/SD_CARD_MAC_TROUBLESHOOTING.md` if card not detected

3. **Write OS to SD Card**
   - Open Raspberry Pi Imager
   - Click "Choose OS" → Select **"Raspberry Pi OS (64-bit)"**
   - Click "Choose Storage" → Select your SD card (select main card, not partitions)
   - Click gear icon (⚙️) for **Advanced Options:**
     - **⚠️ CRITICAL: Enable SSH** - **MUST CHECK THIS!**
     - Set username: `pi` (or your choice)
     - Set password: **WRITE IT DOWN!** (you'll need it for SSH)
     - **Configure WiFi** (optional - you can change later):
       - Enter WiFi SSID and password
       - Or leave unchecked to use Ethernet
     - **Raspberry Pi Connect** (optional - for remote access):
       - If enabled, you'll need a token from connect.raspberrypi.com
       - **📖 Help:** See `references/RASPBERRY_PI_CONNECT_TOKEN.md`
     - Set locale/timezone
   - Click "Save"
   - Click "Write"
   - **Warning:** This will erase all data on SD card - click "Yes"
   - Wait for completion (5-10 minutes)

4. **Eject SD card** and insert into Pi

**📖 References:**
- Official guide: https://www.raspberrypi.com/documentation/computers/getting-started.html
- Detailed setup: `references/SETUP_STEP_BY_STEP.md`
- WiFi setup: `references/WIFI_CONFIGURATION_GUIDE.md`
- Raspberry Pi Connect: `references/RASPBERRY_PI_CONNECT_GUIDE.md`

---

## Part 2: First Boot and Setup

1. **Connect Hardware**
   - Insert SD card into Pi (gold contacts face DOWN)
   - Connect camera module to CSI port (connector facing away from Ethernet port)
   - Connect network: Ethernet cable OR WiFi (if configured in Imager)
   - Connect power supply (5V/5A for Pi 5)

2. **Boot the Pi**
   - Plug in power
   - **Red LED** = Power on (should stay on)
   - **Green LED** = SD card activity (flashes during boot)
   - Wait 30-60 seconds for first boot
   - **No monitor needed** - we'll verify via SSH!

3. **Find Pi's IP Address**
   - **Option 1:** Check router admin page (usually http://192.168.1.1)
     - Look for "Connected Devices" or "DHCP Clients"
     - Find "raspberrypi" or "Raspberry Pi"
   - **Option 2:** Use network scanner
     ```bash
     # On your computer:
     arp -a | grep -i raspberry
     ```
   - **Option 3:** Use mDNS (if available)
     ```bash
     ssh pi@raspberrypi.local
     ```
   - **Option 4:** Use Raspberry Pi Connect (if enabled)
     - Check connect.raspberrypi.com dashboard
   - **📖 Help:** See `references/FIND_PI_NOW.md` for detailed instructions

4. **SSH into Pi**
   ```bash
   # From your computer:
   ssh pi@<pi-ip-address>
   # Example: ssh pi@192.168.1.100
   ```
   - First time: Type `yes` to accept host key
   - Enter password (the one you set in Imager)

5. **Set System Date/Time** (IMPORTANT!)
   ```bash
   # Check current date
   date
   
   # If date is wrong, set it manually:
   sudo date -s "2024-01-15 14:30:00"  # Use current date/time!
   
   # Enable automatic time sync:
   sudo timedatectl set-ntp true
   
   # Verify:
   timedatectl status
   ```
   **Why?** Wrong date causes SSL certificate errors when installing packages!

6. **Run initial setup**
   ```bash
   sudo raspi-config
   ```
   - Change password (if desired)
   - **Enable camera:** Interface Options → Camera → Enable
   - Expand filesystem: Advanced Options → Expand Filesystem
   - Set locale/timezone: Localisation Options
   - Finish and reboot

7. **Reboot**
   ```bash
   sudo reboot
   ```
   - Wait for reboot (30 seconds)
   - SSH back in: `ssh pi@<pi-ip>`

---

## Part 3: Install System Dependencies

**⚠️ Important:** Run these commands **on the Raspberry Pi** (via SSH).

**Step 1: Update System**
```bash
# Make sure you're SSH'd into the Pi
sudo apt update
sudo apt upgrade -y
# This may take 10-20 minutes - be patient!
```

**Step 2: Install Camera Libraries**
```bash
sudo apt install -y libcamera-dev python3-libcamera libcamera-apps
```

**Step 3: Install Python Development Tools**
```bash
sudo apt install -y python3-pip python3-venv git
```

**Step 4: Verify Camera Works**

**⚠️ Note:** On Pi 5, use `rpicam` instead of `libcamera`:

```bash
# Try this first (Pi 5):
rpicam-hello --list-cameras

# If that doesn't work, try:
libcamera-hello --list-cameras

# If camera not detected, enable it:
sudo nano /boot/firmware/config.txt
# Add or uncomment: camera_auto_detect=1
# Save (Ctrl+X, Y, Enter)
sudo reboot
```

**📖 Troubleshooting:**
- See `references/CAMERA_CHECK_PI5.md` for Pi 5 specific camera checks
- See `references/FIX_LIBCAMERA.md` if commands not found
- See `references/ENABLE_CAMERA_CONFIG.md` if camera not detected

---

## Part 4: Transfer Your Code

**⚠️ Important:** Always specify full paths!

**Option 1: Using SCP** (Recommended - from your computer)

**Step 1: From your computer, transfer the project:**
```bash
# Make sure you're in the directory containing the 'raspberry' folder
cd ~/Documents/raspberry  # Or wherever your project is

# Transfer entire project:
scp -r raspberry pi@<pi-ip>:/home/pi/
# Example: scp -r raspberry pi@192.168.1.100:/home/pi/
```

**Step 2: Verify on Pi:**
```bash
# SSH into Pi, then:
cd ~/raspberry
ls -la
# Should see: non_movement, shared, fall_detection folders
```

**Step 3: Create any missing directories:**
```bash
# On Pi:
mkdir -p ~/raspberry/shared/data
mkdir -p ~/raspberry/shared/alerts
mkdir -p ~/raspberry/shared/utils
mkdir -p ~/raspberry/shared/base
```

**Option 2: Using Git** (If code is in repository)
```bash
# On Pi:
cd ~
git clone <your-repo-url>
cd raspberry
```

**Option 3: Using USB drive**
- Copy `raspberry` folder to USB
- Plug USB into Pi
- Mount USB (usually auto-mounted at `/media/pi/`)
- Copy: `cp -r /media/pi/USBNAME/raspberry ~/`

**📖 Reference:** See `references/TRANSFER_PROJECT_SCP.md` for detailed SCP instructions.

---

## Part 5: Set Up Python Environment

**⚠️ Important:** Run these commands **on the Raspberry Pi** (via SSH).

**Step 1: Navigate to Project Directory**
```bash
cd ~/raspberry
# Always specify full path: ~/raspberry
```

**Step 2: Create Virtual Environment with System Site Packages**

**Why `--system-site-packages`?** Allows access to system-installed packages like `libcamera`:

```bash
# Remove old venv if it exists:
rm -rf venv

# Create new venv with system site packages:
python3 -m venv --system-site-packages venv

# Activate it:
source venv/bin/activate

# You should see (venv) in your prompt
```

**Step 3: Fix SSL Issues (if needed)**

If you get SSL certificate errors, use trusted hosts:

```bash
pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

**Step 4: Install Python Packages**

```bash
# Make sure venv is activated (you see (venv) in prompt)

# Install shared dependencies:
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org \
  pyyaml python-dotenv requests numpy opencv-python Pillow python-dateutil

# Install Pi-specific camera package:
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org picamera2

# Install project dependencies (if you have requirements.txt):
cd ~/raspberry/non_movement
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**Step 5: Verify Installation**

```bash
# Check packages installed:
pip list

# Test Python can import:
python3 -c "import cv2; import numpy; import yaml; print('All packages OK!')"

# Test camera access:
python3 -c "from picamera2 import Picamera2; print('Camera library OK!')"
```

**📖 References:**
- Picamera2: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
- If SSL errors persist, see `FAQ_TROUBLESHOOTING.md` → SSL Certificate Errors

---

## Part 6: Connect Camera Module

**Physical connection:**

1. **Locate CSI port** on Pi 5
   - Small connector near GPIO pins
   - Has plastic latch

2. **Insert ribbon cable**
   - Cable from camera module
   - Insert into CSI port
   - Connector facing away from Ethernet port

3. **Lock it**
   - Gently lift latch
   - Push cable in fully
   - Push latch down to lock

4. **Secure camera**
   - Mount in desired location
   - Good field of view
   - Adequate lighting

**Reference**: https://www.raspberrypi.com/documentation/computers/camera_software.html

---

## Part 7: Test Camera

**⚠️ Important:** On Pi 5, use `rpicam` commands, not `libcamera`!

**Step 1: Test Camera Detection**

```bash
# On Pi 5, use rpicam:
rpicam-hello --list-cameras

# If that doesn't work, try:
libcamera-hello --list-cameras

# Should show your camera listed
```

**Step 2: Take Test Photo**

```bash
# On Pi 5:
rpicam-jpeg -o test.jpg

# Or:
libcamera-jpeg -o test.jpg

# Check file was created:
ls -lh test.jpg
# Should show file size > 0
```

**Step 3: View Photo (SSH only setup)**

Since you don't have a monitor, transfer photo to your computer:

```bash
# From your computer (not Pi):
scp pi@<pi-ip>:/home/pi/test.jpg ~/Desktop/
# Then open test.jpg on your computer
```

**Step 4: Test with Python**

```bash
# On Pi, with venv activated:
cd ~/raspberry
source venv/bin/activate

python3 -c "from picamera2 import Picamera2; cam = Picamera2(); cam.start(); print('Camera works!'); cam.stop()"
```

**If camera not detected:**
- Check ribbon cable connection (see `references/CAMERA_PHYSICAL_TROUBLESHOOTING.md`)
- Enable camera in config: `sudo nano /boot/firmware/config.txt` → Add `camera_auto_detect=1`
- Reboot: `sudo reboot`
- **📖 Help:** See `CAMERA_CHECK_PI5.md`, `FIX_LIBCAMERA.md`, `ENABLE_CAMERA_CONFIG.md`

**⚠️ Note:** `vcgencmd get_camera` doesn't work on Pi 5 - use `rpicam-hello` instead!

---

## Part 8: Update Configuration

**Step 1: Edit Non-Movement Config**

```bash
# On Pi:
cd ~/raspberry/non_movement
nano config.yaml
```

**Change these settings:**

```yaml
system:
  use_mock_sensors: false  # Use real camera!
  check_interval: 30  # Check every 30 seconds

# For prototype testing, set short thresholds:
detection:
  no_movement_threshold_active: 0.167  # 10 seconds (for testing)
  no_movement_threshold_sleep: 0.167
  no_movement_threshold_anytime: 0.167
```

**Step 2: Configure Data Logging (ThingSpeak)**

**First, set up ThingSpeak account:**
1. Go to https://thingspeak.com
2. Sign up (free account)
3. Create a new channel
4. Get your Write API Key from API Keys tab

**Then update config.yaml:**
```yaml
data_logging:
  thingspeak:
    enabled: true
    write_api_key: "YOUR_WRITE_API_KEY_HERE"
    channel_id: "YOUR_CHANNEL_ID"  # Optional, for reference
```

**Step 3: Configure Alerts (Discord Webhook)**

**First, set up Discord webhook:**
1. Open Discord
2. Server Settings → Integrations → Webhooks
3. Create new webhook
4. Copy the webhook URL

**Then update config.yaml:**
```yaml
alerts:
  webhook:
    enabled: true
    type: "discord"
    webhook_urls:
      - "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
    timeout: 5
    retry_attempts: 2
  
  # Disable escalation for simple alerts:
  escalation:
    enabled: false
    # If enabled, make sure webhook is in levels:
    levels:
      - channels: ["webhook"]
        delay_minutes: 0
```

**Step 4: Save and Exit**

In nano: Press `Ctrl+X`, then `Y`, then `Enter`

**📖 References:**
- ThingSpeak setup: `references/FREE_SERVICES_SETUP.md`
- Discord setup: `references/FREE_SERVICES_SETUP.md`
- Config examples: `templates/config_non_movement.yaml`

---

## Part 9: Test Real Camera and System

**Step 1: Test Non-Movement Project**

```bash
# On Pi:
cd ~/raspberry/non_movement
source ../venv/bin/activate  # Make sure venv is activated!

python main.py
```

**What to see:**
- Camera initializes successfully
- Real frames being captured
- Detection working
- Logs showing "CONCERNING status detected" when no movement
- No errors

**Step 2: Test ThingSpeak Data Logging**

**Check ThingSpeak dashboard:**
- Go to https://thingspeak.com
- Open your channel
- Go to "Private View" tab
- You should see data appearing (may take 15 seconds due to rate limits)

**Step 3: Test Discord Alerts**

**Test webhook directly:**
```bash
# On Pi:
cd ~/raspberry/non_movement
source ../venv/bin/activate
python test_discord_alert.py  # If you have this test file
```

**Or trigger an alert:**
- Wait for no movement threshold (10 seconds for prototype)
- Check Discord channel for alert message
- Should see formatted message with status

**Step 4: Monitor Logs**

```bash
# In another SSH session or after stopping main.py:
tail -f ~/raspberry/logs/monitoring.log
```

**What to check:**
- No SSL errors
- Camera capturing frames
- ThingSpeak data sending (check rate limits)
- Discord alerts triggering

**Step 5: Test Fall Detection (if building that project)**

```bash
cd ~/raspberry/fall_detection
source ../venv/bin/activate
python main.py
```

**📖 Troubleshooting:**
- If Discord alerts not showing: See `FAQ_TROUBLESHOOTING.md` → Alert Configuration Issues
- If ThingSpeak not working: See `FAQ_TROUBLESHOOTING.md` → ThingSpeak Integration Issues
- If SSL errors: See `FAQ_TROUBLESHOOTING.md` → SSL Certificate Errors

---

## Part 10: Set Up Auto-Start (Optional)

**Create systemd service:**

**File**: `/etc/systemd/system/elderly-monitoring.service`

```ini
[Unit]
Description=Elderly Monitoring System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/raspberry/non_movement
Environment="PATH=/home/pi/raspberry/venv/bin"
ExecStart=/home/pi/raspberry/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable service:**
```bash
sudo systemctl enable elderly-monitoring.service
sudo systemctl start elderly-monitoring.service
```

**Check status:**
```bash
sudo systemctl status elderly-monitoring.service
```

---

## Part 11: Monitor and Maintain

**Check logs:**
```bash
tail -f ~/raspberry/logs/monitoring.log
```

**Check system resources:**
```bash
htop
# or
top
```

**Update code:**
```bash
cd ~/raspberry
git pull  # if using git
# or copy new files
```

---

## Troubleshooting

**📖 Comprehensive Guide:** See `FAQ_TROUBLESHOOTING.md` for detailed solutions!

### Camera not detected
- **Pi 5:** Use `rpicam-hello --list-cameras` (not `vcgencmd get_camera`)
- Check ribbon cable connection (see `references/CAMERA_PHYSICAL_TROUBLESHOOTING.md`)
- Enable camera: `sudo nano /boot/firmware/config.txt` → Add `camera_auto_detect=1`
- Reboot: `sudo reboot`
- **📖 Help:** `references/CAMERA_CHECK_PI5.md`, `references/FIX_LIBCAMERA.md`

### SSL certificate errors
- **Fix system date:** `sudo date -s "YYYY-MM-DD HH:MM:SS"` (use current date!)
- Enable NTP: `sudo timedatectl set-ntp true`
- Use trusted hosts: `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package>`
- **📖 Help:** `FAQ_TROUBLESHOOTING.md` → SSL Certificate Errors

### System date wrong
- Set manually: `sudo date -s "2024-01-15 14:30:00"` (use current date)
- Enable auto-sync: `sudo timedatectl set-ntp true`
- **Why?** Wrong date causes SSL errors!

### Import errors
- Make sure virtual environment is activated: `source venv/bin/activate`
- Check you're in right directory: `cd ~/raspberry/non_movement`
- Check packages: `pip list`
- Recreate venv with system packages: `python3 -m venv --system-site-packages venv`

### Discord alerts not showing
- Check `config.yaml`: `escalation.enabled: false` OR include `"webhook"` in escalation levels
- Test webhook: `python test_discord_alert.py`
- Check webhook URL is correct
- **📖 Help:** `FAQ_TROUBLESHOOTING.md` → Alert Configuration Issues

### ThingSpeak rate limit
- Free tier: 3 messages per 15 seconds
- Increase `check_interval` in config
- Batch data sends
- **📖 Help:** `FAQ_TROUBLESHOOTING.md` → ThingSpeak Integration Issues

### Permission errors
```bash
sudo usermod -a -G video $USER
# Log out and back in (or reboot)
```

### Performance issues
- Reduce camera resolution in config
- Increase check_interval
- Close other programs
- Check temperature: `vcgencmd measure_temp`

---

## ✅ Deployment Checklist

**Setup:**
- [ ] Raspberry Pi OS installed on SD card
- [ ] SSH enabled in Imager
- [ ] WiFi/Ethernet configured
- [ ] SD card inserted into Pi
- [ ] Camera module connected to CSI port
- [ ] Pi powered on and booted successfully

**Initial Configuration:**
- [ ] Found Pi's IP address
- [ ] SSH connection working
- [ ] System date/time set correctly
- [ ] NTP enabled for auto time sync
- [ ] Camera enabled in raspi-config
- [ ] System updated (`apt update && apt upgrade`)

**System Dependencies:**
- [ ] Camera libraries installed (`libcamera-apps`, `libcamera-dev`)
- [ ] Python tools installed (`python3-pip`, `python3-venv`)
- [ ] Camera tested with `rpicam-hello --list-cameras`
- [ ] Test photo taken successfully

**Code Setup:**
- [ ] Project code transferred to Pi (`~/raspberry`)
- [ ] Virtual environment created with `--system-site-packages`
- [ ] Virtual environment activated
- [ ] All Python packages installed
- [ ] SSL issues resolved (if any)

**Configuration:**
- [ ] `config.yaml` updated (`use_mock_sensors: false`)
- [ ] ThingSpeak account created and API key added
- [ ] Discord webhook created and URL added
- [ ] Alert escalation configured correctly

**Testing:**
- [ ] Non-movement project runs without errors
- [ ] Camera captures real frames
- [ ] ThingSpeak data logging working (check dashboard)
- [ ] Discord alerts triggering correctly
- [ ] Logs show no errors

**Optional:**
- [ ] Auto-start configured (systemd service)
- [ ] Fall detection project tested

---

## Next Steps

- Monitor system performance
- Adjust thresholds based on real-world data
- Improve detection algorithms
- Add features (pose estimation, etc.)

---

## Congratulations! 🎉

You've successfully built and deployed an elderly monitoring system!

---

*Your system is now running on real hardware. Monitor it closely and adjust as needed!*
