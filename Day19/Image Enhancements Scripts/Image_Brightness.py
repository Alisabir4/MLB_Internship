# This Program shows how to increase and decrease image brightness

import cv2

img = cv2.imread(r"image.png")

bright = cv2.convertScaleAbs(img, alpha=1, beta=60)

dark = cv2.convertScaleAbs(img, alpha=1, beta=-60)

cv2.imshow("Original", img)
cv2.imshow("Bright", bright)
cv2.imshow("Dark", dark)

cv2.waitKey(0)
cv2.destroyAllWindows()