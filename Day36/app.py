import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="YOLO Model Performance Audit",
    layout="wide"
)

st.title("YOLO Model Performance Audit")

RESULT_DIR = "results"

# -----------------------------
# MODEL EVALUATION
# -----------------------------

st.header("Model Evaluation")

if st.button("Run Evaluation"):

    metrics_path = os.path.join(
        RESULT_DIR,
        "metrics.txt"
    )

    if os.path.exists(metrics_path):

        metrics = {}

        with open(metrics_path, "r") as file:

            for line in file:

                if ":" in line:

                    key, value = line.split(":", 1)

                    metrics[key.strip()] = value.strip()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Precision",
            metrics.get("Precision", "N/A")
        )

        col2.metric(
            "Recall",
            metrics.get("Recall", "N/A")
        )

        col3.metric(
            "mAP@50",
            metrics.get("mAP@50", "N/A")
        )

        col4.metric(
            "mAP@50-95",
            metrics.get("mAP@50-95", "N/A")
        )

        st.success("Evaluation results loaded.")

    else:

        st.error(
            "Evaluation results not found. "
            "Run the evaluation locally first."
        )


# -----------------------------
# CONFUSION MATRIX
# -----------------------------

st.header("Confusion Matrix")

matrix_path = os.path.join(
    RESULT_DIR,
    r"traffic_confusion_matrix.png"
)

if os.path.exists(matrix_path):

    st.image(
        matrix_path,
        caption="Traffic-200 6-Class Confusion Matrix",
        use_container_width=True
    )

else:

    st.warning(
        "Confusion matrix not found."
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

    image = Image.open(uploaded)

    st.image(
        image,
        caption="Challenging Example",
        use_container_width=True
    )