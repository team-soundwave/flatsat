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

#VARIABLES
# NOTE: Configure these values before running the program
THRESHOLD = 2      #Any desired value from the accelerometer (e.g., 2.0 for shake detection)
GRAV_ACCEL = 9.8
REPO_PATH = "."     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "images"   #Your image folder path in your GitHub repo: ex. /Images

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(os.path.join(REPO_PATH, FOLDER_PATH))
        repo.index.commit('New Photo')
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


def take_photo():
    """
    This function is complete. Takes a photo when the FlatSat is shaken.
    """
    prev_x, prev_y, prev_z = accel_gyro.acceleration
    prev_x, prev_y, prev_z = accel_gyro.acceleration
    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        diffx, diffy, diffz = accelx - prev_x, accely - prev_y, accelz - prev_z

        print(accelx, accely, accelz, math.sqrt(accelx**2 + accely**2 + accelz**2))
        # Check if any acceleration reading is above threshold
        if math.sqrt(accelx**2 + accely**2 + accelz**2) > THRESHOLD + GRAV_ACCEL:
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