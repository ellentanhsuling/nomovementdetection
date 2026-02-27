# Using Mac's Built-In Tools to Find Raspberry Pi

## Overview

Your Mac has built-in command-line tools that can scan your network and find your Raspberry Pi - **no extra apps needed!** This guide shows you how to use them step-by-step.

---

## Prerequisites

- Your Mac and Raspberry Pi are on the **same WiFi network**
- Raspberry Pi is **powered on** and has been on for at least 1-2 minutes
- Terminal app (built into Mac)

---

## Method 1: Check ARP Table (Fastest - Shows Recent Devices)

The ARP (Address Resolution Protocol) table shows devices your Mac has recently communicated with.

### Step 1: Open Terminal

Press `Cmd + Space`, type "Terminal", press Enter.

### Step 2: View ARP Table

```bash
arp -a
```

**What you'll see:**
```
? (172.20.80.1) at ec:a7:8d:3c:e9:7f on en1 ifscope [ethernet]
? (172.20.83.63) at 2c:cf:67:43:84:54 on en1 ifscope [ethernet]
```

Each line shows:
- **IP address** (in parentheses)
- **MAC address** (the hardware address)
- **Interface** (en1 = WiFi, en0 = Ethernet)

### Step 3: Identify Raspberry Pi

**Look for Raspberry Pi MAC addresses:**
- Raspberry Pi Foundation MACs often start with:
  - `B8:27:EB` (older Pi models)
  - `DC:A6:32` (Pi 4 and newer)
  - `E4:5F:01` (Pi Zero)

**Example:**
```bash
arp -a | grep -i "b8:27:eb\|dc:a6:32\|e4:5f:01"
```

### Step 4: Test Each Device

For each IP address you find, try to SSH:

```bash
ssh pi@172.20.83.63
```

If it asks for a password, that's your Pi! ✅

---

## Method 2: Try Bonjour/mDNS Hostname (Easiest if It Works)

Raspberry Pi OS often advertises itself as `raspberrypi.local` on the network.

### Step 1: Try the Hostname Directly

```bash
ping -c 1 raspberrypi.local
```

**If it works, you'll see:**
```
PING raspberrypi.local (172.20.83.215): 56 data bytes
64 bytes from 172.20.83.215: icmp_seq=0 ttl=64 time=2.456 ms
```

**The IP address is shown in parentheses!** ✅

### Step 2: SSH Using Hostname

```bash
ssh pi@raspberrypi.local
```

**Advantage:** Works even if the IP address changes!

### Step 3: If Hostname Doesn't Work

The Pi might not be advertising via mDNS. Try the other methods below.

---

## Method 3: Ping Scan Your Network Range

This scans all IP addresses in your network to find active devices.

### Step 1: Find Your Network Range

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Example output:**
```
inet 172.20.83.39 netmask 0xfffff800 broadcast 172.20.87.255
```

This tells you:
- **Your Mac's IP:** `172.20.83.39`
- **Network range:** `172.20.80.x` to `172.20.87.x` (based on netmask)

### Step 2: Scan the Network Range

Replace `172.20.80` with your network prefix:

```bash
for i in {1..254}; do
    ip="172.20.80.$i"
    if ping -c 1 -W 1 $ip > /dev/null 2>&1; then
        echo "✓ Found device at $ip"
        # Try to get hostname
        hostname=$(nslookup $ip 2>/dev/null | grep "name" | awk '{print $4}' | cut -d. -f1)
        if [ ! -z "$hostname" ]; then
            echo "  Hostname: $hostname"
        fi
    fi
done
```

**This will:**
- Ping each IP from 172.20.80.1 to 172.20.80.254
- Show which ones respond
- Try to get hostnames for responding devices
- **Note:** This takes 1-2 minutes to complete

### Step 3: Test Each Found Device

For each device that responds, try SSH:

```bash
ssh pi@172.20.80.XXX
```

(Replace XXX with the IP that responded)

---

## Method 4: Quick One-Liner to Find Pi

This combines ARP table check with hostname lookup:

```bash
arp -a | while read line; do
    ip=$(echo "$line" | awk '{print $2}' | tr -d '()')
    if [[ "$ip" =~ ^172\. ]] || [[ "$ip" =~ ^192\.168\. ]] || [[ "$ip" =~ ^10\. ]]; then
        hostname=$(nslookup "$ip" 2>/dev/null | grep "name" | awk '{print $4}' | cut -d. -f1)
        if [[ "$hostname" == *"raspberry"* ]] || [[ "$hostname" == *"pi"* ]]; then
            echo "🎉 Found Raspberry Pi!"
            echo "   IP: $ip"
            echo "   Hostname: $hostname"
        fi
    fi
done
```

**What it does:**
- Checks all devices in ARP table
- Looks up hostnames
- Finds any with "raspberry" or "pi" in the name

---

## Method 5: Check MAC Address in ARP Table

If you know the Pi's MAC address, you can find it directly:

### Step 1: View ARP Table with MAC Addresses

```bash
arp -a | grep "172.20"
```

### Step 2: Look for Raspberry Pi MAC Prefixes

```bash
arp -a | grep -E "b8:27:eb|dc:a6:32|e4:5f:01"
```

**Common Raspberry Pi MAC prefixes:**
- `B8:27:EB` - Older Pi models (Pi 1, 2, 3)
- `DC:A6:32` - Pi 4 and newer
- `E4:5F:01` - Pi Zero

### Step 3: Extract IP Address

If you find a match, the IP address is in the line:
```
? (172.20.83.215) at dc:a6:32:12:34:56 on en1
```

The IP is `172.20.83.215` ✅

---

## Complete Step-by-Step Workflow

**Recommended order to try:**

### 1. Try Hostname First (Easiest)
```bash
ping -c 1 raspberrypi.local
```
If it works → Use `ssh pi@raspberrypi.local` ✅

### 2. Check ARP Table (Fast)
```bash
arp -a | grep "172.20"
```
Look for Raspberry Pi MAC addresses or try SSH on each IP

### 3. Scan Network Range (Thorough)
Use Method 3 to scan all IPs in your network

### 4. Use Your Scan Script
```bash
cd ~/Documents/raspberry
./find_pi.sh
```

---

## Troubleshooting

### "No devices found in ARP table"
- **Solution:** The Pi might not have communicated with your Mac yet
- **Try:** Ping the router first: `ping -c 1 172.20.80.1`
- **Then:** Check ARP table again: `arp -a`

### "raspberrypi.local not found"
- **Solution:** Pi might not be advertising via mDNS
- **Try:** Other methods (ARP table, network scan)

### "Ping scan takes too long"
- **Solution:** Scan only common IPs first:
  ```bash
  for ip in 172.20.80.{1,10,20,50,100,101,102}; do
      ping -c 1 -W 1 $ip > /dev/null 2>&1 && echo "✓ $ip responds"
  done
  ```

### "SSH connection refused"
- **Solution:** Pi might not have SSH enabled
- **Check:** Wait 1-2 minutes after powering on
- **Try:** Enable SSH via Raspberry Pi Imager settings

### "Can't find Pi anywhere"
- **Check:** Is Pi powered on? (Red LED on?)
- **Check:** Is Pi on same WiFi network?
- **Check:** Wait 2 minutes after powering on
- **Try:** Power cycle the Pi (unplug, wait 10 sec, plug back in)

---

## Quick Reference Commands

```bash
# Check ARP table
arp -a

# Try hostname
ping -c 1 raspberrypi.local

# Find your network
ifconfig | grep "inet " | grep -v 127.0.0.1

# Test SSH on an IP
ssh pi@172.20.80.XXX

# Scan for Pi MAC addresses
arp -a | grep -i "b8:27:eb\|dc:a6:32\|e4:5f:01"
```

---

## Understanding the Output

### ARP Table Format
```
? (IP_ADDRESS) at MAC_ADDRESS on INTERFACE ifscope [ethernet]
```

- **`?`** = Hostname not resolved (normal for most devices)
- **IP_ADDRESS** = Device's IP (what you need!)
- **MAC_ADDRESS** = Hardware address (helps identify device type)
- **INTERFACE** = Network interface (en1 = WiFi, en0 = Ethernet)

### Ping Output
```
PING raspberrypi.local (172.20.83.215): 56 data bytes
64 bytes from 172.20.83.215: icmp_seq=0 ttl=64 time=2.456 ms
```

- **IP in parentheses** = The actual IP address ✅
- **time** = Response time (lower is better)

---

## Why These Methods Work

1. **ARP Table:** Your Mac remembers devices it has talked to
2. **Bonjour/mDNS:** Pi advertises itself as `raspberrypi.local`
3. **Ping Scan:** Tests every IP to see which respond
4. **MAC Address:** Hardware identifier unique to each device

All of these use **built-in Mac tools** - no installation needed!

---

## Next Steps

Once you find the IP address:

1. **SSH into your Pi:**
   ```bash
   ssh pi@<ip-address>
   ```

2. **First time connection:**
   - Type `yes` when asked about authenticity
   - Enter your password (won't show on screen - that's normal!)

3. **Success looks like:**
   ```
   pi@raspberrypi:~ $
   ```

---

*All commands shown work in Terminal on macOS. No additional software required!*
