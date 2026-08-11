import streamlit as st
import os

st.set_page_config(page_title="YOLO Model Performance Audit")

st.title("YOLO Model Performance Audit")

# Model Evaluation
st.header("Model Evaluation")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Precision", "35.95%")
col2.metric("Recall", "12.44%")
col3.metric("mAP@50", "8.83%")
col4.metric("mAP@50-95", "5.13%")

# Confusion Matrix
st.header("Confusion Matrix")

matrix_path = r"results/traffic_confusion_matrix.png"

if os.path.exists(matrix_path):
    st.image(
        matrix_path,
        caption="Traffic-200 Confusion Matrix",
        use_container_width=True
    )
else:
    st.warning("Confusion matrix not found.")

# Challenging Examples
st.header("Challenging Examples")

uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded is not None:
    st.image(
        uploaded,
        caption="Uploaded Challenging Example",
        use_container_width=True
    )