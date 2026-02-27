# Student Build Guide - Index

## Complete Guide Set

Follow these guides **in order** to build the entire project:

---

## 📚 Guide List

### 1. **STUDENT_GUIDE_01_OVERVIEW.md**
**What it covers:**
- What you're building
- Project structure overview
- Build order
- Important concepts

**Read this first!** Gives you the big picture.

---

### 2. **STUDENT_GUIDE_02_SETUP.md**
**What it covers:**
- Installing Python
- Setting up virtual environment
- Installing packages
- Creating project folders

**Time needed:** 30-60 minutes

---

### 3. **STUDENT_GUIDE_03_SHARED_LIBRARY.md**
**What it covers:**
- Building shared code (used by both projects)
- Camera sensors (mock + real)
- Alert system (email, SMS, API)
- Utilities and base classes

**Time needed:** 4-6 hours

**Key files to create:**
- `shared/sensors/base_sensor.py`
- `shared/sensors/mock_camera.py`
- `shared/sensors/real_camera.py`
- `shared/alerts/logger.py`
- `shared/alerts/email_alert.py`
- `shared/alerts/sms_alert.py`
- `shared/alerts/api_alert.py`
- `shared/utils/config_loader.py`
- `shared/utils/time_utils.py`
- `shared/base/monitoring_base.py`

---

### 4. **STUDENT_GUIDE_04_NON_MOVEMENT.md**
**What it covers:**
- Building non-movement detection project
- Movement detector algorithm
- Pattern learning
- Alert management
- Main application

**Time needed:** 3-4 hours

**Key files to create:**
- `non_movement/detection/movement_detector.py`
- `non_movement/detection/pattern_learner.py`
- `non_movement/detection/alert_manager.py`
- `non_movement/main.py`
- `non_movement/config.yaml`
- `non_movement/requirements.txt`

---

### 5. **STUDENT_GUIDE_05_FALL_DETECTION.md**
**What it covers:**
- Building fall detection project
- Fall detector algorithm
- Position analysis
- Immediate alerts
- Main application

**Time needed:** 3-4 hours

**Key files to create:**
- `fall_detection/detection/fall_detector.py`
- `fall_detection/detection/pose_analyzer.py`
- `fall_detection/detection/alert_manager.py`
- `fall_detection/main.py`
- `fall_detection/config.yaml`
- `fall_detection/requirements.txt`

---

### 6. **STUDENT_GUIDE_06_TESTING.md**
**What it covers:**
- Testing shared library
- Testing both projects
- Integration testing
- Performance testing
- Error handling

**Time needed:** 2-3 hours

**What to test:**
- All components work
- Projects run correctly
- Alerts send properly
- Error handling works

---

### 7. **STUDENT_GUIDE_07_RASPBERRY_PI.md**
**What it covers:**
- Setting up Raspberry Pi OS
- Installing dependencies
- Connecting camera
- Deploying code
- Testing on real hardware

**Time needed:** 2-3 hours

**Prerequisites:**
- Raspberry Pi 5
- Camera Module
- All code completed and tested

---

## 📖 How to Use These Guides

1. **Read Overview first** - Understand what you're building
2. **Follow in order** - Each guide builds on the previous
3. **Don't skip steps** - Each part is important
4. **Test as you go** - Don't wait until the end
5. **Ask questions** - If stuck, ask for help

---

## ⏱️ Estimated Total Time

- Setup: 1 hour
- Shared library: 4-6 hours
- Non-movement project: 3-4 hours
- Fall detection project: 3-4 hours
- Testing: 2-3 hours
- Raspberry Pi deployment: 2-3 hours

**Total: 15-21 hours** (spread over multiple sessions)

---

## 🎯 Learning Objectives

By the end, you'll understand:
- ✅ Python object-oriented programming
- ✅ Project structure and organization
- ✅ Working with cameras and image processing
- ✅ Building alert systems
- ✅ Configuration management
- ✅ Testing strategies
- ✅ Raspberry Pi development

---

## 📚 Reference Links

**Python:**
- Official docs: https://docs.python.org/3/
- Tutorial: https://docs.python.org/3/tutorial/

**Packages:**
- PyYAML: https://pyyaml.org/
- OpenCV: https://opencv-python-tutroals.readthedocs.io/
- NumPy: https://numpy.org/doc/
- Requests: https://requests.readthedocs.io/

**Raspberry Pi:**
- Official docs: https://www.raspberrypi.com/documentation/
- Camera: https://www.raspberrypi.com/documentation/computers/camera_software.html
- Picamera2: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

**Troubleshooting:**
- **FAQ_TROUBLESHOOTING.md** - Comprehensive troubleshooting guide with all common issues and solutions
- **references/FREE_SERVICES_SETUP.md** - How to set up ThingSpeak and Discord for free
- **references/MAC_BUILT_IN_SCANNER.md** - Using Mac's built-in Terminal commands to find Raspberry Pi on network
- **references/FIND_PI_NOW.md** - Quick methods to find your Pi's IP address

---

## 💡 Tips for Success

1. **Read carefully** - Don't skim, understand each step
2. **Code along** - Type code yourself, don't copy-paste
3. **Test frequently** - Test after each major component
4. **Use references** - Check documentation when needed
5. **Take breaks** - Don't rush, quality over speed
6. **Ask questions** - Better to ask than guess wrong

---

## 🚀 Ready to Start?

Begin with **STUDENT_GUIDE_01_OVERVIEW.md**

Good luck! You've got this! 💪

---

*These guides are designed to be followed step-by-step. Take your time and understand each part before moving on.*
