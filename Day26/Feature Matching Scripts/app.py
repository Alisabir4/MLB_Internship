import streamlit as st
import cv2
import numpy as np
from PIL import Image

from feature_matching import match_features

st.set_page_config(
    page_title="Image Feature Matching System",
    layout="wide"
)

st.title("Image Feature Matching System")

st.write("Upload two images to compare their features using ORB.")

col1, col2 = st.columns(2)

with col1:
    image1 = st.file_uploader(
        "Upload First Image",
        type=["jpg","jpeg","png"],
        key="img1"
    )

with col2:
    image2 = st.file_uploader(
        "Upload Second Image",
        type=["jpg","jpeg","png"],
        key="img2"
    )

if image1 and image2:

    img1 = np.array(Image.open(image1).convert("RGB"))
    img2 = np.array(Image.open(image2).convert("RGB"))

    img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)

    output, kp1, kp2, matches = match_features(img1, img2)

    st.image(
        cv2.cvtColor(output, cv2.COLOR_BGR2RGB),
        caption="Matched Features",
        use_container_width=True
    )

    st.success(f"Keypoints in Image 1 : {kp1}")
    st.success(f"Keypoints in Image 2 : {kp2}")
    st.success(f"Good Matches : {matches}")