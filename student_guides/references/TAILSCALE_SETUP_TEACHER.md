# Tailscale Setup - Complete Guide for Teacher

## What You're Doing

You're setting up Tailscale on your Mac so you can access your student's Raspberry Pi remotely, even when it's on their home network or a different network.

**Time needed:** 10-15 minutes

**Where to run commands:** 
- Steps 1-2: On your Mac (GUI/App Store)
- Steps 3+: On your Mac Terminal

---

## Prerequisites

- Mac computer (macOS 12 Monterey or later)
- Internet connection
- Student has completed their Tailscale setup (see `TAILSCALE_SETUP_STUDENT.md`)
- Student has shared their Pi's Tailscale IP address with you

---

## Step 1: Download and Install Tailscale

### Method A: Mac App Store (Recommended - Easiest)

1. **Open Mac App Store**
   - Click the App Store icon in your Dock
   - Or press `Cmd + Space`, type "App Store", press Enter

2. **Search for Tailscale**
   - In the search bar, type: `Tailscale`
   - Press Enter

3. **Install Tailscale**
   - Click "Get" or "Install" button
   - Wait for installation to complete (1-2 minutes)

4. **Open Tailscale**
   - Click "Open" in App Store, or
   - Press `Cmd + Space`, type "Tailscale", press Enter
   - Or find it in Applications folder

**Expected:** Tailscale app opens and shows a welcome screen.

---

### Method B: Direct Download (Alternative)

**If App Store doesn't work:**

1. **Visit:** https://tailscale.com/download/macos
2. **Download** the Tailscale installer
3. **Open** the downloaded file
4. **Drag** Tailscale to Applications folder
5. **Open** Tailscale from Applications

---

## Step 2: Sign In to Tailscale

1. **Open Tailscale app**
   - You'll see it in your menu bar (top right, near the clock)
   - Click the Tailscale icon

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
   - Follow the prompts in your web browser
   - You may be asked to authorize Tailscale

5. **Admin Console Question (if asked)**
   - If Tailscale asks: "What VPN are you using?"
   - Answer: **"None"** or **"No other VPN"**
   - (Unless you actually have another VPN installed)

**Expected:** Tailscale icon in menu bar shows you're connected (green/active status).

---

## Step 3: Verify Your Mac is Connected

**Check Tailscale status:**

**Option A: Via Menu Bar**
- Click Tailscale icon in menu bar (top right)
- You should see your Mac listed (e.g., "ellens-mac-mini")

**Option B: Via Terminal**

**On your Mac Terminal, run:**

```bash
tailscale status
```

**Expected output:**
```
100.66.211.91  ellens-mac-mini  your-email@  macOS  active; direct ...
```

You should see:
- Your Mac's Tailscale IP address (e.g., `100.66.211.91`)
- Your Mac's name
- Status showing "active"

**Get your Mac's Tailscale IP:**

```bash
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

**On your Mac Terminal, run:**

```bash
ping -c 3 <student-tailscale-ip>
```

**Example:**
```bash
ping -c 3 100.95.13.28
```

**Expected output:**
```
PING 100.95.13.28 (100.95.13.28): 56 data bytes
64 bytes from 100.95.13.28: icmp_seq=1 ttl=64 time=15.479 ms
64 bytes from 100.95.13.28: icmp_seq=2 ttl=64 time=9.903 ms
64 bytes from 100.95.13.28: icmp_seq=3 ttl=64 time=12.456 ms

--- 100.95.13.28 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss
```

**If ping works (0% or low packet loss):** ✅ Pi is reachable! Proceed to Step 6.

**If ping fails:**
- Check if student completed Tailscale setup
- Ask student to verify: `sudo tailscale status` on their Pi
- Make sure both are signed in to same Tailscale account
- Wait a few minutes for Tailscale to fully connect

---

## Step 6: Connect to Student's Pi via SSH

**On your Mac Terminal, run:**

```bash
ssh pi@<student-tailscale-ip>
```

**Example:**
```bash
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

## Step 7: Verify It's the Right Pi

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

## Step 8: Check Tailscale Status on Both Devices

**On your Mac Terminal (new window, not SSH session), run:**

```bash
tailscale status
```

**Expected output:**
```
100.95.13.28   pi               student-email@  linux  -
100.66.211.91  ellens-mac-mini  your-email@    macOS  active; direct 172.20.83.36:41641, tx 6348 rx 7300
```

You should see:
- Student's Pi with its Tailscale IP
- Your Mac with its Tailscale IP
- Status showing "active; direct" (means direct connection, not relayed)

**"active; direct"** = Best connection type ✅

**"active; relayed"** = Still works, but slower (may need to wait or check firewall)

---

## Complete Checklist

Before connecting, make sure:

- [ ] Tailscale is installed on your Mac (check Applications or menu bar)
- [ ] You're signed in to Tailscale (menu bar shows active status)
- [ ] Your Mac has a Tailscale IP (`tailscale ip -4` shows an IP)
- [ ] Student has shared their Pi's Tailscale IP with you
- [ ] You can ping the student's Pi (`ping -c 3 <student-ip>`)
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

### "Can't find Tailscale in menu bar"
**Solution:**
- Open Tailscale from Applications folder
- Or: Press `Cmd + Space`, type "Tailscale", press Enter
- Check System Preferences → Security & Privacy → allow Tailscale
- Restart Tailscale app

### "Tailscale not found" after curl install
**Solution:**
- On macOS, the `curl` command opens App Store
- Complete installation from App Store
- Then open Tailscale app from Applications

### "Student's Pi not showing in Tailscale status"
**Check:**
- Did student complete all setup steps? (see `TAILSCALE_SETUP_STUDENT.md`)
- Are you both signed in to same Tailscale account?
- Student should run `sudo tailscale status` on Pi to verify
- Wait a few minutes for Tailscale to fully connect
- Both devices need internet connection

**Solution:**
- Verify student's Pi Tailscale IP: Ask student to run `tailscale ip -4` on Pi
- Check if you can ping it: `ping -c 3 <student-ip>`
- If ping fails, student may need to restart Tailscale on Pi: `sudo tailscale up`

### "SSH connection refused" or "Connection timed out"
**Check:**
- Is Tailscale running on both devices?
  ```bash
  # On Mac (Terminal)
  tailscale status
  ```
- Can you ping the Pi's Tailscale IP?
  ```bash
  ping -c 3 100.95.13.28
  ```
- Is SSH enabled on Pi? (Should be by default)
- Is student's Pi powered on?
- Does student's Pi have internet connection?

**Solution:**
- Verify Tailscale is running: `tailscale status` on Mac
- Ask student to verify: `sudo tailscale status` on Pi
- Test connectivity: `ping -c 3 <student-ip>`
- If ping works but SSH doesn't, SSH might be disabled on Pi
- Ask student to enable SSH: `sudo systemctl enable ssh` and `sudo systemctl start ssh`

### "Permission denied (publickey)"
**Solution:**
- This is normal for first connection
- Make sure you're using password authentication
- Try:
  ```bash
  ssh -o PreferredAuthentications=password pi@<tailscale-ip>
  ```
- Enter the Pi's password when prompted (usually `raspberry`)

### "Host key verification failed"
**Solution:**
- This happens when the Pi's host key changed (e.g., after re-imaging SD card)
- Remove old host key:
  ```bash
  ssh-keygen -R <tailscale-ip>
  ```
- Example:
  ```bash
  ssh-keygen -R 100.95.13.28
  ```
- Then try SSH again

### "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!"
**Solution:**
- Same as above - remove old host key:
  ```bash
  ssh-keygen -R <tailscale-ip>
  ```
- Or remove from known_hosts manually:
  ```bash
  ssh-keygen -R <tailscale-ip> -f ~/.ssh/known_hosts
  ```

### "Ping works but SSH times out"
**Solution:**
- SSH might be blocked by firewall
- Ask student to check: `sudo systemctl status ssh` on Pi
- Ask student to enable SSH: `sudo systemctl enable ssh && sudo systemctl start ssh`
- Check if SSH port is open: `nc -zv <student-ip> 22` (should show "succeeded")

### "Tailscale shows 'relayed' instead of 'direct'"
**Solution:**
- "Relayed" still works, but is slower
- Usually means firewall/NAT is blocking direct connection
- Wait a few minutes - Tailscale may establish direct connection
- Check firewall settings on both networks
- "Relayed" is fine for basic SSH access

### "Can't access Pi even though both devices show in Tailscale"
**Check:**
- Are both devices signed in to same Tailscale account?
- Verify student's Pi IP: Ask them to run `tailscale ip -4` again
- Check your Mac's Tailscale status: `tailscale status`
- Test ping: `ping -c 3 <student-ip>`

**Solution:**
- Make sure you're using the correct Tailscale IP (not local network IP)
- Verify both devices are on same Tailscale network
- Wait 1-2 minutes for Tailscale to fully establish connection
- Try disconnecting and reconnecting Tailscale on both devices

---

## Quick Reference Commands

```bash
# Check Tailscale status
tailscale status

# Check your Mac's Tailscale IP
tailscale ip -4

# Test connection to student's Pi
ping -c 3 <student-tailscale-ip>

# Connect to student's Pi
ssh pi@<student-tailscale-ip>

# Remove old host key (if needed)
ssh-keygen -R <student-tailscale-ip>

# Check if SSH port is open
nc -zv <student-tailscale-ip> 22
```

---

## Multiple Students?

If you have multiple students with Pis:

1. **Each student sets up Tailscale** on their Pi (see `TAILSCALE_SETUP_STUDENT.md`)
2. **Each student shares their Tailscale IP** with you
3. **You connect to each using their IP:**
   ```bash
   ssh pi@<student1-tailscale-ip>
   ssh pi@<student2-tailscale-ip>
   ssh pi@<student3-tailscale-ip>
   ```

**Or:** Create a shared Tailscale network and have all students join it.

**To manage multiple connections:**
- Keep a list of student names and their Tailscale IPs
- Use Terminal tabs or windows for each student
- Or use SSH config file for easier access (see below)

---

## Advanced: SSH Config for Easy Access

**Create an SSH config file to make connecting easier:**

**On your Mac, create/edit SSH config:**

```bash
nano ~/.ssh/config
```

**Add entries for each student:**

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

**Save and exit:** `Ctrl + X`, then `Y`, then Enter

**Now you can connect easily:**

```bash
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
│  │
│  └─ Yes → Can you SSH?
│     ├─ No → Check SSH is enabled on Pi
│     │        Check firewall settings
│     │        Try: ssh -v pi@<ip> (verbose mode)
│     │
│     └─ Yes → Success! ✅
```

---

*Once set up, you can access the student's Pi from anywhere with internet!*
