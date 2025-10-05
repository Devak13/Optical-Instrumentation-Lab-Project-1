from PIL import Image
import math
import blink as ub

ifovx = 0.02128

xc = 84  #Distance between camera and laser
xR = 2592
yR = 1944
angle = 14.9768359395
tan = math.tan(math.radians(angle))
yc = xc / tan


image_path = "/home/iap/Pictures/photo1.jpg"
ub.image_capture(image_path)
# Load the image

image = Image.open(image_path).convert("RGB")  # Ensure it's in RGB mode
width, height = image.size
print("width is "+str(width)+" and height is "+str(height))

# Create a copy to modify
processed_image = image.copy()
pixels = processed_image.load()  # Access pixel data

# Accumulators
acc_x = 0
acc_y = 0
acc_count = 0

# Iterate over all pixels
for x in range(int(2592/2 - 250),int(2592/2+50) ):
    for y in range(int(1944/2 -1), int(1944/2 +1)):
        red, green, blue = image.getpixel((x, y))

        '''if (red > green and red > blue and red>235 and blue<100 and green <100) or (red>250 and blue>250 and green > 250):'''
        if (red > green and red > blue and red>70):
            acc_x += x
            acc_y += y
            acc_count += 1
            pixels[x, y] = (255, 255, 255)  # Set pixel to white  

if acc_count == 0:
    print("Outside of region or not reading any red pixel")

# Draw green cross at the mean position
elif acc_count > 0:
    mean_x = int(acc_x / acc_count)
    mean_y = int(acc_y / acc_count)

    # Green Crosshair
    if 1 <= mean_x < width - 1 and 1 <= mean_y < height - 1:
        cross_color = (0, 255, 0)
        pixels[mean_x, mean_y] = cross_color
        pixels[mean_x - 1, mean_y] = cross_color
        pixels[mean_x + 1, mean_y] = cross_color
        pixels[mean_x, mean_y - 1] = cross_color
        pixels[mean_x, mean_y + 1] = cross_color
        pixels[mean_x - 2, mean_y] = cross_color
        pixels[mean_x + 2, mean_y] = cross_color
        pixels[mean_x, mean_y - 2] = cross_color
        pixels[mean_x, mean_y + 2] = cross_color
        
        xoffset_pixel = xR/2 - mean_x
        yoffset_pixel = yR/2 - mean_y
        xoffset_angle = xoffset_pixel * ifovx
        print("offest angle is "+str(xoffset_angle))
        print("offset pixel is "+str(xoffset_pixel))
        if mean_x < int(2592/2):
            y = (yc * xc)/(xc + yc*math.tan(math.radians(xoffset_angle)))
        else:
            y = (yc * xc)/(xc - yc*math.tan(math.radians(xoffset_angle)))
        print("yc is "+str(yc))
        #print(math.tan(math.radians(45)))
        print("Object is at height of "+str(y))
        print("Object is of height "+str(y - yc))

        
    print("laser detected at ("+str(mean_x)+","+str(mean_y)+")")

# Save or show the result
processed_image.save("/home/iap/Pictures/processed_image.jpg")
#processed_image.show()


