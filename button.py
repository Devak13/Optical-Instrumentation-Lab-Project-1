import RPi.GPIO as GPIO
import subprocess
from time import sleep

# GPIO setup
BUTTON_PIN = 16  # You can change this pin number
GPIO.setmode(GPIO.BOARD)  # Using physical pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Internal pull-up

print("Waiting for button press...")

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        if button_state == GPIO.LOW:  # Button pressed (pulled to GND)
            print("Button pressed! Running Blob detect.py...")
            
            # Run your Blob detect.py script
            subprocess.run(["python3", "/home/iap/Desktop/Blob detect.py"])

            # Small debounce delay
            sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()
