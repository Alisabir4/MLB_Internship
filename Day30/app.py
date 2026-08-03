import os
import time
import tempfile

import streamlit as st
from ultralytics import YOLO

from tracking_utils import process_video


# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Smart Object Tracking System",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Object Tracking System")

st.write(
    """
Upload a video to detect and track multiple objects using
**YOLOv8 + ByteTrack / BoT-SORT**.
"""
)


# ----------------------------------------------------
# Load YOLO Model
# ----------------------------------------------------

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()


# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.header("Tracking Settings")

tracker_choice = st.sidebar.selectbox(
    "Tracking Algorithm",
    [
        "ByteTrack",
        "BoT-SORT"
    ]
)

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.10,
    1.00,
    0.30,
    0.05
)


# ----------------------------------------------------
# Upload Video
# ----------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Video",
    type=[
        "mp4",
        "avi",
        "mov",
        "mkv"
    ]
)

video_path = None

if uploaded_file is not None:

    temp_video = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_video.write(uploaded_file.read())
    temp_video.close()

    video_path = temp_video.name

    st.video(video_path)


# ----------------------------------------------------
# Start Tracking
# ----------------------------------------------------

start_tracking = st.button(
    "Start Tracking",
    type="primary",
    disabled=video_path is None
)

if start_tracking:

    tracker_yaml = (
        "bytetrack.yaml"
        if tracker_choice == "ByteTrack"
        else "botsort.yaml"
    )

    output_path = os.path.join(
        tempfile.gettempdir(),
        f"tracked_{int(time.time())}.mp4"
    )

    progress_bar = st.progress(0)

    video_placeholder = st.empty()

    def update_progress(current_frame, total_frames):

        if total_frames > 0:

            progress_bar.progress(
                min(current_frame / total_frames, 1.0),
                text=f"Processing Frame {current_frame}/{total_frames}"
            )

    def update_frame(frame):

        video_placeholder.image(
            frame,
            channels="BGR",
            use_container_width=True
        )
    # ----------------------------------------------------
    # Start Video Processing
    # ----------------------------------------------------

    summary = process_video(
        model=model,
        source_path=video_path,
        output_path=output_path,
        tracker=tracker_yaml,
        conf=confidence,
        progress_callback=update_progress,
        frame_callback=update_frame
    )

    progress_bar.empty()

    st.success("✅ Video Processing Completed Successfully!")

    # ----------------------------------------------------
    # Tracking Summary
    # ----------------------------------------------------

    st.subheader("📊 Tracking Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Unique Objects",
            summary["unique_object_count"]
        )

    with col2:
        st.metric(
            "Frames Processed",
            summary["frames"]
        )

    # ----------------------------------------------------
    # Per-Class Object Counts
    # ----------------------------------------------------

    st.subheader("📋 Object Count by Class")

    if summary["per_class_unique_counts"]:

        table = []

        for class_name, count in summary["per_class_unique_counts"].items():

            table.append(
                {
                    "Object": class_name,
                    "Unique Count": count
                }
            )

        st.table(table)

    else:

        st.warning("No objects detected.")
        
            # ----------------------------------------------------
    # Processed Video
    # ----------------------------------------------------

    st.subheader("🎥 Processed Video")

    if os.path.exists(summary["output_path"]):

        with open(summary["output_path"], "rb") as file:

            video_bytes = file.read()

        st.video(video_bytes)

        st.download_button(
            label="📥 Download Processed Video",
            data=video_bytes,
            file_name="tracked_output.mp4",
            mime="video/mp4"
        )

    else:

        st.error("Output video not found.")

    # ----------------------------------------------------
    # Tracking Details
    # ----------------------------------------------------

    st.subheader("📈 Tracking Details")

    st.write(f"**Tracker Used:** {tracker_choice}")

    st.write(f"**Confidence Threshold:** {confidence}")

    st.write(f"**Frames Processed:** {summary['frames']}")

    st.write(f"**Total Unique Objects:** {summary['unique_object_count']}")

    # ----------------------------------------------------
    # Cleanup
    # ----------------------------------------------------

    try:
        os.remove(video_path)
    except Exception:
        pass

    try:
        os.remove(summary["output_path"])
    except Exception:
        pass

else:

    st.info("👆 Upload a video to begin object tracking.")

