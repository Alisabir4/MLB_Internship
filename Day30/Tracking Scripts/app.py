import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os

# Streamlit Page Configuration

st.set_page_config(
    page_title="Smart Object Tracking System",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Object Tracking System")
st.write("Upload a video to detect and track objects using YOLOv8 + ByteTrack.")

# Load YOLO Model

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()


# Upload Video
uploaded_file = st.file_uploader(
    "Upload Video",
    type=["mp4", "avi", "mov", "mkv"]
)

confidence = st.slider(
    "Confidence Threshold",
    0.10,
    1.00,
    0.30,
    0.05
)

if uploaded_file is not None:

    # Save uploaded file temporarily
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_file.read())
    temp_video.close()

    cap = cv2.VideoCapture(temp_video.name)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = "tracked_output.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    frame_placeholder = st.empty()

    progress = st.progress(0)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    unique_ids = set()

    class_counts = {}

    frame_number = 0

    st.info("Tracking Started...")

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
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
                xyxy = boxes.xyxy.cpu().numpy()

                for box, cls, conf, track_id in zip(
                        xyxy,
                        classes,
                        confs,
                        ids):

                    x1, y1, x2, y2 = map(int, box)

                    class_name = model.names[int(cls)]

                    unique_ids.add(track_id)

                    class_counts[class_name] = class_counts.get(class_name, 0) + 1

                    label = f"{class_name} | ID:{track_id} | {conf:.2f}"

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

        frame_placeholder.image(
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
            "Total Unique Objects",
            len(unique_ids)
        )

    with col2:
        st.metric(
            "Frames Processed",
            frame_number
        )

    st.subheader("Unique Tracking IDs")
    st.write(sorted(unique_ids))

    st.subheader("Detected Object Counts")

    if class_counts:
        st.table({
            "Class": list(class_counts.keys()),
            "Count": list(class_counts.values())
        })
    else:
        st.warning("No objects detected.")

    st.subheader("Processed Video")

    st.video(output_path)

    with open(output_path, "rb") as file:
        st.download_button(
            "⬇ Download Output Video",
            data=file,
            file_name="tracked_output.mp4",
            mime="video/mp4"
        )

    os.remove(temp_video.name)