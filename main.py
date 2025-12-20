"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

#AUTHOR: 
#DATE:

#import libraries
import os
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2
import math
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless systems
import matplotlib.pyplot as plt

#VARIABLES
# NOTE: Configure these values before running the program
THRESHOLD = 2      #Any desired value from the accelerometer (e.g., 2.0 for shake detection)
GRAV_ACCEL = 9.8
REPO_PATH = "."     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "images"   #Your image folder path in your GitHub repo: ex. /Images
GRAPHS_PATH = "graphs"   #Your graphs folder path in your GitHub repo

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images and graphs to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(os.path.join(REPO_PATH, FOLDER_PATH))
        repo.git.add(os.path.join(REPO_PATH, GRAPHS_PATH))
        repo.index.commit('New Photo and Graph')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except Exception as e:
        print(f'Couldn\'t upload to git: {e}')


def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = os.path.join(REPO_PATH, FOLDER_PATH, f'{name}{t}.jpg')
    return imgname


def save_acceleration_graph(timestamps, accel_x, accel_y, accel_z, accel_mag):
    """
    Generates and saves a matplotlib graph of acceleration data.
    
    Parameters:
        timestamps (list): List of timestamps for each acceleration reading
        accel_x (list): X-axis acceleration values
        accel_y (list): Y-axis acceleration values
        accel_z (list): Z-axis acceleration values
        accel_mag (list): Magnitude of acceleration values
    """
    if not timestamps:
        print("No acceleration data to plot")
        return
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot individual acceleration components
    ax1.plot(timestamps, accel_x, label='X-axis', alpha=0.7)
    ax1.plot(timestamps, accel_y, label='Y-axis', alpha=0.7)
    ax1.plot(timestamps, accel_z, label='Z-axis', alpha=0.7)
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Acceleration (m/s²)')
    ax1.set_title('Acceleration Components Over Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot acceleration magnitude
    ax2.plot(timestamps, accel_mag, label='Magnitude', color='purple', linewidth=2)
    ax2.axhline(y=THRESHOLD + GRAV_ACCEL, color='r', linestyle='--', label=f'Threshold ({THRESHOLD + GRAV_ACCEL:.1f} m/s²)')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Acceleration Magnitude (m/s²)')
    ax2.set_title('Acceleration Magnitude Over Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Generate filename with timestamp
    t = time.strftime("_%Y%m%d_%H%M%S")
    graph_path = os.path.join(REPO_PATH, GRAPHS_PATH, f'acceleration{t}.png')
    
    # Ensure graphs directory exists
    os.makedirs(os.path.join(REPO_PATH, GRAPHS_PATH), exist_ok=True)
    
    # Save the figure
    plt.savefig(graph_path, dpi=100, bbox_inches='tight')
    plt.close(fig)
    
    print(f'Acceleration graph saved: {graph_path}')
    return graph_path


def take_photo():
    """
    This function is complete. Takes a photo when the FlatSat is shaken.
    Also collects acceleration data and generates a graph after each session.
    """
    # Lists to store acceleration data for graphing
    # Note: Data is collected until a shake is detected, at which point
    # a graph is generated and the program continues monitoring
    timestamps = []
    accel_x_data = []
    accel_y_data = []
    accel_z_data = []
    accel_mag_data = []
    start_time = time.time()
    
    prev_x, prev_y, prev_z = accel_gyro.acceleration
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        
        # Record acceleration data for graphing
        current_time = time.time() - start_time
        accel_magnitude = math.sqrt(accelx**2 + accely**2 + accelz**2)
        timestamps.append(current_time)
        accel_x_data.append(accelx)
        accel_y_data.append(accely)
        accel_z_data.append(accelz)
        accel_mag_data.append(accel_magnitude)

        print(accelx, accely, accelz, accel_magnitude)
        # Check if any acceleration reading is above threshold
        if accel_magnitude > THRESHOLD + GRAV_ACCEL:
            # Pause to stabilize
            time.sleep(0.5)
            
            # Set name for image
            name = "FlatSat"  # First Name, Last Initial  ex. MasonM
            
            # Take photo
            imgname = img_gen(name)
            picam2.start()
            picam2.capture_file(imgname)
            picam2.stop()
            print(f'Photo saved: {imgname}')
            
            # Generate and save acceleration graph
            save_acceleration_graph(timestamps, accel_x_data, accel_y_data, accel_z_data, accel_mag_data)
            
            # Push photo to GitHub
            git_push()
            while True:
                ax, ay, az = accel_gyro.acceleration
                current_mag = math.sqrt(ax**2 + ay**2 + az**2)
                print(current_mag)
                if current_mag < THRESHOLD + GRAV_ACCEL:
                    break
                time.sleep(0.1)
            
            # # Debounce delay to prevent multiple photos from single shake event
            # time.sleep(1)
        
        # Pause to prevent excessive CPU usage
        time.sleep(0.1)
        prev_x, prev_y, prev_z = accelx, accely, accelz


def main():
    take_photo()


if __name__ == '__main__':
    main()