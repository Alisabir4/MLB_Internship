import cv2
import numpy as np
import os
from datetime import datetime

# Create output folder
os.makedirs("output", exist_ok=True)

# Read image
image = cv2.imread(r"input/Person.png")

# Image properties
height, width, channels = image.shape
file_size = os.path.getsize(r"input/Person.png")

print("Height:", height)
print("Width:", width)
print("Channels:", channels)
print("File Size:", file_size, "bytes")

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("output/grayscale.jpg", gray)

# Resize
resize = cv2.resize(image, (500, 500))
cv2.imwrite("output/resized.jpg", resize)

# Crop
crop = image[100:400, 100:400]
cv2.imwrite("output/cropped.jpg", crop)

# Rotate
rotate90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
rotate180 = cv2.rotate(image, cv2.ROTATE_180)
rotate270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

cv2.imwrite("output/rotate90.jpg", rotate90)
cv2.imwrite("output/rotate180.jpg", rotate180)
cv2.imwrite("output/rotate270.jpg", rotate270)

# Flip
horizontal = cv2.flip(image, 1)
vertical = cv2.flip(image, 0)

cv2.imwrite("output/horizontal.jpg", horizontal)
cv2.imwrite("output/vertical.jpg", vertical)

# Draw shapes
draw = image.copy()

cv2.rectangle(draw, (50, 50), (200, 200), (0, 255, 0), 2)
cv2.circle(draw, (350, 150), 50, (255, 0, 0), 2)
cv2.line(draw, (0, 0), (300, 300), (0, 0, 255), 2)

points = np.array([[250,300], [350,250], [450,300], [400,400], [300,400]], np.int32)
cv2.polylines(draw, [points], True, (255,255,0), 2)

# Add text
today = datetime.now().strftime("%d-%m-%Y")

cv2.putText(draw, "Ali Sabir", (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

cv2.putText(draw, today, (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

cv2.imwrite("output/final.jpg", draw)

print("All images saved in output folder.")