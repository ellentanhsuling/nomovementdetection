# Student Build Guide - Overview

## Welcome! 👋

This guide will help you build an elderly monitoring system step-by-step. You'll create **two separate projects** that share common code.

---

## What You're Building

You'll build **two projects**:

1. **Non-Movement Detection** - Detects when someone hasn't moved for a long time (30+ minutes)
2. **Fall Detection** - Detects when someone falls down immediately

Both projects use a **Raspberry Pi 5** and **Camera Module**.

**Optional (advanced / competition path):** A **Raspberry Pi AI HAT+** with a **Hailo-8L** (or Hailo-8) NPU runs pose-style models on-device so fall detection can use real body posture instead of motion-only guesses. The repo includes a **mock** inference path for your laptop and a **Hailo stub** to fill in on the Pi (`shared/inference/`).

---

## Project Structure (What You'll Create)

```
raspberry/
├── shared/              # Code used by BOTH projects
│   ├── sensors/         # Camera code
│   ├── inference/       # Pose backends: mock (dev) + Hailo stub (Pi + AI HAT+)
│   ├── alerts/          # Email/SMS/webhook alerts
│   ├── utils/           # Helper functions
│   └── base/            # Base class
│
├── non_movement/        # Project 1: Long inactivity detection
│   ├── detection/       # Your detection algorithm
│   └── main.py          # Start here to run
│
└── fall_detection/      # Project 2: Immediate fall detection
    ├── detection/       # Your detection algorithm
    └── main.py          # Start here to run
```

---

## Build Order (Follow These Guides in Order)

1. **STUDENT_GUIDE_02_SETUP.md** - Set up your computer and install tools
2. **STUDENT_GUIDE_03_SHARED_LIBRARY.md** - Build the shared code (used by both projects)
3. **STUDENT_GUIDE_04_NON_MOVEMENT.md** - Build Project 1: Non-Movement Detection
4. **STUDENT_GUIDE_05_FALL_DETECTION.md** - Build Project 2: Fall Detection
5. **STUDENT_GUIDE_06_TESTING.md** - Test everything works
6. **STUDENT_GUIDE_07_RASPBERRY_PI.md** - Deploy to Raspberry Pi

---

## Important Concepts

### Why Two Projects?

- **Different purposes**: One detects long inactivity, one detects immediate falls
- **Different algorithms**: They work differently
- **Can't run together**: Camera can only be used by one program at a time

### Why Shared Library?

- **Avoid duplication**: Don't write the same code twice
- **Easier maintenance**: Fix bugs in one place
- **Clean structure**: Organized and professional

---

## What You'll Learn

✅ Python programming
✅ Object-oriented programming (classes)
✅ Working with cameras
✅ Sending alerts (email, SMS)
✅ Configuration files (YAML)
✅ Project structure and organization
✅ Raspberry Pi development
✅ (Optional) Edge AI: config-driven pose inference and Hailo on Pi

---

## Prerequisites

- Basic Python knowledge
- A computer (Mac, Windows, or Linux)
- Internet connection
- (Later) Raspberry Pi 5 + Camera Module
- (Optional) Raspberry Pi **AI HAT+** with **Hailo-8L** for accelerated pose / fall detection on the device

---

## Getting Help

- **Python Documentation**: https://docs.python.org/3/
- **OpenCV (camera)**: https://opencv-python-tutroals.readthedocs.io/
- **PyYAML (config files)**: https://pyyaml.org/wiki/PyYAMLDocumentation
- **Raspberry Pi Docs**: https://www.raspberrypi.com/documentation/

---

## Ready to Start?

Go to **STUDENT_GUIDE_02_SETUP.md** to begin!

---

*Take your time. Read each step carefully. Ask questions if you're stuck!*
