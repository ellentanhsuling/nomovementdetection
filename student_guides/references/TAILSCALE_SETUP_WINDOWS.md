# Tailscale Setup - Complete Guide for Windows

## What You're Doing

You're setting up Tailscale on your Windows laptop so you can access your student's Raspberry Pi remotely, even when it's on their home network or a different network.

**Time needed:** 10-15 minutes

**Where to run commands:** 
- Steps 1-2: On your Windows laptop (GUI/installer)
- Steps 3+: On your Windows Command Prompt or PowerShell

---

## Prerequisites

- Windows 10 or later
- Internet connection
- Student has completed their Tailscale setup (see `TAILSCALE_SETUP_STUDENT.md`)
- Student has shared their Pi's Tailscale IP address with you

---

## Step 1: Download and Install Tailscale

### Method A: Direct Download (Recommended)

1. **Visit:** https://tailscale.com/download/windows
   - Or go to: https://tailscale.com/download and click "Windows"

2. **Download Tailscale**
   - Click the download button
   - The file will be named something like `Tailscale-1.xx.x-x64.msi`
   - Save it to your Downloads folder

3. **Run the Installer**
   - Open File Explorer
   - Navigate to Downloads folder
   - Double-click the downloaded `.msi` file
   - Click "Yes" if Windows asks for permission

4. **Follow Installation Wizard**
   - Click "Next" on the welcome screen
   - Accept the license agreement
   - Choose installation location (default is fine)
   - Click "Install"
   - Wait for installation to complete (1-2 minutes)
   - Click "Finish"

**Expected:** Tailscale icon appears in your system tray (bottom right, near the clock).

---

### Method B: Microsoft Store (Alternative)

1. **Open Microsoft Store**
   - Press `Windows key`, type "Microsoft Store", press Enter
   - Or click the Microsoft Store icon in Start menu

2. **Search for Tailscale**
   - In the search bar, type: `Tailscale`
   - Press Enter

3. **Install Tailscale**
   - Click "Get" or "Install" button
   - Wait for installation to complete

4. **Launch Tailscale**
   - Click "Open" in Microsoft Store, or
   - Press `Windows key`, type "Tailscale", press Enter

---

## Step 2: Sign In to Tailscale

1. **Open Tailscale**
   - Look for Tailscale icon in system tray (bottom right)
   - Click the Tailscale icon
   - Or press `Windows key`, type "Tailscale", press Enter

2. **Click "Log in" or "Sign up"**

3. **Sign in using one of these options:**
   - **Google account** (recommended - easiest)
   - GitHub account
   - Microsoft account
   - Or create a new Tailscale account

**IMPORTANT - Account Requirements:**

**Option 1: Same Account (Easiest - Recommended)**
- If you and your student sign in with the **exact same Tailscale account** (same email address), you'll automatically see each other's devices
- This is the simplest method - just have students use the same account you use
- **Recommended for classes:** Create one shared Tailscale account (e.g., `classname@example.com`) and have all students use it

**Option 2: Different Accounts (Requires Sharing)**
- If using different accounts, you need to:
  1. Have student share their Pi device with your account in Tailscale admin console, OR
  2. Add students to your Tailscale network/organization
- This requires additional setup and is more complex
- **Not recommended** unless you have specific security requirements

**For simplicity, use the same account for all students!**

4. **Complete sign-in process**
   - A web browser will open
   - Follow the prompts to authorize Tailscale
   - You may be asked to sign in to your account

5. **Admin Console Question (if asked)**
   - If Tailscale asks: "What VPN are you using?"
   - Answer: **"None"** or **"No other VPN"**
   - (Unless you actually have another VPN installed)

**Expected:** Tailscale icon in system tray shows you're connected (green/active status).

---

## Step 3: Verify Your Windows Laptop is Connected

**Check Tailscale status:**

**Option A: Via System Tray**
- Click Tailscale icon in system tray (bottom right)
- You should see your laptop listed (e.g., "DESKTOP-ABC123")

**Option B: Via Command Prompt or PowerShell**

**Open Command Prompt or PowerShell:**
- Press `Windows key + R`
- Type: `cmd` (for Command Prompt) or `powershell` (for PowerShell)
- Press Enter

**Run this command:**

```cmd
tailscale status
```

**Expected output:**
```
100.66.211.91  DESKTOP-ABC123  your-email@  windows  active; direct ...
```

You should see:
- Your laptop's Tailscale IP address (e.g., `100.66.211.91`)
- Your laptop's name
- Status showing "active"

**Get your laptop's Tailscale IP:**

```cmd
tailscale ip -4
```

**Expected output:**
```
100.66.211.91
```

---

## Step 4: Get Student's Tailscale IP Address

**Ask your student to run this on their Pi and share the result:**

```bash
tailscale ip -4
```

**They should share something like:** `100.95.13.28`

**Write this down - you'll need it to connect!**

---

## Step 5: Verify Student's Pi is Connected

**Before connecting, verify the student's Pi is online:**

**On your Windows Command Prompt or PowerShell, run:**

```cmd
ping -n 3 <student-tailscale-ip>
```

**Example:**
```cmd
ping -n 3 100.95.13.28
```

**Expected output:**
```
Pinging 100.95.13.28 with 32 bytes of data:
Reply from 100.95.13.28: bytes=32 time=15ms TTL=64
Reply from 100.95.13.28: bytes=32 time=9ms TTL=64
Reply from 100.95.13.28: bytes=32 time=12ms TTL=64

Ping statistics for 100.95.13.28:
    Packets: Sent = 3, Received = 3, Lost = 0 (0% loss)
```

**If ping works (0% packet loss):** ✅ Pi is reachable! Proceed to Step 6.

**If ping fails:**
- Check if student completed Tailscale setup
- Ask student to verify: `sudo tailscale status` on their Pi
- Make sure both are signed in to same Tailscale account
- Wait a few minutes for Tailscale to fully connect

---

## Step 6: Install SSH Client (If Needed)

**Windows 10 (version 1809 or later) and Windows 11 have SSH built-in.**

**Check if SSH is available:**

**On Command Prompt or PowerShell, run:**

```cmd
ssh -V
```

**If you see version info (e.g., "OpenSSH_8.x"):** ✅ SSH is installed! Skip to Step 7.

**If you get "command not found" or error:**

**For Windows 10:**
1. Open **Settings** (Windows key + I)
2. Go to **Apps** → **Optional Features**
3. Click **Add a feature**
4. Search for **"OpenSSH Client"**
5. Click **Install**
6. Wait for installation
7. Restart Command Prompt/PowerShell

**For Windows 11:**
- SSH should be installed by default
- If not, follow Windows 10 steps above

**Alternative: Use PuTTY**
- Download from: https://www.putty.org/
- Install and use PuTTY instead of command-line SSH

---

## Step 7: Connect to Student's Pi via SSH

**On your Windows Command Prompt or PowerShell, run:**

```cmd
ssh pi@<student-tailscale-ip>
```

**Example:**
```cmd
ssh pi@100.95.13.28
```

**First time connection:**
- You'll see: `The authenticity of host '100.95.13.28' can't be established...`
- Type: `yes` and press Enter
- Enter the Pi's password (the one set during initial setup, usually `raspberry`)

**Success looks like:**
```
Linux pi 6.12.47+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.47-1+rpt1 (2025-09-16) aarch64

The programs included with the Debian GNU/Linux system are free software;
...

pi@pi:~ $
```

**You're now connected to the student's Pi!** ✅

---

## Step 8: Verify It's the Right Pi

**Once connected, verify you're on the correct Pi:**

**On the Pi (you should see `pi@pi:~ $`), run:**

```bash
hostname
```

**Expected output:**
```
pi
```
or
```
raspberrypi
```
or the student's custom hostname (e.g., `ming`)

**Check the Pi's network info:**

```bash
hostname -I
```

**Expected output:**
```
172.20.83.63 100.95.13.28
```

You should see:
- The Pi's local network IP (e.g., `172.20.83.63`)
- The Pi's Tailscale IP (e.g., `100.95.13.28`)

**If both IPs match what you expect:** ✅ You're on the right Pi!

---

## Step 9: Check Tailscale Status on Both Devices

**On your Windows Command Prompt or PowerShell (new window, not SSH session), run:**

```cmd
tailscale status
```

**Expected output:**
```
100.95.13.28   pi               student-email@  linux  -
100.66.211.91  DESKTOP-ABC123   your-email@     windows  active; direct 172.20.83.36:41641, tx 6348 rx 7300
```

You should see:
- Student's Pi with its Tailscale IP
- Your Windows laptop with its Tailscale IP
- Status showing "active; direct" (means direct connection, not relayed)

**"active; direct"** = Best connection type ✅

**"active; relayed"** = Still works, but slower (may need to wait or check firewall)

---

## Complete Checklist

Before connecting, make sure:

- [ ] Tailscale is installed on your Windows laptop (check system tray or Start menu)
- [ ] You're signed in to Tailscale (system tray shows active status)
- [ ] Your laptop has a Tailscale IP (`tailscale ip -4` shows an IP)
- [ ] SSH client is installed (`ssh -V` shows version)
- [ ] Student has shared their Pi's Tailscale IP with you
- [ ] You can ping the student's Pi (`ping -n 3 <student-ip>`)
- [ ] Student has verified their Pi is connected (`sudo tailscale status` on Pi)

---

## FAQ

### "Do I need to use the same account as my student?"

**Short answer:** Yes, for the easiest setup. But there are options:

**What is a Tailnet?**
- A **tailnet** is Tailscale's term for a private network of devices
- All devices signed in with the **same Tailscale account** belong to the **same tailnet**
- Devices in the same tailnet can automatically see and connect to each other
- Devices in **different tailnets** (different accounts) **cannot** see each other by default

**Option 1: Same Account / Same Tailnet (Recommended)**
- ✅ **Easiest:** Both you and student sign in with the exact same Tailscale account (same email)
- ✅ **Same tailnet:** All devices automatically belong to the same tailnet
- ✅ **Automatic:** Devices automatically see each other
- ✅ **No extra setup:** Works immediately after both devices sign in
- **Best for:** Classes where you want simple, quick setup

**Option 2: Different Accounts / Different Tailnets (More Complex)**
- ⚠️ **Different tailnets:** Devices belong to separate networks
- ⚠️ Requires sharing devices or adding users to network
- ⚠️ More setup steps needed
- ⚠️ May require Tailscale for Teams (paid) for advanced sharing
- **Best for:** When you need separate accounts for security reasons

**Recommendation:** Use the same account (same tailnet) for all students. Create a shared account like `yourclass@example.com` that everyone uses. This ensures all devices are in the same tailnet and can see each other automatically.

---

## Alternative: Sharing Devices Between Different Tailnets

**When to use this:** If you and your student are using **different Tailscale accounts** (different tailnets), you can still access their Pi by having them share the device with you.

**Note:** This is more complex than using the same account. We recommend using the same account for simplicity, but this method works if you need separate accounts.

---

### How Device Sharing Works

When a student shares their Pi device with you:
- The Pi remains in the student's tailnet
- You get access to that specific device from your tailnet
- You can connect via SSH using the Pi's Tailscale IP address
- The student controls who has access

---

### Step-by-Step: Student Shares Their Pi

**The student needs to do this on their Pi or via Tailscale admin console:**

1. **Student opens Tailscale admin console**
   - Go to: https://login.tailscale.com/admin/machines
   - Or click Tailscale icon → "Admin console"

2. **Student finds their Raspberry Pi device**
   - Look for device name (usually `pi` or `raspberrypi`)
   - Or look for the Tailscale IP address (e.g., `100.95.13.28`)

3. **Student clicks on the Pi device**
   - This opens the device details page

4. **Student clicks "Share..." or "Share device"**
   - This option appears in the device details

5. **Student invites you via email**
   - Enter your email address (the one you used for Tailscale)
   - Or generate a share link and send it to you

6. **You accept the invitation**
   - Check your email for the Tailscale invitation
   - Click the link in the email
   - Sign in to Tailscale (if not already signed in)
   - Accept the share

7. **Access the shared Pi**
   - The Pi will now appear in your Tailscale admin console
   - You can see its Tailscale IP address
   - Connect via SSH: `ssh pi@<tailscale-ip>`

---

### Important Notes

- **The Pi stays in the student's tailnet** - it's just shared with you
- **You can only access the shared device** - you won't see other devices in the student's tailnet
- **The student can revoke access** at any time from their admin console
- **This works with free Tailscale accounts** - no paid plan needed

---

### Troubleshooting Device Sharing

**Problem:** "I don't see the Share option"
- **Solution:** Make sure you're looking at the device details page, not just the device list
- **Solution:** The student must be signed in to Tailscale admin console

**Problem:** "I didn't receive the invitation email"
- **Solution:** Check spam/junk folder
- **Solution:** Verify the email address is correct
- **Solution:** Have student generate a share link instead

**Problem:** "I accepted but still can't see the device"
- **Solution:** Wait 1-2 minutes for Tailscale to sync
- **Solution:** Refresh your Tailscale admin console
- **Solution:** Check that both devices are online and connected to Tailscale

---

## Troubleshooting

### "Can't find Tailscale in system tray"
**Solution:**
- Press `Windows key`, type "Tailscale", press Enter
- Or check Start menu → All Apps → Tailscale
- Restart Tailscale: Right-click Tailscale icon → Exit, then open Tailscale again
- Check if Tailscale service is running: Open Services (services.msc), find "Tailscale", ensure it's running

### "Tailscale not found" after installation
**Solution:**
- Restart your computer
- Check if installation completed successfully
- Try reinstalling from tailscale.com/download/windows
- Check Windows Defender or antivirus isn't blocking it

### "Student's Pi not showing in Tailscale status"
**Check:**
- Did student complete all setup steps? (see `TAILSCALE_SETUP_STUDENT.md`)
- Are you both signed in to same Tailscale account?
- Student should run `sudo tailscale status` on Pi to verify
- Wait a few minutes for Tailscale to fully connect
- Both devices need internet connection

**Solution:**
- Verify student's Pi Tailscale IP: Ask student to run `tailscale ip -4` on Pi
- Check if you can ping it: `ping -n 3 <student-ip>`
- If ping fails, student may need to restart Tailscale on Pi: `sudo tailscale up`

### "SSH command not found" or "'ssh' is not recognized"
**Solution:**
- Install OpenSSH Client (see Step 6)
- Or use PuTTY as alternative:
  - Download from: https://www.putty.org/
  - Open PuTTY
  - Enter: `pi@<student-tailscale-ip>` as hostname
  - Click "Open"
  - Enter password when prompted

### "SSH connection refused" or "Connection timed out"
**Check:**
- Is Tailscale running on both devices?
  ```cmd
  tailscale status
  ```
- Can you ping the Pi's Tailscale IP?
  ```cmd
  ping -n 3 100.95.13.28
  ```
- Is SSH enabled on Pi? (Should be by default)
- Is student's Pi powered on?
- Does student's Pi have internet connection?

**Solution:**
- Verify Tailscale is running: `tailscale status` on Windows
- Ask student to verify: `sudo tailscale status` on Pi
- Test connectivity: `ping -n 3 <student-ip>`
- If ping works but SSH doesn't, SSH might be disabled on Pi
- Ask student to enable SSH: `sudo systemctl enable ssh` and `sudo systemctl start ssh`

### "Permission denied (publickey)"
**Solution:**
- This is normal for first connection
- Make sure you're using password authentication
- Enter the Pi's password when prompted (usually `raspberry`)
- If using PuTTY, make sure "Keyboard-interactive" authentication is enabled

### "Host key verification failed"
**Solution:**
- This happens when the Pi's host key changed (e.g., after re-imaging SD card)
- Remove old host key:
  ```cmd
  ssh-keygen -R <tailscale-ip>
  ```
- Example:
  ```cmd
  ssh-keygen -R 100.95.13.28
  ```
- Then try SSH again

### "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!"
**Solution:**
- Same as above - remove old host key:
  ```cmd
  ssh-keygen -R <tailscale-ip>
  ```
- Or edit `C:\Users\<YourUsername>\.ssh\known_hosts` manually and remove the line with the IP

### "Ping works but SSH times out"
**Solution:**
- SSH might be blocked by Windows Firewall
- Check Windows Firewall settings
- Ask student to check: `sudo systemctl status ssh` on Pi
- Ask student to enable SSH: `sudo systemctl enable ssh && sudo systemctl start ssh`
- Check if SSH port is open: `telnet <student-ip> 22` (if telnet is enabled)

### "Tailscale shows 'relayed' instead of 'direct'"
**Solution:**
- "Relayed" still works, but is slower
- Usually means firewall/NAT is blocking direct connection
- Wait a few minutes - Tailscale may establish direct connection
- Check Windows Firewall settings
- Check if antivirus is blocking Tailscale
- "Relayed" is fine for basic SSH access

### "Can't access Pi even though both devices show in Tailscale"
**Check:**
- Are both devices signed in to same Tailscale account?
- Verify student's Pi IP: Ask them to run `tailscale ip -4` again
- Check your Windows laptop's Tailscale status: `tailscale status`
- Test ping: `ping -n 3 <student-ip>`

**Solution:**
- Make sure you're using the correct Tailscale IP (not local network IP)
- Verify both devices are on same Tailscale network
- Wait 1-2 minutes for Tailscale to fully establish connection
- Try disconnecting and reconnecting Tailscale on both devices
- Check Windows Firewall isn't blocking Tailscale

### "Windows Firewall blocking connection"
**Solution:**
- Open Windows Defender Firewall
- Click "Allow an app or feature through Windows Defender Firewall"
- Find "Tailscale" in the list
- Make sure both "Private" and "Public" are checked
- If Tailscale isn't listed, click "Allow another app" and add Tailscale

---

## Quick Reference Commands

**Open Command Prompt:**
- Press `Windows key + R`, type `cmd`, press Enter

**Open PowerShell:**
- Press `Windows key + R`, type `powershell`, press Enter
- Or: Right-click Start button → Windows PowerShell

```cmd
REM Check Tailscale status
tailscale status

REM Check your Windows laptop's Tailscale IP
tailscale ip -4

REM Test connection to student's Pi
ping -n 3 <student-tailscale-ip>

REM Connect to student's Pi
ssh pi@<student-tailscale-ip>

REM Remove old host key (if needed)
ssh-keygen -R <student-tailscale-ip>

REM Check SSH version
ssh -V
```

---

## Using PuTTY (Alternative SSH Client)

**If you prefer a GUI SSH client:**

1. **Download PuTTY:**
   - Visit: https://www.putty.org/
   - Download the Windows installer
   - Install PuTTY

2. **Open PuTTY**

3. **Enter connection details:**
   - **Host Name (or IP address):** `<student-tailscale-ip>`
     - Example: `100.95.13.28`
   - **Port:** `22`
   - **Connection type:** `SSH` (should be selected by default)

4. **Click "Open"**

5. **First time connection:**
   - You'll see a security alert - click "Yes"

6. **Login:**
   - **Login as:** `pi`
   - **Password:** Enter the Pi's password (usually `raspberry`)

7. **You're connected!** ✅

---

## Multiple Students?

If you have multiple students with Pis:

1. **Each student sets up Tailscale** on their Pi (see `TAILSCALE_SETUP_STUDENT.md`)
2. **Each student shares their Tailscale IP** with you
3. **You connect to each using their IP:**
   ```cmd
   ssh pi@<student1-tailscale-ip>
   ssh pi@<student2-tailscale-ip>
   ssh pi@<student3-tailscale-ip>
   ```

**Or:** Create a shared Tailscale network and have all students join it.

**To manage multiple connections:**
- Use multiple Command Prompt/PowerShell windows (one per student)
- Or use PuTTY and save sessions for each student
- Or use Windows Terminal with multiple tabs

---

## Advanced: SSH Config for Easy Access

**Create an SSH config file to make connecting easier:**

**On Windows, create/edit SSH config:**

1. **Open File Explorer**
2. **Navigate to:** `C:\Users\<YourUsername>\.ssh\`
   - If `.ssh` folder doesn't exist, create it
3. **Create a file named:** `config` (no extension)
4. **Open with Notepad** and add:

```
Host student1-pi
    HostName 100.95.13.28
    User pi
    Port 22

Host student2-pi
    HostName 100.64.1.2
    User pi
    Port 22
```

5. **Save the file**

**Now you can connect easily:**

```cmd
ssh student1-pi
ssh student2-pi
```

---

## Security Notes

- ✅ Tailscale uses encrypted connections (WireGuard protocol)
- ✅ Only devices on same Tailscale network can access
- ✅ No router configuration needed
- ✅ No open ports on your network
- ✅ Safe for student projects
- ✅ Free for personal use (up to 100 devices)

**Best practices:**
- Use strong passwords on Pis
- Don't share Tailscale IPs publicly
- Only add trusted devices to Tailscale network
- Regularly update Tailscale on all devices
- Keep Windows Firewall enabled
- Keep Windows and Tailscale updated

---

## What Students Need to Know

**Share with students:**
- They need to complete `TAILSCALE_SETUP_STUDENT.md` guide
- They need to share their Tailscale IP with you
- They need to keep their Pi powered on and connected to internet
- They need to keep Tailscale running on their Pi

---

## Next Steps After Connecting

Once you can SSH to the student's Pi:

1. **Verify it's the right Pi:**
   ```bash
   hostname
   ```

2. **Check network info:**
   ```bash
   hostname -I
   ```

3. **Continue with project setup** (see other student guides)
   - Deploy code to Pi
   - Set up environment
   - Run applications
   - Troubleshoot issues

---

## Quick Troubleshooting Flowchart

```
Can't connect to student's Pi?
│
├─ Can you ping the Tailscale IP?
│  ├─ No → Check Tailscale status on both devices
│  │        Verify student completed setup
│  │        Wait a few minutes
│  │        Check Windows Firewall
│  │
│  └─ Yes → Can you SSH?
│     ├─ No → Check SSH is installed (ssh -V)
│     │        Check SSH is enabled on Pi
│     │        Check firewall settings
│     │        Try: ssh -v pi@<ip> (verbose mode)
│     │
│     └─ Yes → Success! ✅
```

---

*Once set up, you can access the student's Pi from anywhere with internet!*
