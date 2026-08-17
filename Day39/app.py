import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import cv2
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Day 39 - Cup Detection",
    page_icon="🥤",
    layout="wide"
)

# =========================================================
# LOAD MODEL
# =========================================================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()

# =========================================================
# HEADER
# =========================================================

st.title("🥤 Day 39 - Custom Cup Detection")
st.write(
    "YOLOv8 custom object detection application trained to detect cups."
)

st.success("Model loaded successfully")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Detection Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.05,
    max_value=0.95,
    value=0.40,
    step=0.05
)

st.sidebar.write(f"Current threshold: **{confidence:.2f}**")

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **Model**
    
    YOLOv8n
    
    **Class**
    
    Cup
    
    **Training**
    
    20 epochs
    """
)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    ["🖼️ Image Detection", "🎥 Video Detection", "📊 Model Information"]
)

# =========================================================
# IMAGE DETECTION
# =========================================================

with tab1:

    st.header("🖼️ Test an Image")

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:

        image = Image.open(uploaded_image).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)

        # -------------------------------------------------
        # RUN MODEL
        # -------------------------------------------------

        with st.spinner("Detecting cups..."):

            results = model.predict(
                source=image,
                conf=confidence,
                verbose=False
            )

        result = results[0]

        # Plot predictions
        annotated = result.plot()

        # Convert BGR → RGB
        annotated = cv2.cvtColor(
            annotated,
            cv2.COLOR_BGR2RGB
        )

        with col2:
            st.subheader("Detection Result")
            st.image(
                annotated,
                use_container_width=True
            )

        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        st.subheader("📊 Detection Statistics")

        boxes = result.boxes

        if boxes is not None and len(boxes) > 0:

            count = len(boxes)

            confidences = boxes.conf.cpu().numpy()

            average_confidence = float(
                confidences.mean()
            )

            highest_confidence = float(
                confidences.max()
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Cups Detected",
                count
            )

            col2.metric(
                "Average Confidence",
                f"{average_confidence:.2f}"
            )

            col3.metric(
                "Highest Confidence",
                f"{highest_confidence:.2f}"
            )

            # -------------------------------------------------
            # DETECTION TABLE
            # -------------------------------------------------

            detection_data = []

            for i, box in enumerate(boxes):

                confidence_score = float(
                    box.conf[0]
                )

                class_id = int(
                    box.cls[0]
                )

                detection_data.append({
                    "Detection": i + 1,
                    "Class": "cup",
                    "Confidence": round(
                        confidence_score,
                        3
                    )
                })

            df = pd.DataFrame(
                detection_data
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.warning(
                "No cup detected. Try lowering the confidence threshold."
            )

        # -------------------------------------------------
        # DOWNLOAD RESULT
        # -------------------------------------------------

        result_rgb = Image.fromarray(
            annotated
        )

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        )

        result_rgb.save(
            temp_file.name,
            format="JPEG"
        )

        with open(
            temp_file.name,
            "rb"
        ) as file:

            st.download_button(
                label="⬇️ Download Prediction",
                data=file,
                file_name="cup_prediction.jpg",
                mime="image/jpeg"
            )

# =========================================================
# VIDEO DETECTION
# =========================================================

with tab2:

    st.header("🎥 Test a Short Video")

    uploaded_video = st.file_uploader(
        "Upload a short video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_video is not None:

        # Save uploaded video temporarily
        input_path = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        ).name

        with open(input_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        # Output directory
        output_dir = os.path.join(
            BASE_DIR,
            "outputs"
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        output_path = os.path.join(
            output_dir,
            "predicted_video.mp4"
        )

        st.info("Processing video... Please wait.")

        try:

            cap = cv2.VideoCapture(input_path)

            width = int(
                cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            )

            height = int(
                cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            )

            fps = cap.get(
                cv2.CAP_PROP_FPS
            )

            if fps <= 0:
                fps = 25

            fourcc = cv2.VideoWriter_fourcc(
                *"mp4v"
            )

            writer = cv2.VideoWriter(
                output_path,
                fourcc,
                fps,
                (width, height)
            )

            frame_count = 0
            total_detections = 0

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                results = model.predict(
                    source=frame,
                    conf=confidence,
                    verbose=False
                )

                result = results[0]

                annotated_frame = result.plot()

                writer.write(
                    annotated_frame
                )

                if result.boxes is not None:
                    total_detections += len(
                        result.boxes
                    )

                frame_count += 1

            cap.release()
            writer.release()

            st.success(
                "✅ Video processing completed!"
            )

            # Show statistics
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Frames Processed",
                    frame_count
                )

            with col2:
                st.metric(
                    "Total Cup Detections",
                    total_detections
                )

            # Display video
            st.subheader(
                "🎬 Prediction Result"
            )

            with open(
                output_path,
                "rb"
            ) as video_file:

                video_bytes = video_file.read()

            st.video(
                video_bytes
            )

            # Download button
            st.download_button(
                label="⬇️ Download Prediction Video",
                data=video_bytes,
                file_name="predicted_cup_video.mp4",
                mime="video/mp4"
            )

        except Exception as e:

            st.error(
                f"Video processing failed: {e}"
            )

        finally:

            if os.path.exists(
                input_path
            ):
                os.remove(
                    input_path
                )

# =========================================================
# MODEL INFORMATION
# =========================================================

with tab3:

    st.header("📊 Model Information")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Model")

        st.write(
            "**Architecture:** YOLOv8n"
        )

        st.write(
            "**Task:** Object Detection"
        )

        st.write(
            "**Classes:** 1"
        )

        st.write(
            "**Class:** cup"
        )

    with col2:

        st.subheader("Training")

        st.write(
            "**Epochs:** 20"
        )

        st.write(
            "**Image Size:** 640 × 640"
        )

        st.write(
            "**Batch Size:** 16"
        )

        st.write(
            "**GPU:** Tesla T4"
        )

    st.markdown("---")

    st.subheader("🎯 Day 39 Objective")

    st.write(
        """
        The model was trained using a custom cup dataset.
        The original black and white cup classes were converted
        into a single class called **cup**, allowing the model
        to detect cups regardless of their color.
        """
    )

    st.subheader("🔍 Error Analysis")

    st.write(
        """
        The model should be tested on at least 20 completely
        unseen images. Difficult examples can include:

        • Small or distant cups

        • Partially hidden cups

        • Poor lighting

        • Cluttered backgrounds

        • Unusual cup shapes
        """
    )

