import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os
from collections import defaultdict

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Object Tracking System",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Object Tracking System")

st.markdown("""
Upload a video to detect and track multiple objects using **YOLOv8** and **ByteTrack**.

### Features
- Upload Video
- Object Detection
- Object Tracking
- Tracking IDs
- Confidence Score
- Unique Object Count
- Save Output Video
""")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Tracking Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.30,
    step=0.05
)

tracker = st.sidebar.selectbox(
    "Tracking Algorithm",
    [
        "bytetrack.yaml",
        "botsort.yaml"
    ]
)

# --------------------------------------------------
# Load YOLO Model
# --------------------------------------------------

@st.cache_resource
def load_model():
    model = YOLO("yolov8n.pt")
    return model

try:
    model = load_model()
    st.sidebar.success("YOLOv8 Model Loaded")
except Exception as e:
    st.error(f"Model Loading Error:\n{e}")
    st.stop()

# --------------------------------------------------
# Upload Video
# --------------------------------------------------

uploaded_video = st.file_uploader(
    "Upload Video",
    type=["mp4", "avi", "mov", "mkv"]
)

if uploaded_video is not None:

    os.makedirs("output_videos", exist_ok=True)

    temp_video = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_video.write(uploaded_video.read())
    temp_video.close()

    cap = cv2.VideoCapture(temp_video.name)

    if not cap.isOpened():
        st.error("Unable to open uploaded video.")
        st.stop()

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    width = 640
    height = 360

    output_path = os.path.join(
        "output_videos",
        "tracked_output.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():
        st.error("Unable to create output video.")
        st.stop()

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    progress = st.progress(0)

    status = st.empty()

    unique_ids = set()

    class_ids = defaultdict(set)

    processed_frames = 0

    st.info("Processing Video...")
    
    while True:

        success, frame = cap.read()

        if not success:
            break

        # Resize frame for better performance
        frame = cv2.resize(frame, (width, height))

        # Run tracking
        results = model.track(
            frame,
            persist=True,
            tracker=tracker,
            conf=confidence,
            verbose=False
        )

        annotated_frame = frame.copy()

        if results and len(results):

            result = results[0]

            if (
                result.boxes is not None
                and result.boxes.id is not None
            ):

                boxes = result.boxes.xyxy.cpu().numpy()
                ids = result.boxes.id.cpu().numpy().astype(int)
                classes = result.boxes.cls.cpu().numpy().astype(int)
                scores = result.boxes.conf.cpu().numpy()

                for box, track_id, cls, score in zip(
                    boxes,
                    ids,
                    classes,
                    scores
                ):

                    x1, y1, x2, y2 = map(int, box)

                    class_name = model.names[int(cls)]

                    unique_ids.add(track_id)
                    class_ids[class_name].add(track_id)

                    label = (
                        f"{class_name} | "
                        f"ID:{track_id} | "
                        f"{score:.2f}"
                    )

                    cv2.rectangle(
                        annotated_frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        annotated_frame,
                        label,
                        (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

        # Write processed frame
        writer.write(annotated_frame)

        processed_frames += 1

        if total_frames > 0:
            progress.progress(
                min(processed_frames / total_frames, 1.0)
            )

        status.text(
            f"Processing Frame {processed_frames}/{total_frames}"
        )

    # ------------------------------
    # Release Resources
    # ------------------------------

    cap.release()
    writer.release()

    progress.empty()
    status.empty()

    st.success("✅ Video Processing Completed Successfully")
    
        # ----------------------------------------
    # Tracking Summary
    # ----------------------------------------

    st.subheader("📊 Tracking Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Unique Objects",
            len(unique_ids)
        )

    with col2:
        st.metric(
            "Frames Processed",
            processed_frames
        )

    # ----------------------------------------
    # Object Count Per Class
    # ----------------------------------------

    st.subheader("📋 Object Count by Class")

    if len(class_ids):

        data = []

        for class_name in sorted(class_ids.keys()):

            data.append(
                {
                    "Object": class_name,
                    "Unique Count": len(class_ids[class_name])
                }
            )

        st.table(data)

    else:

        st.warning("No objects detected.")

    # ----------------------------------------
    # Tracking IDs
    # ----------------------------------------

    st.subheader("🆔 Tracking IDs")

    if unique_ids:

        st.write(sorted(unique_ids))

    else:

        st.write("No IDs Found")

    # ----------------------------------------
    # Output Video
    # ----------------------------------------

    st.subheader("🎥 Processed Video")

    if os.path.exists(output_path):

        file_size = os.path.getsize(output_path)

        st.write(f"Video Size: {round(file_size/1024/1024,2)} MB")

        with open(output_path, "rb") as video_file:

            video_bytes = video_file.read()

        st.video(video_bytes)

        st.download_button(
            "📥 Download Processed Video",
            data=video_bytes,
            file_name="tracked_output.mp4",
            mime="video/mp4"
        )

    else:

        st.error("Output video not found.")

    # ----------------------------------------
    # Cleanup
    # ----------------------------------------

    try:
        cap.release()
    except:
        pass

    try:
        writer.release()
    except:
        pass

    try:
        os.remove(temp_video.name)
    except:
        pass

else:

    st.info("👆 Upload a video to start tracking.")

# ----------------------------------------
# Footer
# ----------------------------------------

st.markdown("---")

st.markdown(
    """
### Smart Object Tracking System

- Model: **YOLOv8 Nano (yolov8n.pt)**
- Tracker: **ByteTrack / BoT-SORT**
- Framework: **Streamlit**
- Library: **Ultralytics YOLO**
- Developer: **Ali Sabir**
"""
)