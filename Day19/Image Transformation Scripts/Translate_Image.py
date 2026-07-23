# This program shows how to translate images horizontally and Vertically


import cv2
import numpy as np

img = cv2.imread(r"img.png")

rows, cols = img.shape[:2]

# Move Right = 100 pixels, Down = 50 pixels

matrix = np.float32([[1, 0, 100],
                     [0, 1, 50]])

translated = cv2.warpAffine(img, matrix, (cols, rows))

cv2.imshow("Original", img)
cv2.imshow("Translated", translated)

cv2.waitKey(0)
cv2.destroyAllWindows()
