import streamlit as st
import os
import cv2
import numpy as np
from ultralytics import YOLO

st.set_page_config(page_title="YOLO Model Performance Audit")

st.title("YOLO Model Performance Audit")

model = YOLO("yolov8n.pt")

st.header("Model Evaluation")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Precision", "35.95%")
col2.metric("Recall", "12.44%")
col3.metric("mAP@50", "8.83%")
col4.metric("mAP@50-95", "5.13%")

st.header("Confusion Matrix")

matrix_path = "results/traffic_confusion_matrix.png"

if os.path.exists(matrix_path):
    st.image(matrix_path)
else:
    st.warning("Confusion matrix not found.")

st.header("Challenging Examples")

uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded is not None:

    image_bytes = uploaded.read()
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is not None:

        results = model.predict(
            source=image,
            conf=0.25,
            iou=0.50,
            verbose=False
        )

        annotated = results[0].plot()

        st.image(
            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
            caption="YOLOv8 Prediction",
            use_container_width=True
        )