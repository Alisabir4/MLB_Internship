import cv2
import os

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Read image
image = cv2.imread(r"D:\python\MLB_Internship\Day27\Sample Images/image1.jpg")

if image is None:
    print("Error: Image not found!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 1. Binary Thresholding

_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 2. Adaptive Thresholding

adaptive = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

# 3. Otsu Thresholding
_, otsu = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# 4. Foreground/Background Segmentation

foreground = cv2.bitwise_and(image, image, mask=otsu)

# Save Outputs

cv2.imwrite("outputs/grayscale.jpg", gray)
cv2.imwrite("outputs/binary_threshold.jpg", binary)
cv2.imwrite("outputs/adaptive_threshold.jpg", adaptive)
cv2.imwrite("outputs/otsu_threshold.jpg", otsu)
cv2.imwrite("outputs/foreground_segmentation.jpg", foreground)


# Display Results

cv2.imshow("Original Image", image)
cv2.imshow("Grayscale", gray)
cv2.imshow("Binary Threshold", binary)
cv2.imshow("Adaptive Threshold", adaptive)
cv2.imshow("Otsu Threshold", otsu)
cv2.imshow("Foreground Segmentation", foreground)

print("All output images have been saved in the 'outputs' folder.")

cv2.waitKey(0)
cv2.destroyAllWindows()