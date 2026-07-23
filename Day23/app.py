import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile

st.set_page_config(
    page_title="Computer Vision Image Processing Studio",
    layout="wide"
)

st.title("🖼️ Computer Vision Image Processing Studio")
st.write("Upload an image, choose an operation, and download the processed result.")


# Image Processing Function


def process_image(image, operation):

    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

   
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
            approx = cv2.approxPolyDP(
                cnt,
                0.04 * peri,
                True
            )

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

            cv2.drawContours(
                result,
                [approx],
                -1,
                (0, 255, 0),
                2
            )

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

        result = cv2.filter2D(
            img,
            -1,
            kernel
        )

    
    # Thresholding
    
    elif operation == "Thresholding":

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        _, result = cv2.threshold(
            gray,
            127,
            255,
            cv2.THRESH_BINARY
        )

    else:

        result = img

    return result, img

# Sidebar


st.sidebar.header("Image Processing Options")

operation = st.sidebar.selectbox(
    "Select Operation",
    [
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
)

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png", "bmp"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    result, original = process_image(image, operation)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    with col2:

        st.subheader("Processed Image")

        if len(result.shape) == 2:
            display = result
        else:
            display = cv2.cvtColor(
                result,
                cv2.COLOR_BGR2RGB
            )

        st.image(display, use_container_width=True)

    # Download Processed Image
    

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    )

    if len(result.shape) == 2:

        cv2.imwrite(
            temp_file.name,
            result
        )

    else:

        cv2.imwrite(
            temp_file.name,
            result
        )

    with open(temp_file.name, "rb") as file:

        st.download_button(
            label="📥 Download Processed Image",
            data=file,
            file_name="processed_image.png",
            mime="image/png"
        )

else:

    st.info("Please upload an image to begin.")

    
