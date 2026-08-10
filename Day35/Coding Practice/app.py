import cv2
import time
import tempfile
import streamlit as st
from ultralytics import YOLO

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Real-Time Video Analytics",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 Real-Time Video Analytics")
st.write(
    "YOLO detection + object tracking + FPS + counting + ROI entry/exit"
)

# -----------------------------
# Load YOLO Model
# -----------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙️ Settings")

confidence = st.sidebar.slider(
    "Confidence",
    0.10,
    1.00,
    0.40,
    0.05
)

show_roi = st.sidebar.checkbox(
    "Show ROI",
    value=True
)

# -----------------------------
# Video Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a traffic or people video",
    type=["mp4", "avi", "mov", "mkv"]
)

if uploaded_file is None:
    st.info("Upload a video to start real-time analytics.")
    st.stop()

# -----------------------------
# Save Uploaded Video
# -----------------------------
temp_file = tempfile.NamedTemporaryFile(
    delete=False,
    suffix=".mp4"
)

temp_file.write(uploaded_file.read())
temp_file.close()

video_path = temp_file.name

# -----------------------------
# Open Video
# -----------------------------
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    st.error("Unable to open video.")
    st.stop()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_video = cap.get(cv2.CAP_PROP_FPS)

# -----------------------------
# ROI
# -----------------------------
roi_x1 = int(width * 0.25)
roi_y1 = int(height * 0.25)

roi_x2 = int(width * 0.75)
roi_y2 = int(height * 0.75)

# -----------------------------
# Tracking Variables
# -----------------------------
previous_positions = {}

entries = 0
exits = 0

# -----------------------------
# Streamlit Layout
# -----------------------------
video_area = st.empty()

col1, col2, col3, col4 = st.columns(4)

fps_display = col1.empty()
object_display = col2.empty()
entry_display = col3.empty()
exit_display = col4.empty()

# -----------------------------
# Processing
# -----------------------------
previous_time = time.time()

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    # -------------------------
    # Start FPS Timer
    # -------------------------
    start_time = time.time()

    # -------------------------
    # YOLO Tracking
    # -------------------------
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=confidence,
        verbose=False
    )

    result = results[0]

    current_positions = {}
    current_objects = 0

    # -------------------------
    # Process Detections
    # -------------------------
    if result.boxes is not None:

        boxes = result.boxes

        for box in boxes:

            # Tracking ID
            if box.id is None:
                continue

            track_id = int(box.id[0])

            # Bounding box
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # Confidence
            conf = float(box.conf[0])

            # Class
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Center point
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            current_positions[track_id] = (
                center_x,
                center_y
            )

            current_objects += 1

            # -------------------------
            # Check ROI
            # -------------------------
            inside_roi = (
                roi_x1 <= center_x <= roi_x2
                and
                roi_y1 <= center_y <= roi_y2
            )

            # -------------------------
            # Entry / Exit Detection
            # -------------------------
            if track_id in previous_positions:

                prev_x, prev_y = previous_positions[track_id]

                was_inside = (
                    roi_x1 <= prev_x <= roi_x2
                    and
                    roi_y1 <= prev_y <= roi_y2
                )

                # Outside → Inside
                if not was_inside and inside_roi:
                    entries += 1

                # Inside → Outside
                elif was_inside and not inside_roi:
                    exits += 1

            # -------------------------
            # Draw Bounding Box
            # -------------------------
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # -------------------------
            # Draw Tracking ID
            # -------------------------
            label = f"ID:{track_id} {class_name} {conf:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            # Center point
            cv2.circle(
                frame,
                (center_x, center_y),
                4,
                (0, 0, 255),
                -1
            )

    # -------------------------
    # Update Previous Positions
    # -------------------------
    previous_positions = current_positions

    # -------------------------
    # Draw ROI
    # -------------------------
    if show_roi:

        cv2.rectangle(
            frame,
            (roi_x1, roi_y1),
            (roi_x2, roi_y2),
            (255, 0, 0),
            3
        )

        cv2.putText(
            frame,
            "ROI",
            (roi_x1, roi_y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

    # -------------------------
    # Calculate FPS
    # -------------------------
    current_time = time.time()

    processing_time = current_time - start_time

    if processing_time > 0:
        fps = 1 / processing_time
    else:
        fps = 0

    # -------------------------
    # Draw Statistics
    # -------------------------
    cv2.rectangle(
        frame,
        (10, 10),
        (330, 120),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Objects: {current_objects}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Entries: {entries}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Exits: {exits}",
        (180, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # -------------------------
    # Display Frame
    # -------------------------
    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    video_area.image(
        frame_rgb,
        channels="RGB",
        use_container_width=True
    )

    # Update metrics
    fps_display.metric("FPS", f"{fps:.1f}")
    object_display.metric("Objects", current_objects)
    entry_display.metric("Entries", entries)
    exit_display.metric("Exits", exits)

# -----------------------------
# Release Video
# -----------------------------
cap.release()

st.success("✅ Video processing completed!")