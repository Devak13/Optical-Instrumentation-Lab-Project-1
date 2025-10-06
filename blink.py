import RPi.GPIO as GPIO
from time import sleep
from picamera2 import Picamera2, Preview
from libcamera import Transform

def image_capture(file_path):
	picam = Picamera2()

	config = picam.create_preview_configuration(main={"size": (2592,1944)})
	config["transform"] = Transform(hflip = 1, vflip = 1)
	picam.configure(config)
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(18, GPIO.OUT)
	i = 0	#variable to run below code only once
	while i==0:
		GPIO.output(18,GPIO.HIGH)
		picam.start_preview(Preview.QTGL, transform = Transform(vflip=1,hflip = 1))
		
		picam.start()
		picam.set_controls({"AeEnable": False, "ExposureTime": 1000, "AnalogueGain":2})
		picam.capture_file(file_path)

		picam.close()
		GPIO.output(18, GPIO.LOW)
		i+=1

image_capture("/home/iap/Pictures/photo1.jpg")
