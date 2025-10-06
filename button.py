import RPi.GPIO as GPIO
import subprocess
from time import sleep

BUTTON_PIN = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def run_blob_detect():
    print("Launching Blob Detect in terminal...")
    subprocess.run(["python3", "/home/iap/Desktop/Blob_Detect.py"])

print("Waiting for button press...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            run_blob_detect()
            sleep(0.5)
        sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting manually...")
finally:
    GPIO.cleanup()
