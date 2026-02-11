# Hardware Selection Guide

This document evaluates hardware options for the **IVAD non-movement detection system**. IVAD captures camera frames, runs OpenCV-based motion analysis (grayscale conversion, Gaussian blur, frame differencing, contour detection), and triggers alerts when no movement is detected for a configurable period.

---

## Project Requirements at a Glance

| Requirement | Detail |
|---|---|
| **Camera input** | Continuous video frames (640x480 minimum) |
| **Image processing** | OpenCV: grayscale, Gaussian blur, absdiff, threshold, contour finding — every 1 second |
| **Runtime** | Python 3 with OpenCV (`cv2`) and optionally `picamera2` |
| **Alert output** | GPIO pin (buzzer / LED via HAT or direct wiring) |
| **OS** | Linux preferred (Picamera2 support); Windows for development only |
| **Power** | Ideally low power for always-on monitoring |
| **Network (optional)** | Wi-Fi / Ethernet useful for remote alerts or SSH management |

---

## Option 1: Raspberry Pi 5 (Recommended)

| Spec | Value |
|---|---|
| CPU | Quad-core Arm Cortex-A76 @ 2.4 GHz |
| RAM | 2 / 4 / 8 GB LPDDR4X |
| Camera | MIPI CSI connector (official Camera Module 3 or V2) |
| GPIO | 40-pin header (fully compatible with Pi HATs) |
| OS | Raspberry Pi OS (Debian-based Linux) |
| Connectivity | Wi-Fi 5, Bluetooth 5.0, Gigabit Ethernet |
| Price | ~$60–$80 USD (board only) |

### Why it fits

- **Runs the IVAD codebase as-is.** Python 3, OpenCV, and Picamera2 are all fully supported with no code changes.
- **More than enough processing power.** The A76 cores handle OpenCV frame differencing at 640x480 with ease; CPU usage stays well under 20%.
- **Native camera interface.** The CSI connector with Picamera2 provides low-latency, high-quality frames with minimal CPU overhead compared to USB webcams.
- **40-pin GPIO.** Directly drives a buzzer or LED, and is compatible with a huge ecosystem of Pi HATs (e.g., Sense HAT, custom alert boards).
- **Headless-friendly.** SSH in, run IVAD in a `tmux`/`systemd` service, and leave it running 24/7.
- **Expandable.** If IVAD ever grows to include AI/ML-based pose estimation (e.g., detecting a person lying on the floor), the Pi 5 has enough horsepower and can use a Coral USB accelerator.

### Limitations

- Higher power draw (~5W idle, ~10W under load) compared to microcontrollers — needs a USB-C power supply.
- Full Linux OS means longer boot time (~15–25 seconds) and OS maintenance (updates, SD card wear).
- Overkill if the only task is simple frame differencing — but the headroom is useful for future features.

### Recommended accessories

- Raspberry Pi Camera Module 3 (or V2)
- Pi HAT with buzzer/LED, or a simple breadboard circuit on the GPIO pins
- 27W USB-C power supply (official)
- MicroSD card (32 GB+ recommended) or NVMe SSD via HAT for reliability

---

## Option 2: Raspberry Pi 4 Model B (Budget Alternative)

| Spec | Value |
|---|---|
| CPU | Quad-core Arm Cortex-A72 @ 1.8 GHz |
| RAM | 2 / 4 / 8 GB LPDDR4 |
| Camera | MIPI CSI connector |
| GPIO | 40-pin header |
| Price | ~$35–$55 USD |

### Why consider it

- Roughly 30% cheaper than the Pi 5 and still comfortably runs the IVAD codebase.
- Same 40-pin GPIO header and camera connector — identical wiring and HAT compatibility.
- Well-tested with Picamera2 and OpenCV.

### Limitations

- About 40% slower CPU than the Pi 5 — not an issue for IVAD today, but less headroom for future AI/ML features.
- USB 2.0 for the camera port (CSI is fine, but USB cameras are slower than on Pi 5's USB 3.0).

### Verdict

A solid pick if you already own one or want to save money. The code runs without any changes.

---

## Option 3: Raspberry Pi Zero 2 W (Compact / Low-Power)

| Spec | Value |
|---|---|
| CPU | Quad-core Arm Cortex-A53 @ 1.0 GHz |
| RAM | 512 MB LPDDR2 |
| Camera | MIPI CSI connector (mini ribbon cable) |
| GPIO | 40-pin header (unpopulated — needs soldering or hammer header) |
| Price | ~$15 USD |

### Why consider it

- Very small form factor — easy to mount in a room or enclosure.
- Low power (~1–2W) — suitable for always-on battery or PoE setups.
- Runs Raspberry Pi OS, Python 3, OpenCV, and Picamera2.
- Price is hard to beat.

### Limitations

- Only 512 MB RAM — OpenCV at 640x480 works but leaves little headroom.
- Single-core effective performance is much lower; frame processing will be slower (~2–3 fps realistically with OpenCV).
- No Ethernet (Wi-Fi only); slower I/O overall.
- The code runs as-is, but you may want to reduce resolution or increase `check_interval_seconds` to avoid lag.

### Verdict

Best choice for a tiny, low-power deployment where cost matters most. Requires no code changes but may need config tuning for performance.

---

## Option 4: Arduino Uno (Not Recommended)

| Spec | Value |
|---|---|
| CPU | ATmega328P, 8-bit AVR @ 16 MHz |
| RAM | 2 KB SRAM, 32 KB flash |
| Camera | None built-in; limited external options (e.g., OV7670 — raw, no library support for processing) |
| GPIO | 14 digital I/O, 6 analog inputs |
| OS | None (bare-metal, programmed in C/C++ via Arduino IDE) |
| Price | ~$25 USD (official); ~$5 for clones |

### Why it does NOT fit

1. **Cannot run Python.** IVAD is written entirely in Python. The Arduino Uno runs compiled C/C++ on bare metal — the entire codebase would need to be rewritten from scratch.
2. **Cannot run OpenCV.** OpenCV requires at minimum tens of megabytes of RAM and a 32-bit+ processor. The Uno has 2 KB of RAM and an 8-bit CPU — image processing is not feasible.
3. **No practical camera support.** While an OV7670 camera module can physically connect to an Uno, capturing and processing even a single 640x480 frame exceeds the Uno's memory by orders of magnitude (a single 640x480 grayscale frame = 307 KB; the Uno has 2 KB).
4. **No networking.** No built-in Wi-Fi or Ethernet (shields exist but add cost and complexity).

### What Arduino IS good for

Arduino excels at simple, real-time I/O tasks: reading sensors (PIR motion sensors, temperature), driving motors/LEDs, and low-power embedded control. If IVAD were redesigned around a **PIR sensor** instead of a camera (i.e., detecting any motion in a room without image analysis), an Arduino could work — but that is a fundamentally different and less capable approach (no ability to distinguish types of movement, no video evidence, no future AI extension).

### Could Arduino be used as a peripheral?

Yes — in a hybrid setup, a Raspberry Pi could run IVAD and send a signal over serial/I2C to an Arduino that drives specialized hardware (e.g., a relay board, siren, motor). But for the core detection logic, a Pi (or equivalent SBC) is required.

### Verdict

**Not suitable as the main board for IVAD.** The project's core requirements (Python, OpenCV, camera frame processing) are fundamentally incompatible with the Arduino Uno's capabilities.

---

## Option 5: ESP32-CAM (Honorable Mention — Advanced Users)

| Spec | Value |
|---|---|
| CPU | Dual-core Xtensa LX6 @ 240 MHz |
| RAM | 520 KB SRAM + 4 MB PSRAM |
| Camera | OV2640 (built-in, 2 MP) |
| GPIO | Limited (some shared with camera/SD) |
| Price | ~$6–$10 USD |

### Why consider it

- Extremely cheap and has a built-in camera.
- Built-in Wi-Fi — can stream frames or send alerts over the network.
- Very low power — can run on batteries.

### Limitations

- **Cannot run Python or OpenCV natively.** Firmware is written in C/C++ (Arduino framework or ESP-IDF). The entire IVAD codebase would need to be rewritten.
- Limited RAM makes sophisticated image processing difficult (though basic frame differencing is possible in C with reduced resolution).
- MicroPython exists for ESP32 but OpenCV is not available; you would need to implement motion detection from scratch.
- GPIO pins are limited and shared with camera functions.

### Verdict

A fascinating option for advanced users willing to rewrite the detection logic in C/C++. Not a drop-in replacement — requires a complete reimplementation. Best suited for ultra-low-cost, battery-powered deployments where minimal motion detection is sufficient.

---

## Option 6: NVIDIA Jetson Nano / Orin Nano (Future-Proofing for AI)

| Spec | Jetson Orin Nano |
|---|---|
| CPU | 6-core Arm Cortex-A78AE |
| GPU | 1024-core NVIDIA Ampere |
| RAM | 4 / 8 GB LPDDR5 |
| Camera | MIPI CSI (up to 4 cameras) |
| GPIO | 40-pin header (Pi-compatible) |
| Price | ~$199–$499 USD |

### Why consider it

- If you plan to add **AI-based detection** (e.g., pose estimation to detect a person lying on the floor, or object detection to distinguish people from pets), the GPU makes neural network inference fast and efficient.
- Pi-compatible 40-pin GPIO header — Pi HATs may work.
- Runs Linux (JetPack / Ubuntu), Python, and OpenCV natively.

### Limitations

- Significantly more expensive than a Raspberry Pi.
- Higher power consumption (~7–15W).
- Complete overkill for simple frame differencing — only justified if AI/ML features are planned.

### Verdict

Only worth it if IVAD will evolve to include neural-network-based detection. For the current frame-differencing approach, a Raspberry Pi is far more cost-effective.

---

## Comparison Summary

| Criteria | Pi 5 | Pi 4 | Pi Zero 2 W | Arduino Uno | ESP32-CAM | Jetson Orin Nano |
|---|---|---|---|---|---|---|
| Runs IVAD as-is | Yes | Yes | Yes | No | No | Yes |
| Python + OpenCV | Yes | Yes | Yes | No | No | Yes |
| Camera support | Excellent | Excellent | Good | Poor | Built-in | Excellent |
| GPIO for alerts | 40-pin | 40-pin | 40-pin | 14 digital | Limited | 40-pin |
| Wi-Fi | Built-in | Built-in | Built-in | No | Built-in | Optional |
| Power consumption | ~5–10W | ~4–8W | ~1–2W | ~0.2W | ~0.3W | ~7–15W |
| Price (board) | ~$60–80 | ~$35–55 | ~$15 | ~$25 | ~$8 | ~$199–499 |
| Code changes needed | None | None | None (maybe config) | Full rewrite (C++) | Full rewrite (C++) | None |
| Future AI/ML ready | Moderate | Moderate | Limited | No | No | Excellent |

---

## Recommendation

**For IVAD as it exists today, the Raspberry Pi 5 is the best choice.** It runs the codebase without modification, has excellent camera support, ample processing power, and a rich GPIO/HAT ecosystem for alerts. The Raspberry Pi 4 is a fine budget alternative with identical compatibility.

The **Arduino Uno is not suitable** for this project — it cannot run Python, OpenCV, or process camera frames. It could only serve as a peripheral to an SBC that handles the actual detection.

If budget and size are the top priority, the **Raspberry Pi Zero 2 W** runs the code as-is for a fraction of the cost, with only minor performance trade-offs.

If you plan to add AI/ML features in the future (pose estimation, fall detection via neural networks), consider the **NVIDIA Jetson Orin Nano**, though it is significantly more expensive.
