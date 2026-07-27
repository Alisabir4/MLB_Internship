import streamlit as st
import cv2
import numpy as np
from PIL import Image

from preprocessing import preprocess_image
from ocr import extract_text
from utils import save_text

st.set_page_config(
    page_title="Document OCR Web Application",
    layout="wide"
)

st.title("Document OCR Web Application")

st.write("Upload a document image and extract text using EasyOCR.")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    image_np = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2BGR
    )

    # Create grayscale image for display
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Preprocess image for OCR
    processed = preprocess_image(image_np)

    # Display grayscale image
    st.subheader("Processed Image")
    st.image(gray, use_container_width=True)

    # OCR uses the processed image
    extracted_text = extract_text(processed)

    st.subheader("Extracted Text")
    st.text_area(
        "",
        extracted_text,
        height=300
    )

    txt_file = save_text(extracted_text)

    st.download_button(
        label="📥 Download OCR Result",
        data=extracted_text,
        file_name="OCR_Result.txt",
        mime="text/plain"
    )