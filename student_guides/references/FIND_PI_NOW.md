# Find Your Raspberry Pi - Quick Steps

## Your Network Info
- **Router IP:** `172.20.80.1`
- **Your Mac IP:** `172.20.83.215`
- **Network Range:** `172.20.80.x` to `172.20.87.x`

---

## Method 1: Try Router Admin Page (Different URLs)

The router admin page might need `http://` or `https://`. Try these in Safari:

1. **http://172.20.80.1** (try this first)
2. **https://172.20.80.1**
3. **http://172.20.80.1:8080**
4. **http://router.local** (some routers support this)

**What to look for:**
- "Connected Devices"
- "DHCP Clients" 
- "Network Map"
- "Attached Devices"
- "Client List"

**Look for:** "raspberrypi" or "Raspberry Pi" in the device list

---

## Method 2: Use Mac's Built-In Scanner (No Apps Needed!)

**Use Terminal commands built into your Mac:**

See detailed guide: **[MAC_BUILT_IN_SCANNER.md](MAC_BUILT_IN_SCANNER.md)**

**Quick methods:**
1. **Try hostname first:**
   ```bash
   ping -c 1 raspberrypi.local
   ```
   If it works, use: `ssh pi@raspberrypi.local`

2. **Check ARP table:**
   ```bash
   arp -a | grep "172.20"
   ```
   Look for Raspberry Pi MAC addresses (B8:27:EB, DC:A6:32, E4:5F:01)

3. **Test each device:**
   ```bash
   ssh pi@172.20.80.XXX
   ```
   (Replace XXX with IPs from ARP table)

**Full guide:** See `MAC_BUILT_IN_SCANNER.md` for complete step-by-step instructions.

---

## Method 2.5: Use the Scan Script (Easiest!)

I created a script that will scan your network automatically:

1. **Open Terminal on your Mac**

2. **Run the scan script:**
   ```bash
   cd ~/Documents/raspberry
   ./find_pi.sh
   ```

3. **Wait for it to scan** (may take 1-2 minutes)

4. **It will show you the Pi's IP address if found**

---

## Method 3: Use Network Scanner App (Fastest!)

**Download a network scanner app:**

### Option A: Fing (Mobile - Easiest)
1. Download **Fing** app on your phone
2. Make sure phone is on same WiFi
3. Open app, tap "Scan"
4. Look for "raspberrypi" in the list
5. Note the IP address

### Option B: LanScan (Mac App Store)
1. Search "LanScan" in Mac App Store
2. Download (paid app, but works well)
3. Open and click "Scan"
4. Look for "raspberrypi"

### Option C: Angry IP Scanner (Free Desktop)
1. Go to: https://angryip.org/download/
2. Download for Mac
3. Enter range: `172.20.80.1` to `172.20.87.255`
4. Click "Start"
5. Look for "raspberrypi" in results

---

## Method 4: Check if Pi is Actually Connected

**Before scanning, verify:**

1. **Is Pi powered on?**
   - Red LED should be on (power)
   - Green LED should flash occasionally (activity)

2. **How long has Pi been on?**
   - Wait at least 1-2 minutes after powering on
   - First boot takes time to connect to WiFi

3. **Is WiFi configured correctly?**
   - You said you entered WiFi name and password in Imager ✓
   - Make sure it's the SAME WiFi network your Mac is on ✓

4. **Try power cycling:**
   - Unplug Pi power
   - Wait 10 seconds
   - Plug back in
   - Wait 2 minutes
   - Then try finding it again

---

## Method 5: Manual IP Range Check

If you want to try manually:

1. **Open Terminal**

2. **Try common IPs:**
   ```bash
   # Try these one by one:
   ping -c 1 172.20.80.10
   ping -c 1 172.20.80.20
   ping -c 1 172.20.80.50
   ping -c 1 172.20.80.100
   ping -c 1 172.20.80.101
   ping -c 1 172.20.80.102
   ```

3. **If ping works, try SSH:**
   ```bash
   ssh pi@172.20.80.XXX
   ```
   (Replace XXX with the IP that responded)

---

## Once You Find the IP Address

**SSH into your Pi:**
```bash
ssh pi@<ip-address>
```

**First time:**
- Type `yes` when asked about authenticity
- Enter password (the one you set in Imager)
- Password won't show on screen - that's normal!

**Success looks like:**
```
pi@raspberrypi:~ $
```

---

## Troubleshooting

### "Connection refused" when trying SSH
- Pi might not have SSH enabled
- Wait longer (first boot takes time)
- Try again in 1-2 minutes

### Can't find Pi anywhere
- **Check:** Is Pi actually powered on? (red LED on?)
- **Check:** Did you wait 2 minutes after powering on?
- **Check:** Is Pi on the same WiFi network?
- **Try:** Power cycle the Pi (unplug, wait 10 sec, plug back in)

### Router admin page won't load
- Try `http://` instead of `https://`
- Try different ports: `:8080`, `:80`
- Check router manual for admin page URL
- Some routers use different IPs (check router label)

---

## Recommended: Start with Method 2 (Scan Script)

**Easiest and fastest:**
```bash
cd ~/Documents/raspberry
./find_pi.sh
```

This will automatically scan and find your Pi!
