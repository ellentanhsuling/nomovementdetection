# Student Build Guide - Step 2: Setup Your Computer

## What You're Doing

Setting up your computer so you can write and test code before using the Raspberry Pi.

---

## Step 1: Check Python is Installed

### On Mac/Linux:
```bash
python3 --version
```

### On Windows:
```bash
python --version
```

**You need Python 3.8 or higher.**

If you don't have Python:
- **Download**: https://www.python.org/downloads/
- **Install**: Follow the installer (check "Add Python to PATH" on Windows)

---

## Step 2: Create Project Folder

```bash
# Create a folder for your project
mkdir raspberry
cd raspberry
```

**Where to run this**: Open Terminal (Mac/Linux) or Command Prompt (Windows)

---

## Step 3: Create Virtual Environment

**Why?** Keeps your project's packages separate from other projects.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**You'll see `(venv)` in your terminal** - that means it's working!

---

## Step 4: Install Required Packages

**What are packages?** Pre-written code you can use (like libraries).

Install these one by one:

```bash
# Configuration files
pip install pyyaml

# Environment variables
pip install python-dotenv

# HTTP requests (for API alerts)
pip install requests

# Image processing
pip install numpy
pip install opencv-python
pip install Pillow

# Date/time handling
pip install python-dateutil

# Testing (optional but recommended)
pip install pytest
```

**Package References:**
- **PyYAML**: https://pypi.org/project/PyYAML/ - For reading config files
- **OpenCV**: https://pypi.org/project/opencv-python/ - For image processing
- **NumPy**: https://pypi.org/project/numpy/ - For working with arrays
- **Pillow**: https://pypi.org/project/Pillow/ - For image manipulation

---

## Step 5: Create Project Folders

Create the folder structure:

```bash
# Shared library folders
mkdir -p shared/sensors
mkdir -p shared/alerts
mkdir -p shared/data
mkdir -p shared/utils
mkdir -p shared/base

# Project 1 folders
mkdir -p non_movement/detection

# Project 2 folders
mkdir -p fall_detection/detection

# Tests folder
mkdir tests
```

**What this does**: Creates empty folders where you'll put your code files.

---

## Step 6: Create Empty Python Files

Create `__init__.py` files (tells Python these are packages):

```bash
# Shared library
touch shared/__init__.py
touch shared/sensors/__init__.py
touch shared/alerts/__init__.py
touch shared/data/__init__.py
touch shared/utils/__init__.py
touch shared/base/__init__.py

# Projects
touch non_movement/__init__.py
touch non_movement/detection/__init__.py
touch fall_detection/__init__.py
touch fall_detection/detection/__init__.py

# Tests
touch tests/__init__.py
```

**On Windows**, use:
```bash
# Instead of touch, create empty files:
type nul > shared/__init__.py
```

---

## Step 7: Verify Setup

Check your structure:

```bash
# See your folders
ls -R
# On Windows: dir /s
```

You should see all the folders you created.

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed
- [ ] Project folders created
- [ ] `__init__.py` files created

---

## Common Issues

### "pip: command not found"
- **Solution**: Use `pip3` instead of `pip`
- Or: `python -m pip install package_name`

### "venv: command not found"
- **Solution**: Install venv: `python3 -m pip install virtualenv`

### Packages won't install
- **Solution**: Update pip first: `pip install --upgrade pip`

---

## Next Step

Once everything is set up, go to **STUDENT_GUIDE_03_SHARED_LIBRARY.md**

---

*Take your time. Setup is important - get it right!*
