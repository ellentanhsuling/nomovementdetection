# SD Card Shows "bootfs" - What to Do

## What "bootfs" Means

**"bootfs"** is the **boot partition** from a previous Raspberry Pi installation.

This means:
- ✅ Your SD card was used with a Raspberry Pi before
- ✅ It has existing partitions (bootfs = boot, rootfs = root)
- ✅ This is **completely normal** and fine!

---

## What You're Seeing

When you click "Choose Storage" in Raspberry Pi Imager, you might see:

```
Storage Options:
  ☐ Generic MassStorageClass Media [32.0 GB]  ← Select THIS one
  ☐ bootfs [500 MB]  ← Don't select this (it's a partition)
  ☐ rootfs [31.5 GB]  ← Don't select this (it's a partition)
```

**OR** you might only see:
```
Storage Options:
  ☐ bootfs [500 MB]  ← This is just a partition, not the full card
```

---

## What to Select

### ✅ CORRECT: Select the Main Card

**Look for:**
- Entry showing **full card size** (e.g., "32.0 GB", "64.0 GB")
- May be named:
  - "Generic MassStorageClass Media"
  - Card brand name (e.g., "SanDisk", "Samsung")
  - "Untitled" or "NO NAME"
- **NOT** showing "bootfs" or "rootfs" in the name

### ❌ WRONG: Don't Select Partitions

**Don't select:**
- `bootfs` (small partition, ~500 MB)
- `rootfs` (larger partition, ~31 GB)
- Any entry with "Partition" in the name
- Any entry showing only part of the card size

---

## Why This Matters

**Raspberry Pi Imager needs to:**
1. **Erase the entire card** (all partitions)
2. **Create new partitions** (fresh boot + root)
3. **Write the OS** to the new partitions

**If you select a partition instead:**
- Imager can't erase the whole card
- May fail or create errors
- Won't properly format the card

---

## Step-by-Step Selection

1. **Click "Choose Storage"** in Imager
2. **Look at all entries** - you should see multiple options
3. **Find the entry with:**
   - Full card size (e.g., "32.0 GB")
   - No "bootfs" or "rootfs" in the name
   - May be at the top or bottom of the list
4. **Select that main card entry**
5. **Ignore/Don't select:**
   - bootfs entries
   - rootfs entries
   - Any partition entries

---

## If You Only See "bootfs"

**If you only see "bootfs" and no main card entry:**

1. **Check if "exclude system files" is checked:**
   - If yes, **uncheck it**
   - This might hide the main card entry

2. **Look more carefully:**
   - Main card might be listed separately
   - Scroll through all options
   - Main card might be at the top or bottom

3. **Try refreshing:**
   - Close and reopen Imager
   - Unplug and replug SD card reader
   - Restart Imager

---

## Verification

**After selecting, you should see:**
- Card name/size in Imager (e.g., "32.0 GB")
- **NOT** "bootfs" or "rootfs"
- Ready to write message
- No errors

**If you see "bootfs" selected:**
- ❌ Wrong - this is just a partition
- Go back and select the main card entry

---

## Example Selection

**What you might see:**
```
Choose Storage Device:

  ☑️ Generic MassStorageClass Media [32.0 GB]  ← ✅ SELECT THIS
  ☐ bootfs [500 MB]  ← ❌ Don't select
  ☐ rootfs [31.5 GB]  ← ❌ Don't select
```

**After selecting correctly:**
- Imager shows: "Generic MassStorageClass Media [32.0 GB]"
- Ready to write OS

---

## Summary

✅ **"bootfs" is normal** - card was used before  
✅ **Select the main card** (full size, not bootfs)  
✅ **Don't select partitions** (bootfs, rootfs)  
✅ **Imager will erase everything** and create fresh partitions  

---

*The card having "bootfs" just means it was used before - Imager will wipe it clean!*
