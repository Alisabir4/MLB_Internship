import streamlit as st

st.set_page_config(
    page_title="Day 38 - Custom Object Detection",
    page_icon="🥤",
    layout="wide"
)

st.title("🥤 Day 38 - Custom Object Detection")

st.header("📊 Dataset Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Original Images", "241")
col2.metric("Train", "201")
col3.metric("Validation", "30")
col4.metric("Test", "10")

st.header("Dataset Split")

data = {
    "Train": (201, 201),
    "Validation": (30, 30),
    "Test": (10, 10)
}

for split, values in data.items():
    c1, c2 = st.columns(2)
    c1.write(f"**{split} Images:** {values[0]}")
    c2.write(f"**{split} Labels:** {values[1]}")

st.header("Class Distribution")

col1, col2 = st.columns(2)

col1.metric("Black", "30")
col2.metric("White", "30")

st.bar_chart({
    "Black": 30,
    "White": 30
})

st.header("Annotation Check")

st.success("All 241 images have corresponding YOLO annotation files.")

st.header("🤖 Model Training")

col1, col2, col3 = st.columns(3)

col1.metric("Model", "YOLOv8n")
col2.metric("Epochs", "10")
col3.metric("Image Size", "640")

st.header("📈 Evaluation Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Precision", "99.77%")
col2.metric("Recall", "100%")
col3.metric("mAP@50", "99.50%")
col4.metric("mAP@50-95", "93.99%")

st.header("🧪 Unseen Image Testing")

st.write(
    "The trained model was tested on 10 completely new images "
    "collected separately from the original dataset."
)

st.warning(
    "The model detected most cups correctly, but at least one cup was missed."
)

st.header("📌 Dataset Summary")

st.write(
    "The dataset contains 241 original images with YOLO "
    "bounding-box annotations."
)

st.write("Classes: black and white.")

st.write(
    "The training dataset was augmented to 650 images."
)

st.write(
    "The YOLOv8n model was trained for 10 epochs."
)