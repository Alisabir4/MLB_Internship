# This program shows how to contrast image
import cv2

img = cv2.imread(r"image.png")

high_contrast = cv2.convertScaleAbs(img, alpha=2, beta=0)

low_contrast = cv2.convertScaleAbs(img, alpha=0.5, beta=0)

cv2.imshow("Original", img)
cv2.imshow("High Contrast", high_contrast)
cv2.imshow("Low Contrast", low_contrast)

cv2.waitKey(0)
cv2.destroyAllWindows()