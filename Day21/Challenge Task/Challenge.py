import cv2
import os
import numpy as np


# Input and Output Paths
input_folder = r"D:\python\MLB_Internship\Day21\Input Images"
output_folder = r"D:\python\MLB_Internship\Day21\Output Images"

os.makedirs(output_folder, exist_ok=True)

# Shape Detection Function

def detect_shape(contour):

    perimeter = cv2.arcLength(contour, True)

    approx = cv2.approxPolyDP(
        contour,
        0.04 * perimeter,
        True
    )

    vertices = len(approx)

    if vertices == 3:
        return "Triangle"

    elif vertices == 4:

        x, y, w, h = cv2.boundingRect(approx)

        aspect_ratio = float(w) / h

        if 0.95 <= aspect_ratio <= 1.05:
            return "Square"
        else:
            return "Rectangle"

    elif vertices > 5:

        area = cv2.contourArea(contour)
        circularity = (
            4 * np.pi * area /
            (perimeter * perimeter)
        )

        if circularity > 0.75:
            return "Circle"

    return "Unknown"

# Process 10 Images

for i in range(1, 11):

    image_name = f"shape{i}.png"

    image_path = os.path.join(
        input_folder,
        image_name
    )

    image = cv2.imread(image_path)


    if image is None:
        print(f"{image_name} not found")
        continue


    print(f"Processing {image_name}")


# Save Original Image

    cv2.imwrite(
        os.path.join(
            output_folder,
            f"{i}_original.png"
        ),
        image
    )


# Convert to Gray

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


# Blur

    blur = cv2.GaussianBlur(
        gray,
        (5,5),
        0
    )


# Threshold

    _, thresh = cv2.threshold(
        blur,
        100,
        255,
        cv2.THRESH_BINARY
    )


# Find Contours

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


# Contour Image

    contour_image = image.copy()

    cv2.drawContours(
        contour_image,
        contours,
        -1,
        (0,255,0),
        3
    )


# Save Contour Result

    cv2.imwrite(
        os.path.join(
            output_folder,
            f"{i}_contours.png"
        ),
        contour_image
    )


# Final Result

    final_image = image.copy()


    for contour in contours:

        area = cv2.contourArea(contour)

        if area < 500:
            continue


        perimeter = cv2.arcLength(
            contour,
            True
        )


        shape = detect_shape(contour)


# Draw contour

        cv2.drawContours(
            final_image,
            [contour],
            -1,
            (0,255,0),
            3
        )


# Get text position

        x, y, w, h = cv2.boundingRect(contour)


        text = (
            f"{shape}\n"
            f"A:{int(area)} "
            f"P:{int(perimeter)}"
        )


# Draw text

        cv2.putText(
            final_image,
            shape,
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,0,255),
            2
        )


        cv2.putText(
            final_image,
            f"Area:{int(area)}",
            (x,y+h+20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255,0,0),
            2
        )


        cv2.putText(
            final_image,
            f"Perimeter:{int(perimeter)}",
            (x,y+h+40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255,0,0),
            2
        )


# Save Final Image

    cv2.imwrite(
        os.path.join(
            output_folder,
            f"{i}_final.png"
        ),
        final_image
    )


print("Shape Detection Completed Successfully!")