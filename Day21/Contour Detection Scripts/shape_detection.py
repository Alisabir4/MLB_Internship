import cv2

image = cv2.imread("hexagon.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

output = image.copy()

for contour in contours:

    area = cv2.contourArea(contour)

    if area < 100:
        continue

    perimeter = cv2.arcLength(contour, True)

    approx = cv2.approxPolyDP(
        contour,
        0.04 * perimeter,
        True
    )

    vertices = len(approx)

    x, y, w, h = cv2.boundingRect(approx)

    if vertices == 3:
        shape = "Triangle"

    elif vertices == 4:

        aspect_ratio = w / float(h)

        if 0.95 <= aspect_ratio <= 1.05:
            shape = "Square"
        else:
            shape = "Rectangle"

    elif vertices > 6:
        shape = "Circle"

    else:
        shape = "Polygon"

    cv2.drawContours(output, [approx], -1, (0,255,0), 2)

    cv2.putText(
        output,
        shape,
        (x, y-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255,0,0),
        2
    )

cv2.imwrite("../outputs/shapes_detected.jpg", output)

cv2.imshow("Shape Detection", output)

cv2.waitKey(0)
cv2.destroyAllWindows()