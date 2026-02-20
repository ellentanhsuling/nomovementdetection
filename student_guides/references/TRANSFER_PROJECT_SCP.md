# Transfer Project to Raspberry Pi Using SCP

## Overview

We're transferring the **non-movement detection project** to your Raspberry Pi. This includes:
- The `shared/` library (common code)
- The `non_movement/` project (detection system)
- Configuration files

**Your Pi IP:** `172.20.83.63`  
**Pi Username:** `pi`

---

## Files to Transfer

### Required Directories:
1. **`shared/`** - Shared library (sensors, alerts, utils)
2. **`non_movement/`** - Non-movement detection project

### Optional Files:
- `README.md` - Project documentation
- `.gitignore` - Git ignore file (if you're using git)

---

## Step 1: Prepare on Your Mac

**From your Mac terminal, navigate to the project directory:**

```bash
cd ~/Documents/raspberry
```

**Verify you're in the right place:**
```bash
ls -la
```

You should see `shared/` and `non_movement/` directories.

---

## Step 2: Transfer Shared Library

**Transfer the entire `shared/` directory:**

```bash
scp -r shared pi@172.20.83.63:/home/pi/
```

**What this does:**
- `-r` = recursive (copies entire directory)
- `shared` = source directory
- `pi@172.20.83.63` = Pi username and IP
- `/home/pi/` = destination on Pi

**Enter password when prompted** (the one you set in Imager).

---

## Step 3: Transfer Non-Movement Project

**Transfer the entire `non_movement/` directory:**

```bash
scp -r non_movement pi@172.20.83.63:/home/pi/
```

**Enter password when prompted.**

---

## Step 4: Verify Transfer

**SSH into your Pi:**

```bash
ssh pi@172.20.83.63
```

**Check that files were transferred:**

```bash
ls -la ~/shared
ls -la ~/non_movement
```

**You should see:**
- `~/shared/` with subdirectories: `sensors/`, `alerts/`, `utils/`, `base/`
- `~/non_movement/` with: `main.py`, `config.yaml`, `requirements.txt`, `detection/`

---

## Step 5: Organize Project Structure

**On the Pi, create the project structure:**

```bash
cd ~
mkdir -p raspberry
mv shared raspberry/
mv non_movement raspberry/
cd raspberry
```

**Verify structure:**

```bash
ls -la
```

Should show:
```
raspberry/
├── shared/
└── non_movement/
```

---

## Alternative: Transfer Everything at Once

**If you want to transfer both directories in one command:**

```bash
cd ~/Documents/raspberry
scp -r shared non_movement pi@172.20.83.63:/home/pi/raspberry/
```

**Note:** This assumes the `raspberry/` directory exists on the Pi. If not, create it first:

```bash
ssh pi@172.20.83.63 "mkdir -p ~/raspberry"
```

Then transfer:
```bash
scp -r shared non_movement pi@172.20.83.63:/home/pi/raspberry/
```

---

## Troubleshooting

### "Permission denied"
- Check password is correct
- Make sure SSH is enabled on Pi

### "Connection refused"
- Check Pi is powered on
- Check Pi IP address is correct
- Wait a minute and try again

### "No such file or directory"
- Make sure you're in the right directory on Mac
- Check destination path on Pi exists

### Files not transferring
- Check you have write permissions on Pi
- Try transferring one directory at a time
- Check disk space on Pi: `df -h`

---

## After Transfer: Next Steps

1. **SSH into Pi:**
   ```bash
   ssh pi@172.20.83.63
   ```

2. **Navigate to project:**
   ```bash
   cd ~/raspberry/non_movement
   ```

3. **Check config is correct:**
   ```bash
   cat config.yaml
   ```
   (Should show 10-second threshold for prototype)

4. **Continue with Step 9: Set Up Python Environment**

---

## Quick Reference

**Transfer commands (run from your Mac):**

```bash
# Navigate to project
cd ~/Documents/raspberry

# Create directory on Pi (if needed)
ssh pi@172.20.83.63 "mkdir -p ~/raspberry"

# Transfer shared library
scp -r shared pi@172.20.83.63:/home/pi/raspberry/

# Transfer non-movement project
scp -r non_movement pi@172.20.83.63:/home/pi/raspberry/
```

**Verify on Pi:**

```bash
ssh pi@172.20.83.63
cd ~/raspberry
ls -la
```

---

**Ready to transfer! Start with Step 2 above.**
