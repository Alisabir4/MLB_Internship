import cv2
import numpy as np

img = cv2.imread(r"image.png")

kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

sharpen = cv2.filter2D(img, -1, kernel)

cv2.imshow("Original", img)
cv2.imshow("Sharpened", sharpen)

cv2.waitKey(0)
cv2.destroyAllWindows()