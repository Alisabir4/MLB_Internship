import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os
from collections import defaultdict

# Streamlit Page Configuration

st.set_page_config(
    page_title="Smart Object Tracking System",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Object Tracking System")
st.markdown(
    """
Upload a video to detect and track multiple objects using **YOLOv8 + ByteTrack**.

### Features
- Upload Video
- Object Detection
- Object Tracking
- Tracking IDs
- Confidence Score
- Unique Object Counting
- Download Processed Video
"""
)


# Sidebar

st.sidebar.header("Tracking Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.30,
    step=0.05
)

tracker = st.sidebar.selectbox(
    "Tracker",
    (
        "bytetrack.yaml",
        "botsort.yaml"
    )
)

# Load Model
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


try:
    model = load_model()
    st.sidebar.success("YOLOv8 Loaded Successfully")
except Exception as e:
    st.error(e)
    st.stop()

# Upload Video

uploaded_video = st.file_uploader(
    "Upload Video",
    type=[
        "mp4",
        "avi",
        "mov",
        "mkv"
    ]
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
        st.error("Unable to open video.")
        st.stop()

    width = 640
    height = 360

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    output_path = os.path.join(
        "output_videos",
        "tracked_output.mp4"
    )

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    progress = st.progress(0)

    status = st.empty()

    unique_ids = set()

    class_object_ids = defaultdict(set)

    frame_count = 0

    st.info("Tracking Started...")

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.resize(
            frame,
            (width, height)
        )

        results = model.track(
            frame,
            persist=True,
            tracker=tracker,
            conf=confidence,
            verbose=False
        )

        annotated = frame.copy()

        if len(results) > 0:

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

                    class_object_ids[class_name].add(track_id)

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

        frame_count += 1

        if total_frames > 0:
            progress.progress(
                min(frame_count / total_frames, 1.0)
            )

        status.text(
            f"Processing Frame {frame_count} / {total_frames}"
        )
        cap.release()
    writer.release()

    progress.empty()
    status.empty()

    st.success("✅ Video Processing Completed!")

   
    # Summary Metrics

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
            frame_count
        )


    # Object Counts
   
    st.subheader("📋 Unique Objects By Class")

    if class_object_ids:

        table = []

        for class_name in sorted(class_object_ids.keys()):

            table.append(
                {
                    "Object": class_name,
                    "Unique Count": len(class_object_ids[class_name])
                }
            )

        st.table(table)

    else:

        st.warning("No objects detected.")

    
    # Tracking IDs
    st.subheader("🆔 Tracking IDs")

    if unique_ids:

        st.write(sorted(list(unique_ids)))

    else:

        st.write("No IDs Found")

    # Processed Video
    st.subheader("🎥 Processed Video")

    st.video(output_path)

    # Download Button
    
    with open(output_path, "rb") as file:

        st.download_button(
            label="📥 Download Processed Video",
            data=file,
            file_name="tracked_output.mp4",
            mime="video/mp4"
        )

   
    # Cleanup
 
    try:
        os.remove(temp_video.name)
    except:
        pass

else:

    st.info("👆 Upload a video to begin object tracking.")

# Footer

st.markdown(
    """
    <div style="text-align: right; color: gray; font-size:16px;">
       © 2026 Developed by <strong>Ali Sabir</strong>
    </div>
    """,
    unsafe_allow_html=True
)