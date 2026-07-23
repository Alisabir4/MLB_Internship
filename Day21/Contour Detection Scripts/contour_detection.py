import cv2

image = cv2.imread("diamond.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

output = image.copy()

cv2.drawContours(output, contours, -1, (0,255,0), 2)

print("Total Contours:", len(contours))

cv2.imwrite("../outputs/contours.jpg", output)

cv2.imshow("Contours", output)

cv2.waitKey(0)
cv2.destroyAllWindows()