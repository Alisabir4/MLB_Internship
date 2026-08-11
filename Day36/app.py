import streamlit as st
import os
import cv2
import numpy as np
from ultralytics import YOLO

st.set_page_config(
    page_title="YOLO Model Performance Audit",
    layout="wide"
)

st.title("YOLO Model Performance Audit")

MODEL_PATH = "yolov8n.pt"
DATA_YAML = "data.yaml"
RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

# -----------------------------
# MODEL EVALUATION
# -----------------------------

st.header("Model Evaluation")

if st.button("Run Evaluation"):

    if not os.path.exists(DATA_YAML):

        st.error("data.yaml not found.")

    else:

        with st.spinner("Running evaluation..."):

            results = model.val(
                data=DATA_YAML,
                split="test",
                imgsz=640,
                conf=0.25,
                iou=0.50,
                plots=True,
                verbose=False
            )

        precision = float(results.box.mp)
        recall = float(results.box.mr)
        map50 = float(results.box.map50)
        map5095 = float(results.box.map)

        st.success("Evaluation completed.")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Precision",
            f"{precision:.4f}"
        )

        col2.metric(
            "Recall",
            f"{recall:.4f}"
        )

        col3.metric(
            "mAP@50",
            f"{map50:.4f}"
        )

        col4.metric(
            "mAP@50-95",
            f"{map5095:.4f}"
        )

        with open(
            os.path.join(RESULTS_DIR, "metrics.txt"),
            "w"
        ) as file:

            file.write(
                f"Precision : {precision:.4f}\n"
                f"Recall    : {recall:.4f}\n"
                f"mAP@50    : {map50:.4f}\n"
                f"mAP@50-95 : {map5095:.4f}\n"
            )


# -----------------------------
# CONFUSION MATRIX
# -----------------------------

st.header("Confusion Matrix")

matrix_paths = [
    "results/traffic_confusion_matrix.png",
    "runs/detect/results/confusion_matrix.png",
    "runs/detect/val/confusion_matrix.png",
    "runs/detect/val2/confusion_matrix.png"
]

matrix_found = False

for matrix_path in matrix_paths:

    if os.path.exists(matrix_path):

        st.image(
            matrix_path,
            caption="Confusion Matrix",
            use_container_width=True
        )

        matrix_found = True
        break

if not matrix_found:

    st.info(
        "Run Evaluation to generate the confusion matrix."
    )


# -----------------------------
# CHALLENGING EXAMPLES
# -----------------------------

st.header("Challenging Examples")

uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded is not None:

    image_bytes = uploaded.read()

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        st.error("Unable to read the uploaded image.")

    else:

        with st.spinner("Running YOLOv8 detection..."):

            predictions = model.predict(
                source=image,
                conf=0.25,
                iou=0.50,
                verbose=False
            )

        annotated_image = predictions[0].plot()

        st.image(
            cv2.cvtColor(
                annotated_image,
                cv2.COLOR_BGR2RGB
            ),
            caption="YOLOv8 Prediction",
            use_container_width=True
        )