import cv2
import numpy as np
import gradio as gr
import tempfile

# -----------------------------
# Image Processing Function
# -----------------------------
def process_image(image, operation):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if operation == "Grayscale":
        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif operation == "Blur":
        result = cv2.GaussianBlur(img, (9, 9), 0)

    elif operation == "Edge Detection":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.Canny(gray, 100, 200)

    elif operation == "Image Rotation":
        h, w = img.shape[:2]
        matrix = cv2.getRotationMatrix2D((w // 2, h // 2), 45, 1)
        result = cv2.warpAffine(img, matrix, (w, h))

    elif operation == "Image Enhancement":
        result = cv2.convertScaleAbs(img, alpha=1.4, beta=30)

    elif operation == "Contour Detection":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        result = img.copy()
        cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    elif operation == "Shape Detection":

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        result = img.copy()

        for cnt in contours:

            area = cv2.contourArea(cnt)

            if area < 300:
                continue

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)

            if len(approx) == 3:
                shape = "Triangle"

            elif len(approx) == 4:
                ratio = w / float(h)
                if 0.95 <= ratio <= 1.05:
                    shape = "Square"
                else:
                    shape = "Rectangle"

            elif len(approx) == 5:
                shape = "Pentagon"

            else:
                shape = "Circle"

            cv2.drawContours(result, [approx], -1, (0, 255, 0), 2)
            cv2.putText(
                result,
                shape,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

    else:
        result = img

    # Convert grayscale back to RGB
    if len(result.shape) == 2:
        display = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    else:
        display = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # Save output for download
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    cv2.imwrite(temp_file.name, cv2.cvtColor(display, cv2.COLOR_RGB2BGR))

    return display, temp_file.name


# -----------------------------
# Gradio Interface
# -----------------------------
demo = gr.Interface(
    fn=process_image,
    inputs=[
        gr.Image(type="numpy", label="Upload Image"),
        gr.Dropdown(
            [
                "Grayscale",
                "Blur",
                "Edge Detection",
                "Image Rotation",
                "Image Enhancement",
                "Contour Detection",
                "Shape Detection"
            ],
            label="Select Operation"
        )
    ],
    outputs=[
        gr.Image(label="Processed Image"),
        gr.File(label="Download Result")
    ],
    title="Computer Vision Toolkit",
    description="Upload an image, choose an image processing operation, view the result, and download the processed image."
)

demo.launch()