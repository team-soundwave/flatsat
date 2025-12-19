#AUTHOR: 
#DATE:

#import libraries
import os
import time
import random
import cv2
from git import Repo

#VARIABLES
# NOTE: Configure these values before running the program
THRESHOLD = 5.0      # Increased threshold for random simulation
REPO_PATH = "."     #Your github repo path
FOLDER_PATH = "images"   #Your image folder path

# Mocking the sensors and camera setup
print("Initializing MacBook Webcam...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

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
        repo.index.commit('New Photo from Mac')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except Exception as e:
        print(f'Couldn\'t upload to git: {e}')


def img_gen(name):
    """
    This function is complete. Generates a new image name.
    """
    t = time.strftime("_%H%M%S")
    imgname = os.path.join(REPO_PATH, FOLDER_PATH, f'{name}{t}.jpg')
    return imgname


def take_photo():
    """
    Simulates shaking detection and takes a photo using the webcam.
    """
    print("Starting monitoring loop... (Press Ctrl+C to stop)")
    try:
        while True:
            # Simulate accelerometer data
            # mostly low numbers, occasionally a "shake"
            accelx = random.uniform(0, 1)
            accely = random.uniform(0, 1)
            accelz = random.uniform(0, 1)

            # Randomly trigger a "shake"
            if random.random() < 0.05: # 5% chance per loop
                accelx = THRESHOLD + 1

            # Check if any acceleration reading is above threshold
            if abs(accelx) > THRESHOLD or abs(accely) > THRESHOLD or abs(accelz) > THRESHOLD:
                print("Shake detected!")
                # Pause to stabilize
                time.sleep(0.5)
                
                # Set name for image
                name = "FlatSat_Mac" 
                
                # Take photo
                imgname = img_gen(name)
                
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(imgname, frame)
                    print(f'Photo saved: {imgname}')
                    
                    # Push photo to GitHub
                    git_push()
                else:
                    print("Failed to capture image")
                
                # Debounce delay
                time.sleep(2.0)
            
            # Pause to prevent excessive CPU usage
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("\nExiting and releasing camera.")


def main():
    take_photo()


if __name__ == '__main__':
    main()
