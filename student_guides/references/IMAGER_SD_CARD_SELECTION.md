# Raspberry Pi Imager - SD Card Selection Guide

## "Exclude System Files" Option

### Quick Answer

**For writing Raspberry Pi OS: NO, don't exclude system files.**

You want to write to the **entire SD card**.

---

## What This Option Means

**"Exclude system files"** typically means:
- Don't show system/internal partitions
- Only show user-accessible storage
- Filter out hidden system volumes

**For SD card setup:**
- You want to write to the **whole card**
- Not just a partition
- Imager needs full access to format and write OS

---

## What to Select in Imager

### When Clicking "Choose Storage"

**You should see:**
- Your SD card listed (may show as "Untitled" or card size)
- Card's total capacity (e.g., "32 GB" or "64 GB")
- Possibly multiple entries if card has partitions

**What to select:**
- ✅ **Select the main SD card entry** (the one showing full size)
- ✅ **Don't exclude system files** - you want full access
- ✅ Select the card itself, not a partition

**Example:**
```
Choose Storage:
  ☑️ Generic MassStorageClass Media [32.0 GB]  ← Select this one
  ☐ Generic MassStorageClass Media [32.0 GB] - Partition 1  ← Don't select partition
```

---

## Why This Matters

**Raspberry Pi Imager needs to:**
1. **Erase entire card** - Remove all existing partitions
2. **Create new partitions** - Boot partition + root partition
3. **Format partitions** - Set up file systems
4. **Write OS files** - Install Raspberry Pi OS

**If you exclude system files:**
- Imager might not see the full card
- May only see one partition
- Can't properly format the entire card
- Installation might fail

---

## Step-by-Step Selection

1. **Click "Choose Storage"** in Imager
2. **Look for your SD card:**
   - Should show card name or "Untitled"
   - Should show full size (e.g., 32 GB, 64 GB)
3. **Select the main card entry** (not a partition)
4. **If there's a checkbox for "exclude system files":**
   - **Leave it UNCHECKED** (you want to see everything)
5. **Click to select the card**
6. **Proceed with writing**

---

## If You See Multiple Entries

**If card shows multiple entries:**
- **Select the one with full size** (e.g., "32.0 GB")
- **Not individual partitions** (e.g., "500 MB" or "31.5 GB")
- Imager will handle partitioning automatically

**Common partition names you might see (DON'T select these):**
- `bootfs` - Boot partition (small, ~500 MB)
- `rootfs` - Root partition (larger, ~31 GB)
- Any entry with "Partition" in the name

**What to select instead:**
- The **parent card entry** showing the full card size
- May show as "Generic MassStorageClass Media" or card brand name
- Should show total capacity (e.g., "32.0 GB")

---

## Verification

**After selecting storage, you should see:**
- Card name/size in Imager
- Ready to write message
- No errors

**If you see errors:**
- Try selecting different entry
- Uncheck "exclude system files" if checked
- Make sure card is not locked

---

## Summary

✅ **Select the main SD card** (full size)  
✅ **Don't exclude system files** - leave unchecked  
✅ **Select card, not partitions**  
✅ **Imager will handle everything**

---

*For OS installation, you want Imager to have full access to the entire card!*
