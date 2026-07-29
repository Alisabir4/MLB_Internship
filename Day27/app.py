import streamlit as st
import cv2
import numpy as np
from PIL import Image

from segmentation import segment_image
from utils import save_image

st.set_page_config(
    page_title="Document & Object Segmentation Tool",
    layout="wide"
)

st.title("📄 Document & Object Segmentation Tool")

st.write(
    "Upload an image and perform different segmentation techniques using OpenCV."
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

method = st.selectbox(
    "Select Segmentation Method",
    [
        "Binary Threshold",
        "Adaptive Threshold",
        "Otsu Threshold",
        "Foreground Segmentation"
    ]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    result = segment_image(image_np, method)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image)

    with col2:
        st.subheader(method)
        st.image(result, clamp=True)

    filename = save_image(result)

    with open(filename, "rb") as file:
        st.download_button(
            "Download Result",
            file,
            file_name="segmented_image.png",
            mime="image/png"
        )