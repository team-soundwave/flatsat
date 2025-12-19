# FlatSat Challenge (Mac Test Branch)

This branch (`mac-test`) is designed for testing the FlatSat logic on a macOS laptop. 
It mocks the IMU (accelerometer) with random data and uses the laptop's webcam instead of the Raspberry Pi camera.

## Requirements

- macOS
- Webcam
- [uv](https://docs.astral.sh/uv/)

## Setup & Usage

1. **Install Dependencies:**
   ```bash
   uv sync
   ```

2. **Run the script:**
   ```bash
   uv run main.py
   ```

3. **What to expect:**
   - The script will start a loop.
   - It randomly simulates "accelerometer" readings.
   - About 5% of the time, it will trigger a "shake".
   - Your webcam will turn on, take a picture, save it to `images/`, and attempt to push it to GitHub.
   - **Press Ctrl+C to stop.**