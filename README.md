# FlatSat Challenge

This project captures photos on a Raspberry Pi when a shake is detected via an IMU, then automatically pushes the images to GitHub.

## Requirements

- Raspberry Pi with Camera Module
- LSM6DSOX Accelerometer/Gyro
- LIS3MDL Magnetometer
- [uv](https://docs.astral.sh/uv/) installed on the Pi

## Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:team-soundwave/flatsat.git
   cd flatsat
   ```

2. **Configure GitHub Access:**
   Ensure your Pi has SSH keys configured or a PAT set up so that `git push` works without manual interaction.

3. **Install Dependencies:**
   ```bash
   uv sync
   ```

## Usage

Run the main script:
```bash
uv run main.py
```

The script will:
1. Monitor the IMU for acceleration exceeding the `THRESHOLD`.
2. Capture a photo and save it to the `images/` directory.
3. Commit and push the new photo to the `origin` remote.
