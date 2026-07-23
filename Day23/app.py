import cv2
import numpy as np
import gradio as gr
import tempfile


# Image Processing Function
def process_image(image, operation):

    if image is None:
        return None, None, None

    # Convert RGB to BGR
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Grayscale
    
    if operation == "Grayscale":

        result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur
    elif operation == "Blur":

        result = cv2.GaussianBlur(img, (9, 9), 0)

    
    # Edge Detection
    
    elif operation == "Edge Detection":

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.Canny(gray, 100, 200)

    # Image Rotation
    
    elif operation == "Image Rotation":

        h, w = img.shape[:2]

        matrix = cv2.getRotationMatrix2D(
            (w // 2, h // 2),
            45,
            1
        )

        result = cv2.warpAffine(img, matrix, (w, h))

    # Image Enhancement

    elif operation == "Image Enhancement":

        result = cv2.convertScaleAbs(
            img,
            alpha=1.4,
            beta=30
        )

    # Contour Detection
    
    elif operation == "Contour Detection":

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 100, 200)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        result = img.copy()

        cv2.drawContours(
            result,
            contours,
            -1,
            (0, 255, 0),
            2
        )
            
    # Shape Detection
    
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

    # Image Flip
    elif operation == "Image Flip":

        result = cv2.flip(img, 1)

    # Image Sharpening
 
    elif operation == "Image Sharpening":

        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])

        result = cv2.filter2D(img, -1, kernel)

    # Thresholding
    elif operation == "Thresholding":

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, result = cv2.threshold(
            gray,
            127,
            255,
            cv2.THRESH_BINARY
        )

    else:

        result = img

    # Convert Result for Display

    if len(result.shape) == 2:
        display = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    else:
        display = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    # Save Processed Image
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    )

    cv2.imwrite(
        temp_file.name,
        cv2.cvtColor(display, cv2.COLOR_RGB2BGR)
    )

    return image, display, temp_file.name
# Gradio User Interface


operations = [
    "Grayscale",
    "Blur",
    "Edge Detection",
    "Image Rotation",
    "Image Enhancement",
    "Contour Detection",
    "Shape Detection",
    "Image Flip",
    "Image Sharpening",
    "Thresholding"
]

with gr.Blocks(title="Computer Vision Image Processing Studio") as demo:

    gr.Markdown(
        """
        # 🖼 Computer Vision Image Processing Studio

        Upload an image, choose an image processing operation,
        preview the result, and download the processed image.
        """
    )

    with gr.Row():

        input_image = gr.Image(
            type="numpy",
            label="Upload Image"
        )

        operation = gr.Dropdown(
            choices=operations,
            value="Grayscale",
            label="Select Operation"
        )

    process_btn = gr.Button("Process Image", variant="primary")

    with gr.Row():

        original_image = gr.Image(
            label="Original Image"
        )

        processed_image = gr.Image(
            label="Processed Image"
        )

    download_file = gr.File(
        label="Download Processed Image"
    )

    process_btn.click(
        fn=process_image,
        inputs=[input_image, operation],
        outputs=[
            original_image,
            processed_image,
            download_file
        ]
    )

gr.Markdown(
    """
    ### Features

    ✅ Upload Image

    ✅ Grayscale

    ✅ Blur

    ✅ Edge Detection

    ✅ Image Rotation

    ✅ Image Enhancement

    ✅ Contour Detection

    ✅ Shape Detection

    ✅ Image Flip

    ✅ Image Sharpening

    ✅ Thresholding

    ✅ Download Processed Image
    """
)

if __name__ == "__main__":
    demo.launch()