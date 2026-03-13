# Tailscale Setup - Complete Step-by-Step Guide for Students

## What You're Doing

You're setting up Tailscale so your teacher can access your Raspberry Pi remotely, even when it's on your home network or a different network.

**Time needed:** 10-15 minutes (including troubleshooting)

**Where to run commands:** All commands in this guide are run **on your Raspberry Pi**, either:
- Via SSH (if you're connected remotely)
- Directly on the Pi (if you have keyboard/monitor connected)

Your prompt should look like: `pi@pi:~ $` or `pi@raspberrypi:~ $`

---

## Prerequisites

- Raspberry Pi is powered on
- You have SSH access to the Pi (or keyboard/monitor)
- You know the Pi's password (default is usually `raspberry`)
- Pi is connected to WiFi or Ethernet

---

## Step 1: Connect to Your Pi

### Option A: If You're Already Connected via SSH

You should see a prompt like:
```
pi@pi:~ $
```

**You're ready!** Skip to Step 2.

### Option B: If You Need to Connect via SSH

**On your computer (Mac/Windows/Linux), open Terminal and run:**

```bash
ssh pi@<pi-ip-address>
```

Replace `<pi-ip-address>` with your Pi's IP address (e.g., `172.20.83.63`).

**If you don't know the IP address:**
- Check your router's admin page
- Use `ping raspberrypi.local` (if on same network)
- Check the Pi's screen if you have a monitor connected

---

## Step 2: Check Your Current Location

**On your Pi (you should see `pi@pi:~ $`), run:**

```bash
pwd
```

**Expected output:**
```
/home/pi
```

This confirms you're in the Pi's home directory. **All commands from now on are run here unless specified otherwise.**

---

## Step 3: Check Internet Connection

**On your Pi (`pi@pi:~ $`), test internet connectivity:**

```bash
ping -c 3 google.com
```

**Expected output (if working):**
```
PING google.com (142.250.191.14): 56 data bytes
64 bytes from 142.250.191.14: icmp_seq=0 ttl=118 time=15.234 ms
64 bytes from 142.250.191.14: icmp_seq=1 ttl=118 time=14.567 ms
64 bytes from 142.250.191.14: icmp_seq=2 ttl=118 time=16.123 ms

--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss
```

**If you see responses (0% packet loss or low packet loss):** ✅ Internet is working! Skip to Step 4.

**If you see 100% packet loss:** Continue to troubleshooting below.

---

### Troubleshooting: No Internet Connection

**Step 3a: Check if Pi can reach the gateway/router**

**On your Pi (`pi@pi:~ $`), run:**

```bash
ip route show
```

**Expected output:**
```
default via 172.20.80.1 dev wlan0 proto dhcp src 172.20.83.63 metric 600
172.20.80.0/21 dev wlan0 proto kernel scope link src 172.20.83.63 metric 600
```

The IP after "default via" is your gateway/router (e.g., `172.20.80.1`).

**Test if you can reach the gateway:**

```bash
ping -c 3 172.20.80.1
```

(Replace `172.20.80.1` with your actual gateway IP from the `ip route show` output)

**If gateway ping works (0% packet loss):**
- Your local network is working
- The issue is internet access beyond the router
- You can still proceed with Tailscale installation (see Step 4b for manual method)

**If gateway ping fails:**
- Check your WiFi/Ethernet connection
- Verify Pi is connected to the network
- Check router settings

**Step 3b: Test direct IP connectivity (bypass DNS)**

**On your Pi (`pi@pi:~ $`), run:**

```bash
ping -c 3 8.8.8.8
```

(8.8.8.8 is Google's DNS server - this tests internet without DNS)

**If this works:** Internet is fine, DNS might be the issue. You can proceed.

**If this fails:** Internet access is blocked. You'll need to use the manual installation method (Step 4b).

---

## Step 4: Install Tailscale

### Method A: Direct Installation (If Internet Works)

**On your Pi (`pi@pi:~ $`), run:**

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

**What you'll see:**
- May ask for your password (for sudo) - enter your Pi password
- Downloads and installs Tailscale
- Installation takes 1-2 minutes

**Expected output:**
```
Installing Tailscale for debian trixie, using method apt
...
Installation complete! Log in to start using Tailscale by running:

tailscale up
```

**If you see "Installation complete!":** ✅ Skip to Step 5.

**If you get an SSL certificate error:** See troubleshooting below, then use Method B.

---

### Troubleshooting: SSL Certificate Errors

**Error message you might see:**
```
curl: (60) SSL certificate problem: certificate has expired
```
or
```
curl: (60) SSL certificate problem: certificate is not yet valid
```

**This means your Pi's system date is wrong!**

**Step 4a: Check the current date**

**On your Pi (`pi@pi:~ $`), run:**

```bash
date
```

**Expected output should show the current date/time:**
```
Wed Feb 19 14:30:00 UTC 2025
```

**If the date is wrong (e.g., shows 2020 or 2030):**

**Step 4b: Set the correct date**

**On your Pi (`pi@pi:~ $`), run:**

```bash
sudo date -s "2025-02-19 14:30:00"
```

(Replace with the actual current date and time)

**Step 4c: Enable automatic time sync**

**On your Pi (`pi@pi:~ $`), run:**

```bash
sudo timedatectl set-ntp true
```

**Step 4d: Verify the date is correct**

```bash
date
```

**Step 4e: Retry Tailscale installation**

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

---

### Method B: Manual Installation (If Direct Installation Fails)

**If the direct installation doesn't work, download the installer on your computer and transfer it to the Pi:**

**Step 4b1: On your computer (Mac/Windows/Linux), download the installer:**

**On Mac/Linux Terminal:**
```bash
cd ~/Downloads
curl -fsSL https://tailscale.com/install.sh -o tailscale_install.sh
```

**On Windows (PowerShell):**
```powershell
cd $env:USERPROFILE\Downloads
curl.exe -fsSL https://tailscale.com/install.sh -o tailscale_install.sh
```

**Step 4b2: Transfer the installer to your Pi via SCP:**

**On your computer Terminal (replace `<pi-ip>` with your Pi's IP):**

```bash
scp ~/Downloads/tailscale_install.sh pi@<pi-ip>:~/
```

**Example:**
```bash
scp ~/Downloads/tailscale_install.sh pi@172.20.83.63:~/
```

You'll be asked for the Pi's password.

**Step 4b3: On your Pi (`pi@pi:~ $`), make the installer executable and run it:**

```bash
chmod +x ~/tailscale_install.sh
sudo ~/tailscale_install.sh
```

**Expected output:**
```
Installing Tailscale for debian trixie, using method apt
...
Installation complete! Log in to start using Tailscale by running:

tailscale up
```

**If you still get SSL certificate errors:** Fix the system date first (see Step 4a-4e above), then retry.

---

### Troubleshooting: "curl: command not found"

**If you get this error, install curl first:**

**On your Pi (`pi@pi:~ $`), run:**

```bash
sudo apt update
sudo apt install curl -y
```

Then retry the installation.

---

## Step 5: Start Tailscale and Authenticate

**On your Pi (`pi@pi:~ $`), run:**

```bash
sudo tailscale up
```

**What you'll see:**
```
To authenticate, visit:
https://login.tailscale.com/a/xxxxx-xxxxx-xxxxx
```

**IMPORTANT:** 
1. **Copy that entire URL** (it's unique to your Pi)
2. **Don't close your Pi terminal** - you'll need to come back to it

---

## Step 6: Sign In to Tailscale

**On your computer or phone (NOT on the Pi):**

1. **Open the URL** from Step 5 in a web browser
   - The URL looks like: `https://login.tailscale.com/a/xxxxx-xxxxx-xxxxx`
   - Copy it exactly as shown

2. **Sign in** using one of these options:
   - **Google account** (easiest - recommended)
   - GitHub account
   - Microsoft account
   - Or create a new Tailscale account

3. **After signing in**, you'll see a success message like:
   ```
   Success! Your device is now connected to Tailscale.
   ```

**IMPORTANT - Account Requirements (Tailnet):**

**What is a Tailnet?**
- A **tailnet** is Tailscale's term for a private network of devices
- All devices signed in with the **same Tailscale account** belong to the **same tailnet**
- Devices in the same tailnet can automatically see and connect to each other
- Devices in **different tailnets** (different accounts) **cannot** see each other by default

**Option 1: Same Account / Same Tailnet (Easiest)**
- If you and your teacher sign in with the **exact same Tailscale account** (same email address), you'll both be in the **same tailnet**
- You'll automatically see each other's devices
- This is the simplest method - just use the same account!

**Option 2: Different Accounts / Different Tailnets (Requires Sharing)**
- If you use different accounts, you'll be in **different tailnets**
- Your teacher needs to share their device with you, or you need to share your Pi with them
- This requires additional setup in Tailscale admin console
- **Recommended:** Use the same account for simplicity

**Ask your teacher which account to use before signing in!**

---

## Step 7: Get Your Pi's Tailscale IP Address

**Go back to your Pi terminal (`pi@pi:~ $`), and run:**

```bash
tailscale ip -4
```

**Expected output:**
```
100.95.13.28
```

**This is your Pi's Tailscale IP address!** ✅

**Write this down or copy it - you'll need to share it with your teacher.**

**If you see nothing or an error:**
- Make sure you completed Step 6 (signed in via web browser)
- Wait 30 seconds, then try again: `tailscale ip -4`
- If still nothing, try: `sudo tailscale up` again

---

## Step 8: Verify It's Working

**On your Pi (`pi@pi:~ $`), check Tailscale status:**

```bash
sudo tailscale status
```

**Expected output:**
```
100.95.13.28   pi               your-email@  linux  -
100.66.211.91  teacher-device   your-email@  macOS  active; direct ...
```

You should see:
- Your Pi listed with its Tailscale IP (`100.95.13.28` in the example)
- Your teacher's device (if they're already connected)
- Both devices showing as connected

**If you only see your Pi:** That's okay! Your teacher will connect later.

---

## Step 9: Share Your Tailscale IP with Your Teacher

**Send your teacher:**
1. **Your Pi's Tailscale IP address** (from Step 7)
   - Example: `100.95.13.28`

**That's all they need!** ✅

---

## Step 10: Test Connection (Optional)

**Your teacher can now connect to your Pi using:**

```bash
ssh pi@<your-tailscale-ip>
```

**Example:**
```bash
ssh pi@100.95.13.28
```

They'll be asked for your Pi's password (the same one you use to log in).

---

## Complete Checklist

Before asking your teacher to connect, make sure:

- [ ] Tailscale is installed (`which tailscale` should show a path)
- [ ] You've signed in via the web browser (Step 6)
- [ ] You have a Tailscale IP address (`tailscale ip -4` shows an IP)
- [ ] Tailscale status shows your Pi (`sudo tailscale status`)
- [ ] You've shared your Tailscale IP with your teacher

---

## Common Troubleshooting

### "curl: command not found"
**Solution:** Install curl first:
```bash
sudo apt update
sudo apt install curl -y
```

### "Permission denied" when running sudo commands
**Solution:** 
- Make sure you're using the `pi` user (or your user with sudo access)
- Test: `sudo whoami` (should return "root")
- Enter your password when prompted

### "Can't access login URL"
**Solution:**
- Copy the URL exactly as shown (no extra spaces)
- Make sure you have internet access
- Try opening in a different browser
- Try on your phone if computer doesn't work

### "tailscale ip -4" shows nothing
**Solution:**
- Make sure you completed Step 6 (signed in via web browser)
- Try: `sudo tailscale up` again
- Wait 30 seconds, then try `tailscale ip -4` again
- Check status: `sudo tailscale status`

### "Installation failed" or SSL certificate errors
**Solution:**
- Check Pi's system date: `date` (should be current)
- If wrong, set it: `sudo date -s "YYYY-MM-DD HH:MM:SS"`
- Enable NTP: `sudo timedatectl set-ntp true`
- Retry installation

### "Pi can't reach internet but can reach gateway"
**Solution:**
- Your local network works, but internet is blocked
- Use Method B (manual installation) in Step 4
- Or fix your network/router settings

### "Teacher can't connect via Tailscale IP"
**Solution:**
- Verify your Pi's Tailscale IP: `tailscale ip -4`
- Check Tailscale status: `sudo tailscale status`
- **If using different accounts:** You need to share your Pi device (see section below)

---

## Alternative: Sharing Your Pi with Teacher (Different Accounts)

**When to use this:** If you and your teacher are using **different Tailscale accounts** (different tailnets), you can share your Pi device with them so they can access it.

**Note:** This is more complex than using the same account. We recommend using the same account for simplicity, but this method works if you need separate accounts.

---

### How Device Sharing Works

When you share your Pi device with your teacher:
- Your Pi stays in your tailnet
- Your teacher gets access to your Pi from their tailnet
- They can connect via SSH using your Pi's Tailscale IP address
- You control who has access and can revoke it anytime

---

### Step-by-Step: Share Your Pi Device

1. **Open Tailscale Admin Console**
   - Go to: https://login.tailscale.com/admin/machines
   - Or: Click Tailscale icon in menu bar → "Admin console"
   - Sign in with your Tailscale account (if not already signed in)

2. **Find Your Raspberry Pi Device**
   - Look for your device name (usually `pi` or `raspberrypi`)
   - Or look for your Tailscale IP address (from Step 7)
   - Click on the device to open its details page

3. **Click "Share..." or "Share device"**
   - This option appears in the device details page
   - If you don't see it, make sure you're on the device details page, not just the list

4. **Invite Your Teacher**
   - **Option A: Via Email**
     - Enter your teacher's email address (the one they used for Tailscale)
     - Click "Send invitation"
     - Your teacher will receive an email with the share link
   
   - **Option B: Generate Share Link**
     - Click "Generate share link" or "Copy link"
     - Send the link to your teacher (via email, chat, etc.)
     - Your teacher clicks the link to accept the share

5. **Wait for Teacher to Accept**
   - Your teacher needs to:
     1. Check their email for the invitation (or click the share link)
     2. Sign in to Tailscale (if not already signed in)
     3. Accept the share
   - This usually takes 1-2 minutes

6. **Verify Sharing Worked**
   - Your teacher should now be able to see your Pi in their Tailscale admin console
   - They can connect via SSH: `ssh pi@<your-tailscale-ip>`
   - Ask your teacher to confirm they can see your device

---

### Important Notes

- **Your Pi stays in your tailnet** - it's just shared with your teacher
- **Your teacher can only access your Pi** - they won't see your other devices
- **You can revoke access anytime** from your Tailscale admin console
- **This works with free Tailscale accounts** - no paid plan needed
- **You need to share each time** if your Pi gets a new Tailscale IP (rare, but possible)

---

### Troubleshooting Device Sharing

**Problem:** "I don't see the Share option"
- **Solution:** Make sure you clicked on the device to open its details page
- **Solution:** Make sure you're signed in to Tailscale admin console
- **Solution:** Try refreshing the page

**Problem:** "Teacher says they didn't receive the invitation"
- **Solution:** Check that you entered the correct email address
- **Solution:** Ask teacher to check spam/junk folder
- **Solution:** Try generating a share link instead and send it directly

**Problem:** "Teacher accepted but still can't see my Pi"
- **Solution:** Wait 1-2 minutes for Tailscale to sync
- **Solution:** Ask teacher to refresh their Tailscale admin console
- **Solution:** Verify your Pi is online and connected: `sudo tailscale status`
- **Solution:** Make sure you shared the correct device (check the Tailscale IP matches)

---

### "Teacher can't connect via Tailscale IP"
**Solution:**
- Verify your Pi's Tailscale IP: `tailscale ip -4`
- Check Tailscale status: `sudo tailscale status`
- **If using different accounts:** You need to share your Pi device (see section above)
- Make sure both you and teacher are signed in to same Tailscale account
- Wait a few minutes for Tailscale to fully connect
- Teacher should check their Tailscale status too

---

## What Your Teacher Needs

After completing all steps, share with your teacher:

1. **Your Pi's Tailscale IP address** (from `tailscale ip -4`)
   - Example: `100.95.13.28`

**That's it!** Your teacher can then connect using:
```bash
ssh pi@100.95.13.28
```

---

## Quick Reference Commands

```bash
# Check internet
ping -c 3 google.com

# Check system date
date

# Set date (if wrong)
sudo date -s "2025-02-19 14:30:00"
sudo timedatectl set-ntp true

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Start Tailscale
sudo tailscale up

# Get Tailscale IP
tailscale ip -4

# Check status
sudo tailscale status
```

---

## Next Steps

Once your teacher has set up Tailscale on their computer, they can connect to your Pi using:

```bash
ssh pi@<your-tailscale-ip>
```

**Your Pi is now accessible remotely!** ✅

---

*If you run into any problems not covered here, ask your teacher for help!*
