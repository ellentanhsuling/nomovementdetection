# Raspberry Pi 5 Setup - Step by Step Guide

## ⚠️ Important: Read This First

This guide goes **step by step** with verification at each stage. **Do not skip ahead**. Complete each step and verify it works before moving to the next.

**Official Documentation:**
- Raspberry Pi Getting Started: https://www.raspberrypi.com/documentation/computers/getting-started.html
- Raspberry Pi 5 Specific: https://www.raspberrypi.com/documentation/computers/raspberry-pi-5.html

---

## What You Have

✅ Raspberry Pi 5  
✅ Camera Module  
✅ Pi HAT (already mounted)  
✅ USB (power supply)  
✅ SD Card  
✅ Camera module (not plugged in yet)

**⚠️ Setup Method:** SSH only - no HDMI/monitor needed!

---

## Step 1: Verify Your Hardware

### 1.1 Check Raspberry Pi 5

**What to look for:**
- Board should say "Raspberry Pi 5"
- Check for any visible damage
- Pi HAT should be securely mounted

**✅ Verification:** Pi 5 board looks good, no damage visible

**Status:** [ ] Complete

---

### 1.2 Check Camera Module

**What to look for:**
- Camera Module 3 (check label)
- Ribbon cable attached to camera
- No damage to cable or camera

**✅ Verification:** Camera module and cable look good

**Status:** [ ] Complete

---

### 1.3 Check SD Card

**What to check:**
- Size (should be at least 32GB, 64GB recommended)
- Format (should be empty or need formatting)
- Insert into computer to check

**✅ Verification:** SD card is [ ] 32GB [ ] 64GB [ ] Other: _____

**Status:** [ ] Complete

---

### 1.4 Check Power Supply

**What to check:**
- USB-C connector (Pi 5 uses USB-C)
- Power rating: Should be **5V/5A (27W minimum)**
- Official Pi 5 power supply recommended

**⚠️ Important:** Pi 5 needs more power than Pi 4. Check your USB adapter:
- Look for "5V/5A" or "27W" on the label
- Official Pi 5 power supply: https://www.raspberrypi.com/products/raspberry-pi-5-power-supply/

**✅ Verification:** Power supply is [ ] Official Pi 5 supply [ ] 5V/5A rated [ ] Other: _____

**Status:** [ ] Complete

---

## Step 2: Prepare SD Card with Raspberry Pi OS

### 2.1 Download Raspberry Pi Imager

**Official tool:** https://www.raspberrypi.com/software/

**Steps:**
1. Go to the link above
2. Download Raspberry Pi Imager for your computer (Mac/Windows/Linux)
3. Install it

**✅ Verification:** Raspberry Pi Imager is installed

**Status:** [ ] Complete

---

### 2.2 Insert SD Card into Computer

**Steps:**
1. **Check your SD card reader type:**
   - **Most common**: Gold contacts (teeth) face **DOWN** when inserting
   - **Some readers**: Gold contacts face **UP** (less common)
   - **How to tell**: Look at the reader slot - you should see metal pins inside
   - **Rule**: Contacts on card must touch pins in reader

2. **Insert SD card:**
   - Insert card into reader slot
   - Push gently until it clicks or stops
   - **Don't force it** - if it doesn't go in, flip it over

3. **Insert reader into computer:**
   - Plug USB card reader into computer USB port
   - Wait for computer to recognize it
   - You should see SD card appear

**Mac-specific:**
- Check **Finder** sidebar - card should appear under "Devices"
- Or open **Disk Utility** - card should appear in left sidebar
- Or run in Terminal: `diskutil list` - shows all connected disks

**⚠️ Note:** If computer doesn't recognize SD card, try:
- Flip the card over (wrong orientation)
- Different USB port
- Different card reader
- Check if card is locked (small switch on side of SD card)
- Eject and re-insert card
- **📖 Mac Help:** See `SD_CARD_MAC_TROUBLESHOOTING.md` for detailed Mac troubleshooting

**✅ Verification:** 
- [ ] SD card appears on computer (Finder, Disk Utility, or Imager)
- [ ] Card may show as "Untitled" or "NO NAME" - this is normal!
- [ ] Can see files/folders on card (or empty if new)
- **OR** card appears in Raspberry Pi Imager (that's what matters!)

**Note:** "Untitled" or "NO NAME" is perfectly normal - card doesn't have a name yet. This is fine!

**Status:** [ ] Complete

---

### 2.3 Write Raspberry Pi OS to SD Card

**⚠️ About Previously Used SD Cards:**
- **You DON'T need to manually format** - Raspberry Pi Imager will automatically erase and format the card
- If your SD card was used for another project, that's fine - Imager will wipe it clean
- The card can have any files on it - Imager will handle everything

**Steps:**
1. Open Raspberry Pi Imager
2. Click "Choose OS"
3. Select **"Raspberry Pi OS (64-bit)"** (recommended for Pi 5)
4. Click "Choose Storage"
5. Select your SD card:
   - **Select the main card entry** (showing full size, e.g., "32 GB" or "64 GB")
   - **If you see "exclude system files" option**: Leave it **UNCHECKED** (you want full access)
   - **Select the card itself**, not individual partitions
   - Card may show as "Untitled" or with a name - that's fine
   - **📖 Help:** See `IMAGER_SD_CARD_SELECTION.md` for detailed selection guide
6. Click the gear icon (⚙️) for advanced options:
   - **⚠️ CRITICAL: Enable SSH** - **MUST CHECK THIS BOX!** (we're using SSH only)
   - **Set username and password**: 
     - Username: `pi` (or choose your own)
     - Password: Choose a strong password (**WRITE IT DOWN!** - you'll need it for SSH)
   - **Raspberry Pi Connect**: (Optional - for remote access)
     - If enabled, you'll need a **token** from your Raspberry Pi Connect account
     - **To find token**: Sign in at connect.raspberrypi.com → Account Settings → Look for "Connect Token"
     - **Or skip it**: Uncheck Connect, use SSH instead (both work!)
     - **📖 Help:** See `RASPBERRY_PI_CONNECT_TOKEN.md` for detailed instructions
   - **Configure wireless LAN**: (Choose one)
     - **Option A: WiFi** - If you know WiFi details, enter SSID (network name) and password
     - **Option B: Ethernet** - Leave WiFi unchecked, use Ethernet cable instead
     - **You can change WiFi later** - it's not permanent!
   - **Set locale settings**: Choose your timezone
   
   **📖 WiFi Help:** See `WIFI_CONFIGURATION_GUIDE.md` for detailed WiFi options
7. Click "Save"
8. Click "Write"
9. **Warning message will appear**: "All existing data on [SD card] will be erased"
   - This is normal and expected
   - Click "Yes" to continue
10. Wait for writing to complete (5-10 minutes)
    - Progress bar will show status
    - Don't close Imager during this time
    - Keep computer plugged in

**⚠️ Important:** 
- **This will erase everything on the SD card** - make sure you don't need anything on it
- Keep computer plugged in during writing
- Don't remove SD card during writing
- Don't close Raspberry Pi Imager during writing

**Official Guide:** https://www.raspberrypi.com/documentation/computers/getting-started.html#using-raspberry-pi-imager

**✅ Verification:** 
- [ ] OS written successfully
- [ ] "Write Successful" message shown
- [ ] SD card ejected automatically

**Status:** [ ] Complete

---

### 2.4 Verify SD Card Contents (Optional)

**Steps:**
1. Re-insert SD card if needed
2. Open SD card on computer
3. You should see files like:
   - `boot/` folder
   - Various `.txt` and `.dat` files
   - `ssh` file (if SSH enabled)

**✅ Verification:** SD card has boot files

**Status:** [ ] Complete

---

## Step 3: Connect Hardware (First Time)

### 3.1 Insert SD Card into Pi

**Steps:**
1. **Power off Pi** (if it's on, unplug power)
2. Locate SD card slot on Pi 5 (under the board, push-push mechanism)
3. Insert SD card (gold contacts facing down, towards Pi board)
4. Push until it clicks/locks

**⚠️ Important:** 
- Pi must be OFF when inserting SD card
- SD card goes in only one way

**✅ Verification:** SD card is inserted and locked in place

**Status:** [ ] Complete

---

### 3.2 Connect Camera Module

**⚠️ STOP: Do this carefully!**

**Steps:**
1. Locate **CSI connector** on Pi 5:
   - Small connector near GPIO pins
   - Has a small plastic latch
   - Usually labeled or near the edge

2. **Prepare ribbon cable:**
   - Cable should be attached to camera module
   - Connector end should be clean
   - Check orientation (connector has a specific side)

3. **Connect cable:**
   - **Gently lift the latch** on CSI connector (don't force it)
   - Insert ribbon cable:
     - Connector should face **away from Ethernet port**
     - Push cable in **gently but firmly**
     - Should go in about 1-2mm
   - **Push latch down** to lock it in place

4. **Verify connection:**
   - Cable should be straight
   - No visible gaps
   - Latch is down and locked

**⚠️ Important:**
- Be gentle with the latch (it's fragile)
- Don't force the cable
- If it doesn't go in, check orientation
- Official guide: https://www.raspberrypi.com/documentation/computers/camera_software.html#physical-connection

**✅ Verification:** 
- [ ] Camera cable connected
- [ ] Latch is down and locked
- [ ] Cable looks secure

**Status:** [ ] Complete

---

### 3.3 Connect Network (Required for SSH)

**⚠️ IMPORTANT: We're using SSH only - no HDMI needed!**

**Steps:**
1. **Choose network connection:**
   - **Option A: Ethernet** (easiest, most reliable)
     - Connect Ethernet cable from Pi to router
   - **Option B: WiFi** (if configured in Imager)
     - WiFi should connect automatically on boot
     - Make sure WiFi details were set in Imager advanced options

2. **Verify network:**
   - We'll check connection after boot
   - Need to find Pi's IP address to SSH in

**✅ Verification:** 
- [ ] Ethernet cable connected (if using Ethernet)
- [ ] OR WiFi configured in Imager (if using WiFi)
- [ ] Router is on and working

**Status:** [ ] Complete

---

## Step 4: First Boot

### 4.1 Connect Power

**Steps:**
1. **Double-check:**
   - SD card inserted
   - Camera connected (if doing now)
   - Peripherals connected (if using)
   - Network connected (if using SSH)

2. **Connect power supply:**
   - Plug USB-C into Pi 5
   - Plug power adapter into wall
   - **Red LED should light up** on Pi

**⚠️ Important:**
- Use official Pi 5 power supply or 5V/5A rated supply
- Don't use phone charger (usually not enough power)
- Red LED = power is on
- Green LED = SD card activity
- **No monitor needed** - we're using SSH only!

**✅ Verification:**
- [ ] Red LED is on (power connected)
- [ ] Green LED flashes (SD card activity - Pi is booting)
- [ ] Network cable connected (if using Ethernet)

**Status:** [ ] Complete

---

### 4.2 Wait for Boot

**Steps:**
1. Wait 30-60 seconds for first boot
2. Green LED should flash during boot (this means Pi is working)
3. **No monitor needed** - we'll verify via SSH

**⚠️ How to know if boot succeeded:**
- Green LED flashes during boot, then steady or occasional flashes
- Red LED stays on (power)
- After 30-60 seconds, Pi should be ready for SSH

**⚠️ If boot fails:**
- Check SD card is properly inserted
- Check power supply is adequate
- Check green LED - if it doesn't flash at all, there's a problem
- Try re-writing OS to SD card
- Check official troubleshooting: https://www.raspberrypi.com/documentation/computers/troubleshooting.html

**✅ Verification:** 
- [ ] Green LED flashes during boot
- [ ] Red LED stays on
- [ ] Waited 30-60 seconds for boot to complete

**Status:** [ ] Complete

---

## Step 5: Initial Configuration

### 5.1 First Login via SSH

**⚠️ We're using SSH only - no desktop needed!**

**Steps:**
1. **First, find Pi's IP address** (see next step 5.2)
2. **Once you have IP address, SSH in:**
   ```bash
   ssh pi@<ip-address>
   ```
   - Replace `<ip-address>` with actual IP (e.g., `ssh pi@192.168.1.100`)
3. **First time connection:**
   - You'll see: "The authenticity of host... Are you sure you want to continue?"
   - Type: `yes` and press Enter
4. **Enter password:**
   - Password is what you set in Imager advanced options
   - Type password (won't show on screen - this is normal)
   - Press Enter

**✅ Verification:** 
- [ ] Successfully connected via SSH
- [ ] See command prompt: `pi@raspberrypi:~ $`
- [ ] Can type commands

**Status:** [ ] Complete

---

### 5.2 Find IP Address (Required for SSH)

**⚠️ You need the Pi's IP address to SSH in!**

**Option 1: Check Router (Easiest)**
1. Log into router admin page (usually http://192.168.1.1 or http://192.168.0.1)
2. Look for "Connected Devices" or "DHCP Clients"
3. Find "Raspberry Pi" or "raspberrypi" in the list
4. Note the IP address (e.g., 192.168.1.100)

**Option 2: Use Network Scanner App**
- **Mac/Windows:** Use app like "Fing" (mobile app) or "Angry IP Scanner" (desktop)
- **Mac:** Can use built-in Network Utility
- Scan your network (usually 192.168.1.x or 192.168.0.x)
- Look for device named "raspberrypi" or "Raspberry Pi"

**Option 3: Use Raspberry Pi Imager (If Using Raspberry Pi Connect)**
- If you enabled Raspberry Pi Connect in Imager
- You can connect via: `ssh pi@raspberrypi.local`
- Or check your Raspberry Pi Connect dashboard online

**Option 4: Use mDNS (If Available)**
- Try: `ssh pi@raspberrypi.local`
- This works if your network supports mDNS/Bonjour
- May not work on all networks

**✅ Verification:** 
- [ ] IP address found: _______________
- [ ] Can ping Pi: `ping <ip-address>` (should get responses)

**Status:** [ ] Complete

---

### 5.3 Run Initial Setup (raspi-config)

**⚠️ Make sure you're SSH'd into the Pi!**

**Steps:**
1. **You should already be SSH'd in** (from step 5.1)
2. Run: `sudo raspi-config`
3. Navigate with arrow keys, Enter to select

**Configure these:**
1. **Change Password** (System Options → Password)
   - Recommended: Change from default password
2. **Enable Camera** (Interface Options → Camera → Enable)
   - **IMPORTANT:** Must enable camera for your project!
3. **Expand Filesystem** (Advanced Options → Expand Filesystem)
   - Uses full SD card space
4. **Set Locale** (Localisation Options → Locale)
   - Choose your language/region
5. **Set Timezone** (Localisation Options → Timezone)
   - Choose your timezone
6. **Set Keyboard** (Localisation Options → Keyboard)
   - Choose your keyboard layout (if needed)

**Navigate:**
- Arrow keys: Move up/down
- Tab: Move between sections
- Enter: Select/Confirm
- Esc: Go back

**✅ Verification:**
- [ ] Password changed (if desired)
- [ ] Camera enabled (CRITICAL!)
- [ ] Filesystem expanded
- [ ] Locale/timezone set

**Status:** [ ] Complete

---

### 5.4 Reboot

**Steps:**
1. In raspi-config, select "Finish"
2. Choose "Yes" to reboot
3. Wait for reboot to complete

**Or manually:**
```bash
sudo reboot
```

**✅ Verification:** Pi reboots successfully

**Status:** [ ] Complete

---

## Step 6: Verify Camera Works

### 6.1 Test Camera Detection

**Steps:**
1. SSH in or open terminal
2. Run: `vcgencmd get_camera`
3. Should show: `supported=1 detected=1`

**If shows `detected=0`:**
- Camera not detected
- Check cable connection
- Try reconnecting camera
- Check camera enabled in raspi-config

**Official guide:** https://www.raspberrypi.com/documentation/computers/camera_software.html#verify-your-camera

**✅ Verification:** Camera detected (`supported=1 detected=1`)

**Status:** [ ] Complete

---

### 6.2 Test Camera with libcamera

**Steps:**
1. Run: `libcamera-hello --list-cameras`
2. Should list your camera

**If error:**
- Install: `sudo apt install -y libcamera-apps`
- Try again

**✅ Verification:** Camera listed

**Status:** [ ] Complete

---

### 6.3 Take Test Photo

**Steps:**
1. Run: `libcamera-jpeg -o test.jpg`
2. Wait a few seconds
3. Check if file created: `ls -l test.jpg`
4. **To view photo (since no monitor):**
   - **Option A:** Transfer to your computer via SCP:
     ```bash
     # From your computer (not Pi):
     scp pi@<pi-ip>:/home/pi/test.jpg ~/Desktop/
     ```
   - **Option B:** Check file exists and size:
     ```bash
     ls -lh test.jpg  # Should show file size > 0
     ```

**✅ Verification:** 
- [ ] Photo taken successfully
- [ ] File exists: `test.jpg`
- [ ] File has size > 0 (check with `ls -lh test.jpg`)

**Status:** [ ] Complete

---

## Step 7: Install System Dependencies

### 7.1 Update System

**Steps:**
1. Run: `sudo apt update`
2. Wait for update to complete
3. Run: `sudo apt upgrade -y`
4. Wait for upgrade (may take 10-20 minutes)

**⚠️ Important:** Keep Pi connected to power and network during update

**✅ Verification:** System updated successfully

**Status:** [ ] Complete

---

### 7.2 Install Camera Libraries

**Steps:**
1. Run: `sudo apt install -y libcamera-dev python3-libcamera`
2. Wait for installation

**✅ Verification:** Libraries installed

**Status:** [ ] Complete

---

### 7.3 Install Python Development Tools

**Steps:**
1. Run: `sudo apt install -y python3-pip python3-venv git`
2. Wait for installation

**✅ Verification:** Tools installed

**Status:** [ ] Complete

---

### 7.4 Verify Installations

**Steps:**
1. Check Python: `python3 --version` (should show 3.x)
2. Check pip: `pip3 --version`
3. Check git: `git --version`

**✅ Verification:** All tools installed and working

**Status:** [ ] Complete

---

## Step 8: Transfer Your Project Code

### 8.1 Choose Transfer Method

**Option A: Using Git (Recommended)**
- If code is in Git repository
- Clone to Pi

**Option B: Using SCP (from your computer)**
- Copy files over network

**Option C: Using USB Drive**
- Copy files to USB
- Plug into Pi
- Copy to Pi

**Which method are you using?** [ ] Git [ ] SCP [ ] USB

---

### 8.2 Transfer Code

**If using Git:**
```bash
cd ~
git clone <your-repo-url>
cd raspberry
```

**If using SCP (from your computer):**
```bash
scp -r raspberry pi@<pi-ip>:/home/pi/
```

**If using USB:**
1. Plug USB into Pi
2. Mount USB (usually auto-mounted)
3. Copy files: `cp -r /media/pi/USBNAME/raspberry ~/`
4. `cd ~/raspberry`

**✅ Verification:** Code is in `~/raspberry` directory

**Status:** [ ] Complete

---

## Step 9: Set Up Python Environment

### 9.1 Create Virtual Environment

**Steps:**
1. Navigate to project: `cd ~/raspberry`
2. Create venv: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. You should see `(venv)` in prompt

**✅ Verification:** Virtual environment created and activated

**Status:** [ ] Complete

---

### 9.2 Install Python Packages

**Steps:**
1. Upgrade pip: `pip install --upgrade pip`
2. Install packages:
```bash
pip install pyyaml python-dotenv requests numpy opencv-python Pillow python-dateutil
```
3. Wait for installation (may take 5-10 minutes)

**⚠️ Note:** Some packages take time to compile on Pi

**✅ Verification:** Packages installed (check with `pip list`)

**Status:** [ ] Complete

---

### 9.3 Install Pi-Specific Packages

**Steps:**
1. Install picamera2: `pip install picamera2`
2. Wait for installation

**✅ Verification:** picamera2 installed

**Status:** [ ] Complete

---

## Step 10: Test Your Project

### 10.1 Test with Mock Sensors First

**Steps:**
1. Navigate to non_movement: `cd ~/raspberry/non_movement`
2. Edit config: `nano config.yaml`
3. Make sure: `use_mock_sensors: true`
4. Save and exit (Ctrl+X, Y, Enter)
5. Run: `python main.py --mock`
6. Should start without errors

**✅ Verification:** Project runs with mock sensors

**Status:** [ ] Complete

---

### 10.2 Test with Real Camera

**Steps:**
1. Edit config: `nano config.yaml`
2. Change: `use_mock_sensors: false`
3. Save and exit
4. Run: `python main.py`
5. Should detect real camera

**✅ Verification:** Project runs with real camera

**Status:** [ ] Complete

---

## Troubleshooting Common Issues

### Camera Not Detected
- Check cable connection
- Run: `vcgencmd get_camera`
- Enable camera in raspi-config
- Reboot

### Import Errors
- Make sure venv is activated
- Check packages installed: `pip list`
- Reinstall packages if needed

### Permission Errors
- Add user to video group: `sudo usermod -a -G video $USER`
- Log out and back in

### Performance Issues
- Reduce camera resolution in config
- Close other programs
- Check temperature: `vcgencmd measure_temp`

---

## Next Steps

Once everything is working:
1. Configure alerts (email/SMS)
2. Adjust detection thresholds
3. Set up auto-start (optional)
4. Monitor and test

---

## Progress Checklist

- [ ] Step 1: Hardware verified
- [ ] Step 2: SD card prepared
- [ ] Step 3: Hardware connected
- [ ] Step 4: First boot successful
- [ ] Step 5: Initial configuration done
- [ ] Step 6: Camera verified working
- [ ] Step 7: System dependencies installed
- [ ] Step 8: Code transferred
- [ ] Step 9: Python environment set up
- [ ] Step 10: Project tested

---

**Remember:** Complete each step and verify before moving on. Don't rush!
