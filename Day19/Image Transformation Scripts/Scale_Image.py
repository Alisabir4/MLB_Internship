# This program show to scale imae up and down

import cv2

img = cv2.imread(r"img.png")

# Scale Up
scale_up = cv2.resize(img, None, fx=2, fy=2)

# Scale Down
scale_down = cv2.resize(img, None, fx=0.5, fy=0.5)

cv2.imshow("Original", img)
cv2.imshow("Scale Up", scale_up)
cv2.imshow("Scale Down", scale_down)

cv2.waitKey(0)
cv2.destroyAllWindows()