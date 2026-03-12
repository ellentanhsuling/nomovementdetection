# Accessing Raspberry Pi on a Different Network

## Overview

If your student's Raspberry Pi is on a different network (like their home WiFi), you can't access it directly using local network scanning. This guide shows you several ways to access the Pi remotely.

---

## Prerequisites

- Raspberry Pi is powered on and connected to the internet
- You have the student's cooperation to set up remote access
- Both you and the student have internet access

---

## Method 1: Bring Pi to Same Network (Simplest - Recommended for Class)

**Best for:** In-person classes, labs, or when student can bring Pi to school

### Step 1: Student Brings Pi to School

Have the student:
1. Power off the Pi
2. Bring it to school/lab
3. Connect it to the same WiFi network as your Mac
4. Power it on

### Step 2: Find the Pi on Local Network

Once on the same network, use the methods in `MAC_BUILT_IN_SCANNER.md`:

```bash
# Try hostname first
ping -c 1 raspberrypi.local

# Or check ARP table
arp -a | grep "172.20"
```

### Step 3: SSH to Pi

```bash
ssh pi@<ip-address>
# or
ssh pi@raspberrypi.local
```

**Advantages:**
- ✅ No setup required
- ✅ Fast and reliable
- ✅ Works immediately
- ✅ No security concerns

**Disadvantages:**
- ❌ Requires physical access
- ❌ Student must bring Pi to location

---

## Method 2: Tailscale VPN (Free, Easy - Recommended for Remote Access)

**Best for:** Remote access when student can't bring Pi to school

Tailscale creates a secure VPN between devices - **completely free for personal use** and very easy to set up.

**📖 For detailed step-by-step instructions, see:**
- **Students:** `TAILSCALE_SETUP_STUDENT.md` - Complete guide with troubleshooting
- **Teachers:** `TAILSCALE_SETUP_TEACHER.md` - Complete guide with troubleshooting

### Quick Overview

**Student (on Pi):**
1. Install Tailscale: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Start Tailscale: `sudo tailscale up`
3. Sign in via web browser (URL provided)
4. Get Tailscale IP: `tailscale ip -4`
5. Share IP with teacher

**Teacher (on Mac):**
1. Install Tailscale from Mac App Store or tailscale.com/download
2. Sign in with same account
3. Connect via SSH: `ssh pi@<student-tailscale-ip>`

**For complete instructions and troubleshooting, see the detailed guides above.**

**Advantages:**
- ✅ Free for personal use
- ✅ Easy setup (5-10 minutes)
- ✅ Secure (encrypted VPN)
- ✅ Works from anywhere with internet
- ✅ No router configuration needed

**Disadvantages:**
- ❌ Requires both parties to install Tailscale
- ❌ Requires internet connection

---

## Method 3: ZeroTier VPN (Alternative Free Option)

**Best for:** Similar to Tailscale, another free VPN option

### Step 1: Student Sets Up ZeroTier on Pi

**On the Raspberry Pi:**

```bash
# Install ZeroTier
curl -s https://install.zerotier.com | sudo bash

# Join a network (student creates network at my.zerotier.com)
sudo zerotier-cli join <NETWORK_ID>

# Get the IP address
sudo zerotier-cli listnetworks
```

### Step 2: You Join Same ZeroTier Network

**On your Mac:**

1. Visit: https://www.zerotier.com/download/
2. Download and install ZeroTier for macOS
3. Join the same network ID
4. Approve both devices in the ZeroTier web interface

### Step 3: Access Pi via ZeroTier IP

```bash
ssh pi@<zerotier-ip>
```

**Advantages:**
- ✅ Free
- ✅ Works from anywhere
- ✅ No router setup

**Disadvantages:**
- ❌ Slightly more complex than Tailscale
- ❌ Requires network approval in web interface

---

## Method 4: SSH Port Forwarding (Advanced - Not Recommended)

**Best for:** When VPN services aren't available (requires router access)

This method requires the student to configure port forwarding on their home router, which is:
- Complex for students
- Security risk if not done correctly
- May not work if router doesn't support it

**⚠️ Not recommended for student projects** - Use Method 1 or 2 instead.

---

## Method 5: Dynamic DNS + Port Forwarding (Very Advanced)

**Best for:** Permanent remote access (not recommended for students)

Requires:
- Router configuration
- Dynamic DNS service
- Port forwarding setup
- Security hardening

**⚠️ Not recommended** - Too complex and risky for student projects.

---

## Quick Decision Guide

### "Student can bring Pi to school"
→ **Use Method 1** (Same Network)

### "Student is at home, needs remote access"
→ **Use Method 2** (Tailscale) - Easiest and free

### "Tailscale doesn't work"
→ **Use Method 3** (ZeroTier) - Alternative VPN

### "Need permanent remote access"
→ Consider Method 5 (but not for students)

---

## Step-by-Step: Setting Up Tailscale (Recommended)

**📖 For complete detailed instructions with troubleshooting, see:**
- **Students:** `TAILSCALE_SETUP_STUDENT.md` - Includes all troubleshooting steps, date fixes, manual installation, etc.
- **Teachers:** `TAILSCALE_SETUP_TEACHER.md` - Includes App Store installation, verification steps, SSH troubleshooting, etc.

**Quick summary:**
1. Student follows `TAILSCALE_SETUP_STUDENT.md` on their Pi
2. Teacher follows `TAILSCALE_SETUP_TEACHER.md` on their Mac
3. Teacher connects: `ssh pi@<student-tailscale-ip>`

**That's it!** ✅

---

## Troubleshooting

### "Can't connect via Tailscale IP"
- **Check:** Is Tailscale running on both devices?
  ```bash
  # On Mac
  tailscale status
  
  # On Pi
  sudo tailscale status
  ```
- **Check:** Are both devices signed in to same Tailscale account?
- **Check:** Is Pi's Tailscale IP correct? (`tailscale ip -4` on Pi)

### "Student can't install Tailscale on Pi"
- **Check:** Pi has internet connection: `ping -c 3 google.com`
- **Check:** Student has sudo access: `sudo whoami` (should return "root")
- **Try:** Manual installation from Tailscale docs

### "Pi is on different network but student can't set up VPN"
- **Solution:** Use Method 1 - have student bring Pi to school
- **Alternative:** Use screen sharing (student shares screen while you guide them)

### "Need to access multiple student Pis"
- **Solution:** Each student sets up Tailscale, you join their network or they add you
- **Or:** All students join one shared Tailscale network (you create it)

---

## Security Notes

### Tailscale/ZeroTier (VPN Methods)
- ✅ Encrypted connection
- ✅ Only devices on same network can access
- ✅ No open ports on router
- ✅ Generally safe for student projects

### Port Forwarding (Not Recommended)
- ⚠️ Opens router to internet
- ⚠️ Requires strong passwords
- ⚠️ Risk of unauthorized access
- ⚠️ Not recommended for students

---

## Quick Reference

```bash
# Method 1: Same Network
ping -c 1 raspberrypi.local
ssh pi@<local-ip>

# Method 2: Tailscale
ssh pi@<tailscale-ip>

# Check Tailscale status
tailscale status
tailscale ip -4
```

---

## Next Steps After Connecting

Once you can SSH to the Pi:

1. **Verify it's the right Pi:**
   ```bash
   hostname
   ```

2. **Check network info:**
   ```bash
   hostname -I
   ```

3. **Continue with your project setup** (see other student guides)

---

*For in-person classes, Method 1 (same network) is recommended. For remote access, Method 2 (Tailscale) is the easiest and safest option.*
