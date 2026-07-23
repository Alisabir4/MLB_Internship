# This Program shows how to rotate an image

import cv2

img = cv2.imread(r"img.png")

rows, cols = img.shape[:2]
center = (cols // 2, rows // 2)

for angle in [45, 90, 180]:
    matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotated = cv2.warpAffine(img, matrix, (cols, rows))
    cv2.imshow(f"Rotation {angle}", rotated)

cv2.waitKey(0)
cv2.destroyAllWindows()