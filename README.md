# IVAD – Long period of non-movement detection

Detects long periods without motion (e.g. person down, no activity) using **Raspberry Pi 5** + camera module + Pi HAT. You can **develop and test on Windows** (with a webcam), then deploy the same code on the Pi.

## Build and run on Windows

1. **Create a virtual environment** (recommended):
   ```powershell
   cd c:\Users\ellen\OneDrive\Documents\IVAD
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies** (OpenCV for webcam):
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the app** (uses your default webcam):
   ```powershell
   python -m src.main
   ```
   - Optional: `--stillness-seconds 30` (alert after 30 s of no motion), `--test-camera` (use second webcam).

On Windows the app uses **OpenCV** and your webcam. Alerts are printed to the console (no GPIO).

## Deploy on Raspberry Pi 5 (camera + Pi HAT)

1. **Copy the project** to the Pi (e.g. `IVAD` folder via USB, SCP, or Git).

2. **Enable the camera** and install Pi packages:
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   sudo apt update
   sudo apt install -y python3-picamera2 python3-opencv python3-venv
   # Optional: for Pi HAT buzzer/LED
   sudo apt install -y python3-rpi.gpio
   ```

3. **On the Pi**, create a venv and install:
   ```bash
   cd /path/to/IVAD
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run on the Pi** (uses Picamera2 and, if you use it, GPIO):
   ```bash
   python3 -m src.main --stillness-seconds 60 --gpio --gpio-pin 17
   ```
   Use `--gpio-pin` to match the pin your Pi HAT uses for buzzer or LED.

## Project layout

- `src/detector.py` – Motion detection and main loop (Picamera2 on Pi, OpenCV on Windows).
- `src/alerts.py` – Alert handlers (console on Windows, optional GPIO on Pi).
- `src/main.py` – CLI entry point.
- `config.example.yaml` – Example config (optional; CLI args take precedence).
- `requirements.txt` – Python deps (OpenCV on both; picamera2/GPIO only on Pi).

## Summary

| Where        | Camera              | Alerts        |
|-------------|---------------------|---------------|
| **Windows** | Webcam (OpenCV)     | Console only  |
| **Raspberry Pi 5** | Camera module (Picamera2) | Console + optional GPIO (Pi HAT) |

You can edit and run the app on your Windows machine, then copy the same `IVAD` folder to the Pi and run it there with `--gpio` for the Pi HAT.
