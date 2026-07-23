import cv2
import numpy as np

img = cv2.imread(r"img.png")

pts1 = np.float32([[70, 50],
                   [450, 40],
                   [60, 350],
                   [460, 360]])

pts2 = np.float32([[0, 0],
                   [400, 0],
                   [0, 500],
                   [400, 500]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)

result = cv2.warpPerspective(img, matrix, (400, 500))

cv2.imshow("Original", img)
cv2.imshow("Scanned Document", result)

cv2.waitKey(0)
cv2.destroyAllWindows()