import os
import cv2
import tempfile
import streamlit as st
from ultralytics import YOLO
from PIL import Image

# Page Configuration

st.set_page_config(
    page_title="Smart Object Detection",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Object Detection Application")
st.markdown("Detect objects in **Images** and **Videos** using a pre-trained **YOLO11n** model.")

# Load YOLO Model

@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")

model = load_model()

# Sidebar

st.sidebar.header("Settings")

input_type = st.sidebar.radio(
    "Choose Input Type",
    ["Image", "Video"]
)

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.25,
    step=0.05
)

os.makedirs("outputs/images", exist_ok=True)
os.makedirs("outputs/videos", exist_ok=True)

# IMAGE DETECTION

if input_type == "Image":

    uploaded_image = st.file_uploader(
        "Upload an Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:

        image = Image.open(uploaded_image).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)

        if st.button("Detect Objects"):

            with st.spinner("Detecting Objects..."):

                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".jpg"
                )

                image.save(temp_file.name)

                results = model.predict(
                    source=temp_file.name,
                    conf=confidence
                )

                annotated = results[0].plot()

                annotated = cv2.cvtColor(
                    annotated,
                    cv2.COLOR_BGR2RGB
                )

                with col2:
                    st.subheader("Detected Objects")
                    st.image(
                        annotated,
                        use_container_width=True
                    )

                st.subheader("Detection Results")

                detections = []

                if len(results[0].boxes) == 0:
                    st.warning("No objects detected.")

                else:

                    for box in results[0].boxes:

                        class_id = int(box.cls[0])
                        conf = float(box.conf[0])

                        detections.append({
                            "Object": model.names[class_id],
                            "Confidence": f"{conf:.2f}"
                        })

                    st.dataframe(
                        detections,
                        use_container_width=True
                    )

                output_path = "outputs/images/detected_image.jpg"

                cv2.imwrite(
                    output_path,
                    cv2.cvtColor(
                        annotated,
                        cv2.COLOR_RGB2BGR
                    )
                )

                with open(output_path, "rb") as file:

                    st.download_button(
                        label="⬇ Download Processed Image",
                        data=file,
                        file_name="detected_image.jpg",
                        mime="image/jpeg"
                    )

                os.unlink(temp_file.name)


# VIDEO DETECTION
else:

    uploaded_video = st.file_uploader(
        "Upload a Video",
        type=["mp4", "avi", "mov", "mkv"]
    )

    if uploaded_video:

        st.video(uploaded_video)

        if st.button("Process Video"):

            with st.spinner("Processing Video..."):

                temp_video = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp4"
                )

                temp_video.write(uploaded_video.read())

                cap = cv2.VideoCapture(temp_video.name)

                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)

                output_video = "outputs/videos/detected_video.mp4"

                writer = cv2.VideoWriter(
                    output_video,
                    cv2.VideoWriter_fourcc(*"mp4v"),
                    fps,
                    (width, height)
                )

                while True:

                    success, frame = cap.read()

                    if not success:
                        break

                    results = model(
                        frame,
                        conf=confidence
                    )

                    annotated = results[0].plot()

                    writer.write(annotated)

                cap.release()
                writer.release()

                st.success("Video Processed Successfully!")

                st.video(output_video)

                with open(output_video, "rb") as file:

                    st.download_button(
                        "⬇ Download Processed Video",
                        file,
                        file_name="detected_video.mp4",
                        mime="video/mp4"
                    )

                os.unlink(temp_video.name)

st.markdown("---")

st.markdown(
    """
    <div style="text-align: right; color: gray; font-size:16px;">
        © 2026 Developed By <strong>Ali Sabir</strong>
    </div>
    """,
    unsafe_allow_html=True
)