import cv2

image = cv2.imread("rectangle.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

output = image.copy()

for contour in contours:

    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)

    print(f"Area: {area:.2f}")
    print(f"Perimeter: {perimeter:.2f}")
    print("-------------------")

    cv2.drawContours(output, [contour], -1, (0,255,0), 2)

cv2.imwrite("../outputs/contour_properties.jpg", output)

cv2.imshow("Properties", output)

cv2.waitKey(0)
cv2.destroyAllWindows()