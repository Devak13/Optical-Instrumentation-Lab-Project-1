from PIL import Image, ImageDraw
import numpy as np
import math
from time import sleep
import blink as ub    #invoking function file

# Camera and geometry setup
ifovx = 0.0211032992                           # radians per pixel (horizontal IFOV) with 54.6997 degrees 30.0cm field and distance 29.0cm
xc = 82.5                                      # distance between camera and laser
xR = 2592                                      # image width
yR = 1944                                      # image height
angle = math.degrees(math.atan(xc/290))        #Angle between laser and camera    
tan = math.tan(math.radians(angle))            #tan of angle between laser and camera
yc = xc / tan                                  #Distance at which laser hits camera center in reference plane
y1=yc                                          

# Capture image of the screen
image_path = "/home/iap/Pictures/photo1.jpg"  
ub.image_capture(image_path)

# Load image as numpy array and saving image with rgb values
image = Image.open(image_path).convert("RGB")         
width, height = image.size
print(f"width is {width} and height is {height}")

np_img = np.array(image)  # shape: (height, width, 3)

# Define region of interest (ROI) around image center
x_min, x_max = int(xR/2 - 1000), int(xR/2 + 400)
y_min, y_max = int(yR/2 - 100), int(yR/2 + 300)

roi = np_img[y_min:y_max, x_min:x_max, :]   # sub-image

# Split rgb channels
red   = roi[:, :, 0].astype(np.int16)
green = roi[:, :, 1].astype(np.int16)
blue  = roi[:, :, 2].astype(np.int16)

# Threshold mask for "red" pixels
mask = (red > 80) & (red > 1.5*green) & (red > 1.5*blue)

ys, xs = np.where(mask)

if len(xs) == 0:
    print("Outside of region or not reading any red pixel")
    print("Waiting for button press...")

else:
    # Compute centroid of detected blob
    mean_x = int(xs.mean()) + x_min
    mean_y = int(ys.mean()) + y_min

    # Geometry calculations
    xoffset_pixel = xR/2 - mean_x
    yoffset_pixel = yR/2 - mean_y
    xoffset_angle = xoffset_pixel * ifovx   

    """print(f"offset angle (rad): {xoffset_angle}")
    print(f"offset pixels: {xoffset_pixel}")"""

    if mean_x < xR/2:
        y = (yc * xc)/(xc + yc*math.tan(math.radians(xoffset_angle)))
    else:
        y = (yc * xc)/(xc - yc*math.tan(math.radians(xoffset_angle)))
    print(f"Object is at distance of {y}")
    """print(f"laser detected at ({mean_x},{mean_y})")"""
    
     # Draw crosshair at centroid
    processed_image = image.copy()
    draw = ImageDraw.Draw(processed_image)
    draw.line((mean_x-5, mean_y, mean_x+5, mean_y), fill=(0,255,0), width=2)
    draw.line((mean_x, mean_y-5, mean_x, mean_y+5), fill=(0,255,0), width=2)
    processed_image.save("/home/iap/Pictures/processed_image1.jpg")


# Capture image with obbject in front of screen

print("insert the object")
sleep(5)

image_path = "/home/iap/Pictures/photo2.jpg"
ub.image_capture(image_path)

# Load image as numpy array
image = Image.open(image_path).convert("RGB")
width, height = image.size
print(f"width is {width} and height is {height}")

np_img = np.array(image)  # shape: (height, width, 3)

# Define region of interest (ROI) around image center
x_min, x_max = int(xR/2 - 1000), int(xR/2 + 400)
y_min, y_max = int(yR/2 - 100), int(yR/2 + 300)

roi = np_img[y_min:y_max, x_min:x_max, :]   # sub-image

# Split channels
red   = roi[:, :, 0].astype(np.int16)
green = roi[:, :, 1].astype(np.int16)
blue  = roi[:, :, 2].astype(np.int16)

# Threshold mask for "red" pixels
mask = (red > 30) & (red > 1.5*green) & (red > 1.5*blue)

ys, xs = np.where(mask)

if len(xs) == 0:
    print("Outside of region or not reading any red pixel")
    print("Waiting for button press...")

else:
    # Compute centroid of detected blob
    mean_x = int(xs.mean()) + x_min
    mean_y = int(ys.mean()) + y_min

    # Geometry calculations
    xoffset_pixel = xR/2 - mean_x
    yoffset_pixel = yR/2 - mean_y
    xoffset_angle = xoffset_pixel * ifovx   
    print(f"offset angle (rad): {xoffset_angle}")
    print(f"offset pixels: {xoffset_pixel}")
    
    
    # Draw crosshair at centroid
    processed_image = image.copy()
    draw = ImageDraw.Draw(processed_image)
    draw.line((mean_x-5, mean_y, mean_x+5, mean_y), fill=(0,255,0), width=2)
    draw.line((mean_x, mean_y-5, mean_x, mean_y+5), fill=(0,255,0), width=2)
    processed_image.save("/home/iap/Pictures/processed_image2.jpg")


    if mean_x < xR/2:
        y1 = (yc * xc)/(xc + yc*math.tan(math.radians(xoffset_angle)))
    else:
        y1 = (yc * xc)/(xc - yc*math.tan(math.radians(xoffset_angle)))    
    
"""print(f"yc is {yc}, y1 is {y1}, y is {y}")
print(f"laser detected at ({mean_x},{mean_y})")"""
print(f"Object is at distance of {y}")
print(f"Height of the object is {y - y1}")

print("Waiting for button press...")

