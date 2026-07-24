import streamlit as st
import easyocr
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Simple OCR Document Reader", page_icon="📄")

st.title("Simple OCR Document Reader")
st.write("Upload an image and extract text using EasyOCR.")

# Load EasyOCR
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png", "bmp"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    img = np.array(image)

    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    enhanced = cv2.equalizeHist(gray)

    st.subheader("Enhanced Image")
    st.image(enhanced, use_container_width=True)

    with st.spinner("Extracting text..."):

        results = reader.readtext(enhanced, detail=0)

        extracted_text = "\n".join(results)

    st.subheader("Extracted Text")
    st.text_area(
        "",
        extracted_text,
        height=300
    )

    st.download_button(
        "📥 Download Extracted Text",
        extracted_text,
        file_name="extracted_text.txt",
        mime="text/plain"
    )