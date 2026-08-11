import streamlit as st
import os
from ultralytics import YOLO

st.set_page_config(
    page_title="YOLO Model Performance Audit"
)

st.title("YOLO Model Performance Audit")

model = YOLO("yolov8n.pt")

# Model Evaluation
st.header("Model Evaluation")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Precision", "35.95%")
col2.metric("Recall", "12.44%")
col3.metric("mAP@50", "8.83%")
col4.metric("mAP@50-95", "5.13%")

# Confusion Matrix
st.header("Confusion Matrix")

matrix_path = "results/traffic_confusion_matrix.png"

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

    from PIL import Image

    image = Image.open(uploaded)

    results = model.predict(
        source=image,
        conf=0.25,
        iou=0.50,
        verbose=False
    )

    annotated = results[0].plot()

    st.image(
        annotated,
        caption="YOLOv8 Prediction",
        channels="BGR",
        use_container_width=True
    )