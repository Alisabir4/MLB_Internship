import cv2

# Load image
image = cv2.imread("circle.png")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Save outputs
cv2.imwrite("../outputs/grayscale.jpg", gray)
cv2.imwrite("../outputs/threshold.jpg", thresh)

print("Grayscale and Threshold images saved.")

cv2.imshow("Original", image)
cv2.imshow("Grayscale", gray)
cv2.imshow("Threshold", thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()