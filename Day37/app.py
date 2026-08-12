import os
import streamlit as st
from ultralytics import YOLO
from PIL import Image

st.set_page_config(
    page_title="YOLO Model Improvement",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 YOLO Model Improvement")
st.write("Model V1 → Data Improvement → Model V2")

# --------------------------------------------------
# MODEL PATHS
# --------------------------------------------------

V1_PATH = "yolov8n.pt"
V2_PATH = "best.pt"

# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

@st.cache_resource
def load_models():
    v1 = YOLO(V1_PATH)
    v2 = YOLO(V2_PATH)
    return v1, v2

v1, v2 = load_models()

# --------------------------------------------------
# V1 VS V2 METRICS
# --------------------------------------------------

st.header("V1 vs V2 Performance")

metrics = {
    "Precision": [0.3595, 0.8041],
    "Recall": [0.1244, 0.4077],
    "mAP@50": [0.0883, 0.4275],
    "mAP@50-95": [0.0513, 0.2724]
}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Model V1")
    st.metric("Precision", "0.3595")
    st.metric("Recall", "0.1244")
    st.metric("mAP@50", "0.0883")
    st.metric("mAP@50-95", "0.0513")

with col2:
    st.subheader("Model V2")
    st.metric("Precision", "0.8041")
    st.metric("Recall", "0.4077")
    st.metric("mAP@50", "0.4275")
    st.metric("mAP@50-95", "0.2724")

# --------------------------------------------------
# COMPARISON TABLE
# --------------------------------------------------

st.header("Performance Comparison")

st.table({
    "Metric": list(metrics.keys()),
    "V1": [0.3595, 0.1244, 0.0883, 0.0513],
    "V2": [0.8041, 0.4077, 0.4275, 0.2724]
})

# --------------------------------------------------
# CLASS DISTRIBUTION
# --------------------------------------------------

st.header("Original Class Distribution")

class_data = {
    "Class": [
        "bicycle",
        "bus",
        "car",
        "motorcycle",
        "person",
        "truck"
    ],
    "Samples": [
        1014,
        44,
        1785,
        672,
        0,
        17
    ]
}

st.table(class_data)

st.write(
    "The truck and bus classes had fewer samples. "
    "Augmentation was applied to improve the training data."
)

# --------------------------------------------------
# AUGMENTATION
# --------------------------------------------------

st.header("Data Improvement")

st.write("""
The V2 model was trained after improving the training data.

- Class distribution was analyzed.
- Underrepresented classes were identified.
- Image augmentation was applied.
- Augmented samples were added to the training dataset.
- YOLOv8 Nano was retrained for 20 epochs.
""")

# --------------------------------------------------
# FIVE COMPARISON EXAMPLES
# --------------------------------------------------

st.header("5 V2 Comparison Examples")

example_dir = "comparison_examples"

if os.path.exists(example_dir):

    examples = [
        f for f in os.listdir(example_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    examples = examples[:5]

    if examples:
        cols = st.columns(len(examples))

        for i, file in enumerate(examples):
            with cols[i]:
                image = Image.open(
                    os.path.join(example_dir, file)
                )
                st.image(
                    image,
                    caption=f"Example {i + 1}",
                    use_container_width=True
                )
    else:
        st.warning("No comparison examples found.")

else:
    st.warning("comparison_examples folder not found.")

# --------------------------------------------------
# LIVE IMAGE COMPARISON
# --------------------------------------------------

st.header("Live V1 vs V2 Prediction")

uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    image = Image.open(uploaded).convert("RGB")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("V1 Prediction")

        result_v1 = v1.predict(
            image,
            conf=0.25,
            verbose=False
        )[0]

        output_v1 = result_v1.plot()

        st.image(
            output_v1,
            caption="Model V1",
            use_container_width=True
        )

    with col2:

        st.subheader("V2 Prediction")

        result_v2 = v2.predict(
            image,
            conf=0.25,
            verbose=False
        )[0]

        output_v2 = result_v2.plot()

        st.image(
            output_v2,
            caption="Model V2",
            use_container_width=True
        )

# --------------------------------------------------
# CONCLUSION
# --------------------------------------------------

st.header("Conclusion")

st.success(
    "V2 achieved higher Precision, Recall, mAP@50 and mAP@50-95 "
    "than V1 under the available evaluation setup."
)

st.info(
    "V2 was created using improved training data and augmentation. "
    "The comparison demonstrates the effect of data improvement "
    "on YOLO model performance."
)