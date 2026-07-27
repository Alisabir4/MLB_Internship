import streamlit as st
import easyocr
import cv2
import numpy as np
from PIL import Image

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

st.set_page_config(page_title="OCR Coding Practice", layout="wide")

st.title("📝 OCR Coding Practice")
st.write("Upload an image to extract text using EasyOCR.")

# Upload Image
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Read image
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    # Display Original Image
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # Convert RGB to BGR
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # -------- Image Preprocessing --------
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    denoise = cv2.medianBlur(threshold, 3)

    # Display Processed Image
    st.subheader("Processed Image")
    st.image(denoise, use_container_width=True)

    # OCR
    result = reader.readtext(denoise, detail=0)

    extracted_text = "\n".join(result)

    # Display Text
    st.subheader("Extracted Text")
    st.text_area("", extracted_text, height=250)

    # Download Button
    st.download_button(
        label="📥 Download Text",
        data=extracted_text,
        file_name="OCR_Result.txt",
        mime="text/plain"
    )