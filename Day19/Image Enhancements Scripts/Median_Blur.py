import cv2

img = cv2.imread(r"image.png")

median = cv2.medianBlur(img, 5)

cv2.imshow("Original", img)
cv2.imshow("Median Blur", median)

cv2.waitKey(0)
cv2.destroyAllWindows()