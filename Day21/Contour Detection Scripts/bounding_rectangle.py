import cv2

image = cv2.imread("rectangle.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

output = image.copy()

for contour in contours:

    x, y, w, h = cv2.boundingRect(contour)

    cv2.rectangle(
        output,
        (x,y),
        (x+w,y+h),
        (255,0,0),
        2
    )

cv2.imwrite("../outputs/bounding_rectangle.jpg", output)

cv2.imshow("Bounding Rectangle", output)

cv2.waitKey(0)
cv2.destroyAllWindows()