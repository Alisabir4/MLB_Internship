import cv2
import os
import numpy as np


input_folder = r"D:\python\MLB_Internship\Day20\Input Images"
output_folder = r"D:\python\MLB_Internship\Day20\Output Images"


os.makedirs(output_folder, exist_ok=True)


def detect_document(image_path, save_path):

    image = cv2.imread(image_path)

    if image is None:
        print("Image not found:", image_path)
        return

# Save Original Image
    cv2.imwrite(
        os.path.join(save_path, "original.jpg"),
        image
    )

# Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5,5), 0)


# Canny Edge Detection
    edges = cv2.Canny(
        blur,
        50,
        150
    )

    cv2.imwrite(
        os.path.join(save_path, "edges.jpg"),
        edges
    )


# Morphological Operations
    kernel = np.ones((5,5), np.uint8)

    morph = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel
    )


    cv2.imwrite(
        os.path.join(save_path, "morphology.jpg"),
        morph
    )


# Find Contours
    contours, _ = cv2.findContours(
        morph,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    if contours:

        largest_contour = max(
            contours,
            key=cv2.contourArea
        )


        area = cv2.contourArea(largest_contour)


        if area > 1000:

            cv2.drawContours(
                image,
                [largest_contour],
                -1,
                (0,255,0),
                3
            )


# Save Final Output
    cv2.imwrite(
        os.path.join(save_path, "final_boundary.jpg"),
        image
    )



for filename in os.listdir(input_folder):

    if filename.lower().endswith(
        (".jpg",".jpeg",".png")
    ):

        name = os.path.splitext(filename)[0]

        save_path = os.path.join(
            output_folder,
            name
        )

        os.makedirs(
            save_path,
            exist_ok=True
        )


        image_path = os.path.join(
            input_folder,
            filename
        )


        detect_document(
            image_path,
            save_path
        )


print("Document Boundary Detection Completed!")