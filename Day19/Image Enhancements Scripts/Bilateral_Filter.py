import cv2

img = cv2.imread(r"image.png")

bilateral = cv2.bilateralFilter(img, 9, 75, 75)

cv2.imshow("Original", img)
cv2.imshow("Bilateral Filter", bilateral)

cv2.waitKey(0)
cv2.destroyAllWindows()