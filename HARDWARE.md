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

## Option 4: Arduino UNO Q (Strong Contender)

> **Source:** [Arduino UNO Q hardware docs](https://docs.arduino.cc/hardware/uno-q/) and [product page](https://www.arduino.cc/product-uno-q/)

The Arduino UNO Q is a **completely different class of board** from the classic Arduino Uno (R3/R4). It is a full Linux single-board computer with AI capabilities, built around a Qualcomm Dragonwing processor. Do not confuse it with the classic Uno — it has far more in common with a Raspberry Pi.

| Spec | Value |
|---|---|
| MPU | Qualcomm Dragonwing QRB2210: Quad-core Arm Cortex-A53 @ 2.0 GHz |
| GPU | Adreno 702 @ 845 MHz (3D graphics accelerator) |
| ISP | 2x Image Signal Processor (13 MP + 13 MP or 25 MP) @ 30 fps |
| MCU | STM32U585 Arm Cortex-M33 @ 160 MHz (for real-time Arduino sketches via Zephyr OS) |
| RAM | 2 GB or 4 GB LPDDR4 (two SKU variants) |
| Storage | 16 GB or 32 GB eMMC (no SD card wear issues) |
| Camera | USB cameras via USB-C dongle; dual MIPI-CSI interfaces via bottom JMEDIA header + carrier board |
| GPIO | UNO-compatible headers (3.3V MCU, 5V tolerant) + Qwiic I2C connector |
| OS | Debian Linux (upstream support) on MPU; Zephyr OS on MCU |
| Connectivity | Wi-Fi 5 dual-band (2.4/5 GHz), Bluetooth 5.1 |
| Development | Arduino App Lab (Python + Arduino sketches + AI models), Arduino IDE 2.0+ |
| Price | Not yet listed at time of writing — check the [Arduino Store](https://www.arduino.cc/product-uno-q/) |

### Why it fits IVAD

- **Runs Debian Linux with Python support.** The MPU side runs a full Debian environment. Python 3 and OpenCV can be installed and used natively, just like on a Raspberry Pi.
- **AI and machine vision built in.** Arduino's own product page describes it as a platform for "AI-powered vision and sound solutions." The Qualcomm QRB2210 includes integrated AI acceleration, a GPU, and dual ISPs (Image Signal Processors) designed for camera processing — making it purpose-built for projects like IVAD.
- **Camera support.** Supports USB cameras via a USB-C dongle, and high-resolution MIPI-CSI cameras via the bottom high-speed JMEDIA connector (requires a carrier board). IVAD's OpenCV-based USB camera path would work without code changes.
- **Dual-processor architecture.** The Linux MPU handles heavy processing (OpenCV, AI models), while the STM32 MCU can handle real-time GPIO tasks (buzzer, LED alerts) via Arduino sketches. They communicate through a built-in RPC bridge. This is actually a cleaner separation of concerns than a Pi, where GPIO and processing share the same OS.
- **Arduino App Lab.** Comes pre-loaded with Arduino App Lab, which lets you combine Python scripts, Arduino sketches, and containerized AI models in a single workflow — interesting for future IVAD features like neural-network-based fall detection.
- **eMMC storage.** Unlike Raspberry Pi's microSD cards, eMMC is more reliable for always-on deployments (no SD card corruption from power loss).
- **Familiar UNO form factor.** Compatible with existing Arduino shields and the wider Arduino ecosystem.

### What would need to change in IVAD

- **Camera backend.** IVAD's Picamera2 code path is Raspberry Pi-specific and would not work. However, the OpenCV (`cv2.VideoCapture`) code path — which IVAD already has for Windows development — should work with a USB camera on the UNO Q's Debian Linux out of the box.
- **GPIO alerts.** The `RPi.GPIO` library is Pi-specific. On the UNO Q, GPIO alerts would be handled by the STM32 MCU running an Arduino sketch, with the Linux side sending commands via the RPC bridge. This requires writing a small Arduino sketch for the MCU side and modifying `alerts.py` to communicate over serial/RPC instead of RPi.GPIO.
- **No Picamera2.** If you want to use a MIPI-CSI camera (for higher quality than USB), you would need to use the Qualcomm camera stack rather than Picamera2. USB cameras via OpenCV are the simpler path.

### Limitations

- **New product.** The UNO Q is a recent addition to the Arduino lineup. Community resources, tutorials, and third-party support are still growing compared to the mature Raspberry Pi ecosystem.
- **Camera requires accessories.** Unlike the Pi's simple CSI ribbon cable, MIPI-CSI cameras on the UNO Q need a carrier board connected to the bottom high-speed headers. USB cameras work with just a USB-C dongle but add bulk.
- **GPIO is indirect.** GPIO is managed by the STM32 MCU, not the Linux MPU. This adds a layer of complexity (RPC bridge) compared to the Pi's direct GPIO access from Python. However, this dual-processor design is arguably more robust for real-time alert triggering.
- **Price uncertainty.** Pricing was not available at time of research. Given the Qualcomm SoC, GPU, and eMMC, it may be priced higher than a Raspberry Pi 5.
- **Smaller ecosystem.** Far fewer community projects, tutorials, and StackOverflow answers compared to Raspberry Pi.

### Verdict

**A genuinely viable alternative to the Raspberry Pi 5 for IVAD**, especially if you value the integrated AI acceleration, eMMC reliability, and the dual-processor architecture. The OpenCV USB camera path works without code changes; GPIO alerts would need modest refactoring to use the RPC bridge instead of RPi.GPIO. If you are drawn to the Arduino ecosystem or plan to add AI/ML features, the UNO Q is worth serious consideration.

---

## Option 5: Arduino Uno R3 / R4 WiFi (Not Recommended)

> **Important:** The classic Arduino Uno (R3 and R4 WiFi) should not be confused with the Arduino UNO Q above. They are fundamentally different products.

| Spec | Arduino Uno R3 | Arduino Uno R4 WiFi |
|---|---|---|
| CPU | ATmega328P, 8-bit AVR @ 16 MHz | Renesas RA4M1, Arm Cortex-M4 @ 48 MHz |
| RAM | 2 KB SRAM | 32 KB SRAM |
| Flash | 32 KB | 256 KB |
| Camera | None | None |
| GPIO | 14 digital I/O, 6 analog inputs | 14 digital I/O, 6 analog inputs |
| OS | None (bare-metal C/C++) | None (bare-metal C/C++) |
| Connectivity | None | Wi-Fi, Bluetooth (via ESP32-S3) |
| Price | ~$25 USD (official); ~$5 for clones | ~$28 USD |

### Why they do NOT fit

1. **Cannot run Python.** IVAD is written entirely in Python. These boards run compiled C/C++ on bare metal — the entire codebase would need to be rewritten from scratch.
2. **Cannot run OpenCV.** OpenCV requires at minimum tens of megabytes of RAM and a 32-bit+ processor with an OS. The Uno R3 has 2 KB of RAM; the R4 has 32 KB. Neither can run an operating system or OpenCV.
3. **No practical camera support.** Neither board has a camera interface. Even connecting a basic camera module (e.g., OV7670) is impractical — a single 640x480 grayscale frame (307 KB) exceeds the R3's total memory by 150x and the R4's by 10x.
4. **The R4 WiFi's ESP32-S3 co-processor** handles only Wi-Fi/Bluetooth communication — it is not user-accessible for general-purpose computing or camera processing.

### What classic Arduinos ARE good for

Arduino excels at simple, real-time I/O tasks: reading sensors (PIR motion sensors, temperature), driving motors/LEDs, and low-power embedded control. If IVAD were redesigned around a **PIR sensor** instead of a camera (i.e., detecting any motion in a room without image analysis), a classic Arduino could work — but that is a fundamentally different and less capable approach (no ability to distinguish types of movement, no video evidence, no future AI extension).

### Could a classic Arduino be used as a peripheral?

Yes — in a hybrid setup, a Raspberry Pi or UNO Q could run IVAD and send a signal over serial/I2C to a classic Arduino that drives specialized hardware (e.g., a relay board, siren, motor). But for the core detection logic, a Linux-capable SBC is required.

### Verdict

**Not suitable as the main board for IVAD.** The project's core requirements (Python, OpenCV, camera frame processing) are fundamentally incompatible with classic Arduino Uno capabilities. If you are interested in the Arduino ecosystem, look at the **UNO Q** (Option 4) instead.

---

## Option 6: ESP32-CAM (Honorable Mention — Advanced Users)

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

## Option 7: NVIDIA Jetson Nano / Orin Nano (Future-Proofing for AI)

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

| Criteria | Pi 5 | Pi 4 | Pi Zero 2 W | UNO Q | Arduino Uno R3/R4 | ESP32-CAM | Jetson Orin Nano |
|---|---|---|---|---|---|---|---|
| Runs IVAD as-is | Yes | Yes | Yes | Mostly (USB cam path) | No | No | Yes |
| Python + OpenCV | Yes | Yes | Yes | Yes | No | No | Yes |
| Camera support | Excellent | Excellent | Good | Good (USB + MIPI-CSI via carrier) | None | Built-in | Excellent |
| GPIO for alerts | 40-pin (direct) | 40-pin (direct) | 40-pin (direct) | Via MCU + RPC bridge | 14 digital | Limited | 40-pin (direct) |
| Wi-Fi | Built-in | Built-in | Built-in | Built-in (Wi-Fi 5) | R3: No / R4: Yes | Built-in | Optional |
| AI/ML acceleration | Moderate | Moderate | Limited | Built-in (Qualcomm AI + GPU) | No | No | Excellent (NVIDIA GPU) |
| Power consumption | ~5–10W | ~4–8W | ~1–2W | TBD (likely ~3–7W) | ~0.2W | ~0.3W | ~7–15W |
| Storage | microSD | microSD | microSD | 16/32 GB eMMC | 32–256 KB flash | 4 MB flash | microSD/NVMe |
| Price (board) | ~$60–80 | ~$35–55 | ~$15 | TBD (check Arduino Store) | ~$5–28 | ~$8 | ~$199–499 |
| Code changes needed | None | None | None (maybe config) | Minor (GPIO refactor) | Full rewrite (C++) | Full rewrite (C++) | None |
| Ecosystem maturity | Excellent | Excellent | Good | New (growing) | Excellent (but irrelevant for IVAD) | Good | Good |

---

## Recommendation

**For IVAD as it exists today, the Raspberry Pi 5 remains the top recommendation.** It runs the codebase without modification, has excellent camera support via Picamera2, ample processing power, and a rich GPIO/HAT ecosystem for alerts. The Raspberry Pi 4 is a fine budget alternative with identical compatibility.

**The Arduino UNO Q is a strong second choice** — and a genuine surprise if you were expecting a classic Arduino. It runs Debian Linux, supports Python and OpenCV, has built-in AI acceleration and dual ISPs for camera processing, and includes eMMC storage (more reliable than SD cards for always-on use). The trade-offs are that GPIO requires going through the MCU's RPC bridge (a modest code change to `alerts.py`), MIPI-CSI cameras need a carrier board, and the ecosystem is still young. If you are drawn to the Arduino platform or plan to add AI/ML features, the UNO Q deserves serious consideration — check the [Arduino Store](https://www.arduino.cc/product-uno-q/) for current pricing and availability.

**The classic Arduino Uno (R3 / R4 WiFi) is not suitable** for this project — it cannot run Python, OpenCV, or process camera frames. It should not be confused with the UNO Q.

If budget and size are the top priority, the **Raspberry Pi Zero 2 W** runs the code as-is for a fraction of the cost, with only minor performance trade-offs.

If you plan to add heavy AI/ML features in the future (pose estimation, fall detection via neural networks), consider the **NVIDIA Jetson Orin Nano**, though it is significantly more expensive.
