import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Smart Object Tracking System",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Object Tracking System")
st.markdown(
    "Upload a video to detect and track objects using **YOLOv8 + ByteTrack**."
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.10,
    1.00,
    0.30,
    0.05
)

tracker = st.sidebar.selectbox(
    "Tracking Algorithm",
    ["bytetrack.yaml", "botsort.yaml"]
)

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

st.sidebar.success("YOLOv8 Model Loaded")

# -----------------------------
# Upload Video
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Video",
    type=["mp4", "avi", "mov", "mkv"]
)

if uploaded_file is not None:

    os.makedirs("output_videos", exist_ok=True)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(uploaded_file.read())
    temp_file.close()

    cap = cv2.VideoCapture(temp_file.name)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = os.path.join(
        "output_videos",
        "tracked_output.mp4"
    )

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    progress = st.progress(0)

    video_placeholder = st.empty()

    unique_ids = set()

    class_id_map = {}

    frame_number = 0

    st.info("Processing Video...")

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        results = model.track(
            frame,
            persist=True,
            tracker=tracker,
            conf=confidence,
            verbose=False
        )

        result = results[0]

        annotated = frame.copy()

        if result.boxes is not None:

            boxes = result.boxes

            if boxes.id is not None:

                ids = boxes.id.cpu().numpy().astype(int)
                classes = boxes.cls.cpu().numpy().astype(int)
                confs = boxes.conf.cpu().numpy()
                coords = boxes.xyxy.cpu().numpy()

                for box, cls, score, track_id in zip(
                        coords,
                        classes,
                        confs,
                        ids):

                    x1, y1, x2, y2 = map(int, box)

                    class_name = model.names[int(cls)]

                    unique_ids.add(track_id)

                    if track_id not in class_id_map:
                        class_id_map[track_id] = class_name

                    label = (
                        f"{class_name} "
                        f"ID:{track_id} "
                        f"{score:.2f}"
                    )

                    cv2.rectangle(
                        annotated,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        annotated,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

        writer.write(annotated)

        rgb = cv2.cvtColor(
            annotated,
            cv2.COLOR_BGR2RGB
        )

        video_placeholder.image(
            rgb,
            channels="RGB",
            use_container_width=True
        )

        frame_number += 1

        progress.progress(
            min(frame_number / total_frames, 1.0)
        )

    cap.release()
    writer.release()

    st.success("Tracking Completed Successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Unique Objects",
            len(unique_ids)
        )

    with col2:
        st.metric(
            "Frames Processed",
            frame_number
        )

    st.subheader("Detected Unique Objects")

    rows = []

    for track_id in sorted(class_id_map):

        rows.append({
            "Tracking ID": track_id,
            "Object": class_id_map[track_id]
        })

    st.dataframe(rows, use_container_width=True)

    st.subheader("Processed Video")

    st.video(output_path)

    with open(output_path, "rb") as file:

        st.download_button(
            label="📥 Download Processed Video",
            data=file,
            file_name="tracked_output.mp4",
            mime="video/mp4"
        )

    cap.release()

    os.remove(temp_file.name)