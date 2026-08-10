import os
import time
import tempfile

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from ultralytics import YOLO


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Video Analytics System",
    page_icon="🎥",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎥 Smart Video Analytics System")

st.caption(
    "AI-powered object detection, tracking, counting and ROI analytics"
)


# ============================================================
# LOAD YOLO MODEL
# ============================================================

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

st.sidebar.header("⚙️ Processing Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.40,
    step=0.05
)

resolution = st.sidebar.selectbox(
    "Processing Resolution",
    [640, 480],
    index=0
)

frame_skip = st.sidebar.selectbox(
    "Frame Skipping",
    [1, 2, 3],
    index=0,
    format_func=lambda x: (
        "Disabled" if x == 1
        else f"Process every {x}nd/rd frame"
    )
)


# ============================================================
# ROI SETTINGS
# ============================================================

st.sidebar.header("📍 ROI Settings")

roi_x1_percent = st.sidebar.slider(
    "ROI Left (%)",
    0,
    90,
    25
)

roi_y1_percent = st.sidebar.slider(
    "ROI Top (%)",
    0,
    90,
    25
)

roi_x2_percent = st.sidebar.slider(
    "ROI Right (%)",
    10,
    100,
    75
)

roi_y2_percent = st.sidebar.slider(
    "ROI Bottom (%)",
    10,
    100,
    75
)


# ============================================================
# VIDEO UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📤 Upload a traffic or people video",
    type=["mp4", "avi", "mov", "mkv"]
)


if uploaded_file is None:

    st.info(
        "Upload a short 15–30 second traffic or people video."
    )

    st.stop()


# ============================================================
# VIDEO INFORMATION
# ============================================================

st.subheader("🎬 Uploaded Video")

st.write(
    f"**File:** {uploaded_file.name}"
)

st.write(
    f"**Size:** {uploaded_file.size / (1024 * 1024):.2f} MB"
)


# ============================================================
# START BUTTON
# ============================================================

start_processing = st.button(
    "▶️ Start Video Analytics",
    type="primary",
    use_container_width=True
)


if not start_processing:

    st.info(
        "Configure the settings from the sidebar and click "
        "'Start Video Analytics'."
    )

    st.stop()


# ============================================================
# SAVE UPLOADED VIDEO TEMPORARILY
# ============================================================

suffix = os.path.splitext(
    uploaded_file.name
)[1]

temp_input = tempfile.NamedTemporaryFile(
    delete=False,
    suffix=suffix
)

temp_input.write(
    uploaded_file.getbuffer()
)

temp_input.close()

input_path = temp_input.name


# ============================================================
# OPEN VIDEO
# ============================================================

cap = cv2.VideoCapture(
    input_path
)

if not cap.isOpened():

    st.error(
        "❌ Unable to open the uploaded video."
    )

    os.remove(input_path)

    st.stop()


# ============================================================
# ORIGINAL VIDEO INFORMATION
# ============================================================

original_width = int(
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)

original_height = int(
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)

video_fps = cap.get(
    cv2.CAP_PROP_FPS
)

total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)

if video_fps <= 0:
    video_fps = 30.0


video_duration = (
    total_frames / video_fps
    if video_fps > 0
    else 0
)


# ============================================================
# DISPLAY VIDEO INFORMATION
# ============================================================

info_col1, info_col2, info_col3 = st.columns(3)

info_col1.metric(
    "Original Width",
    f"{original_width}px"
)

info_col2.metric(
    "Original Height",
    f"{original_height}px"
)

info_col3.metric(
    "Duration",
    f"{video_duration:.1f}s"
)


# ============================================================
# CALCULATE PROCESSING SIZE
# ============================================================

if original_width >= original_height:

    processing_width = resolution

    processing_height = int(
        original_height *
        resolution /
        original_width
    )

else:

    processing_height = resolution

    processing_width = int(
        original_width *
        resolution /
        original_height
    )


# Make dimensions even for video codecs
processing_width -= processing_width % 2
processing_height -= processing_height % 2


# ============================================================
# ROI COORDINATES
# ============================================================

roi_x1 = int(
    processing_width *
    roi_x1_percent /
    100
)

roi_y1 = int(
    processing_height *
    roi_y1_percent /
    100
)

roi_x2 = int(
    processing_width *
    roi_x2_percent /
    100
)

roi_y2 = int(
    processing_height *
    roi_y2_percent /
    100
)


# Safety check
if roi_x2 <= roi_x1:
    roi_x1 = int(processing_width * 0.25)
    roi_x2 = int(processing_width * 0.75)

if roi_y2 <= roi_y1:
    roi_y1 = int(processing_height * 0.25)
    roi_y2 = int(processing_height * 0.75)


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    "outputs",
    exist_ok=True
)

processed_video_path = (
    "outputs/processed_video.mp4"
)

events_csv_path = (
    "outputs/events.csv"
)


# ============================================================
# VIDEO WRITER
# ============================================================

fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)

writer = cv2.VideoWriter(
    processed_video_path,
    fourcc,
    video_fps,
    (
        processing_width,
        processing_height
    )
)

if not writer.isOpened():

    cap.release()

    st.error(
        "❌ Could not create the output video."
    )

    st.stop()


# ============================================================
# TRACKING VARIABLES
# ============================================================

unique_ids = set()

previous_inside_state = {}

current_inside_ids = set()

events = []

total_entries = 0
total_exits = 0

maximum_roi_objects = 0

fps_values = []

inference_times = []

frame_number = 0

processed_frames = 0

skipped_frames = 0

start_processing_time = time.time()


# ============================================================
# STREAMLIT DISPLAY
# ============================================================

st.subheader("📺 Live Processing")

video_placeholder = st.empty()

progress_bar = st.progress(0)

metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = (
    st.columns(5)
)

fps_metric = metric_col1.empty()
current_metric = metric_col2.empty()
unique_metric = metric_col3.empty()
entry_metric = metric_col4.empty()
exit_metric = metric_col5.empty()


# ============================================================
# VIDEO PROCESSING LOOP
# ============================================================

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    frame_number += 1

    # --------------------------------------------------------
    # RESIZE FRAME
    # --------------------------------------------------------

    frame = cv2.resize(
        frame,
        (
            processing_width,
            processing_height
        )
    )

    # --------------------------------------------------------
    # FRAME SKIPPING
    # --------------------------------------------------------

    should_process = (
        frame_number % frame_skip == 0
        or frame_number == 1
    )

    if not should_process:

        skipped_frames += 1

        # Write skipped frame without new detection
        writer.write(frame)

        # Show frame
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        video_placeholder.image(
            frame_rgb,
            channels="RGB",
            use_container_width=True
        )

        if total_frames > 0:

            progress_bar.progress(
                min(
                    frame_number / total_frames,
                    1.0
                )
            )

        continue

    # --------------------------------------------------------
    # START INFERENCE TIMER
    # --------------------------------------------------------

    inference_start = time.perf_counter()

    # --------------------------------------------------------
    # YOLO TRACKING
    # --------------------------------------------------------

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=confidence,
        verbose=False
    )

    inference_time = (
        time.perf_counter()
        - inference_start
    )

    inference_times.append(
        inference_time
    )

    processed_frames += 1

    result = results[0]

    current_objects = 0

    current_positions = {}

    current_inside_ids = set()

    # --------------------------------------------------------
    # PROCESS DETECTIONS
    # --------------------------------------------------------

    if result.boxes is not None:

        for box in result.boxes:

            if box.id is None:
                continue

            # -----------------------------------------------
            # TRACKING ID
            # -----------------------------------------------

            track_id = int(
                box.id[0]
            )

            unique_ids.add(
                track_id
            )

            # -----------------------------------------------
            # BOUNDING BOX
            # -----------------------------------------------

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # -----------------------------------------------
            # CONFIDENCE
            # -----------------------------------------------

            conf = float(
                box.conf[0]
            )

            # -----------------------------------------------
            # CLASS
            # -----------------------------------------------

            class_id = int(
                box.cls[0]
            )

            class_name = model.names[
                class_id
            ]

            # -----------------------------------------------
            # CENTER
            # -----------------------------------------------

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )

            current_positions[
                track_id
            ] = (
                center_x,
                center_y
            )

            current_objects += 1

            # -----------------------------------------------
            # ROI CHECK
            # -----------------------------------------------

            inside_roi = (
                roi_x1 <= center_x <= roi_x2
                and
                roi_y1 <= center_y <= roi_y2
            )

            if inside_roi:

                current_inside_ids.add(
                    track_id
                )

            # -----------------------------------------------
            # PREVIOUS ROI STATE
            # -----------------------------------------------

            was_inside = (
                previous_inside_state.get(
                    track_id,
                    False
                )
            )

            # -----------------------------------------------
            # ENTRY
            # -----------------------------------------------

            if (
                not was_inside
                and inside_roi
            ):

                total_entries += 1

                events.append({
                    "Frame": frame_number,
                    "Time_Seconds": round(
                        frame_number / video_fps,
                        2
                    ),
                    "Track_ID": track_id,
                    "Object": class_name,
                    "Event": "Entry",
                    "X": center_x,
                    "Y": center_y
                })

            # -----------------------------------------------
            # EXIT
            # -----------------------------------------------

            elif (
                was_inside
                and not inside_roi
            ):

                total_exits += 1

                events.append({
                    "Frame": frame_number,
                    "Time_Seconds": round(
                        frame_number / video_fps,
                        2
                    ),
                    "Track_ID": track_id,
                    "Object": class_name,
                    "Event": "Exit",
                    "X": center_x,
                    "Y": center_y
                })

            # -----------------------------------------------
            # SAVE CURRENT ROI STATE
            # -----------------------------------------------

            previous_inside_state[
                track_id
            ] = inside_roi

            # -----------------------------------------------
            # DRAW BOUNDING BOX
            # -----------------------------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # -----------------------------------------------
            # DRAW LABEL
            # -----------------------------------------------

            label = (
                f"ID:{track_id} "
                f"{class_name} "
                f"{conf:.2f}"
            )

            cv2.putText(
                frame,
                label,
                (
                    x1,
                    max(
                        y1 - 10,
                        20
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            # -----------------------------------------------
            # DRAW CENTER
            # -----------------------------------------------

            cv2.circle(
                frame,
                (
                    center_x,
                    center_y
                ),
                4,
                (0, 0, 255),
                -1
            )

    # ========================================================
    # ROI STATISTICS
    # ========================================================

    current_roi_objects = len(
        current_inside_ids
    )

    maximum_roi_objects = max(
        maximum_roi_objects,
        current_roi_objects
    )

    # --------------------------------------------------------
    # FPS
    # --------------------------------------------------------

    processing_time = (
        time.perf_counter()
        - inference_start
    )

    if processing_time > 0:

        current_fps = (
            1 / processing_time
        )

    else:

        current_fps = 0

    fps_values.append(
        current_fps
    )

    # ========================================================
    # DRAW ROI
    # ========================================================

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
        (
            roi_x1,
            max(
                roi_y1 - 10,
                25
            )
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2
    )

    # ========================================================
    # DRAW ANALYTICS PANEL
    # ========================================================

    panel_height = 170

    cv2.rectangle(
        frame,
        (10, 10),
        (390, panel_height),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        f"FPS: {current_fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Current Objects: {current_objects}",
        (20, 68),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Unique Objects: {len(unique_ids)}",
        (20, 96),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"ROI Objects: {current_roi_objects}",
        (20, 124),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Entry: {total_entries}",
        (210, 124),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Exit: {total_exits}",
        (210, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (255, 255, 255),
        2
    )

    # ========================================================
    # WRITE PROCESSED FRAME
    # ========================================================

    writer.write(
        frame
    )

    # ========================================================
    # DISPLAY FRAME
    # ========================================================

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    video_placeholder.image(
        frame_rgb,
        channels="RGB",
        use_container_width=True
    )

    # ========================================================
    # LIVE METRICS
    # ========================================================

    fps_metric.metric(
        "⚡ FPS",
        f"{current_fps:.1f}"
    )

    current_metric.metric(
        "Current Objects",
        current_objects
    )

    unique_metric.metric(
        "Unique Objects",
        len(unique_ids)
    )

    entry_metric.metric(
        "Entries",
        total_entries
    )

    exit_metric.metric(
        "Exits",
        total_exits
    )

    # ========================================================
    # PROGRESS
    # ========================================================

    if total_frames > 0:

        progress_bar.progress(
            min(
                frame_number / total_frames,
                1.0
            )
        )


# ============================================================
# RELEASE RESOURCES
# ============================================================

cap.release()

writer.release()


# ============================================================
# PROCESSING TIME
# ============================================================

total_processing_time = (
    time.time()
    - start_processing_time
)


# ============================================================
# AVERAGE FPS
# ============================================================

if fps_values:

    average_fps = float(
        np.mean(fps_values)
    )

else:

    average_fps = 0.0


# ============================================================
# AVERAGE INFERENCE TIME
# ============================================================

if inference_times:

    average_inference_ms = (
        np.mean(inference_times)
        * 1000
    )

else:

    average_inference_ms = 0.0


# ============================================================
# SAVE EVENTS CSV
# ============================================================

events_df = pd.DataFrame(
    events
)

if events_df.empty:

    events_df = pd.DataFrame(
        columns=[
            "Frame",
            "Time_Seconds",
            "Track_ID",
            "Object",
            "Event",
            "X",
            "Y"
        ]
    )


events_df.to_csv(
    events_csv_path,
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

st.success(
    "✅ Video processing completed successfully!"
)

st.subheader(
    "📊 Final Analytics Summary"
)


summary_col1, summary_col2, summary_col3 = (
    st.columns(3)
)

summary_col1.metric(
    "Total Objects",
    len(unique_ids)
)

summary_col2.metric(
    "Total Entries",
    total_entries
)

summary_col3.metric(
    "Total Exits",
    total_exits
)


summary_col4, summary_col5, summary_col6 = (
    st.columns(3)
)

summary_col4.metric(
    "Maximum Objects in ROI",
    maximum_roi_objects
)

summary_col5.metric(
    "Average FPS",
    f"{average_fps:.1f}"
)

summary_col6.metric(
    "Processing Time",
    f"{total_processing_time:.1f}s"
)


# ============================================================
# PERFORMANCE INFORMATION
# ============================================================

st.subheader(
    "⚡ Performance Test"
)

performance_data = pd.DataFrame({
    "Setting": [
        "Resolution",
        "Frame Skip",
        "Processed Frames",
        "Skipped Frames",
        "Average FPS",
        "Average Inference Time"
    ],
    "Value": [
        f"{resolution}px",
        (
            "Disabled"
            if frame_skip == 1
            else f"Every {frame_skip} frames"
        ),
        processed_frames,
        skipped_frames,
        f"{average_fps:.2f}",
        f"{average_inference_ms:.2f} ms"
    ]
})

st.table(
    performance_data
)


# ============================================================
# EVENTS
# ============================================================

st.subheader(
    "📋 Entry / Exit Events"
)

if events_df.empty:

    st.info(
        "No entry or exit events were detected."
    )

else:

    st.dataframe(
        events_df,
        use_container_width=True
    )


# ============================================================
# DOWNLOAD SECTION
# ============================================================

st.subheader(
    "📥 Download Results"
)


# ------------------------------------------------------------
# DOWNLOAD CSV
# ------------------------------------------------------------

with open(
    events_csv_path,
    "rb"
) as csv_file:

    st.download_button(
        label="📄 Download events.csv",
        data=csv_file,
        file_name="events.csv",
        mime="text/csv",
        use_container_width=True
    )


# ------------------------------------------------------------
# DOWNLOAD PROCESSED VIDEO
# ------------------------------------------------------------

if os.path.exists(
    processed_video_path
):

    with open(
        processed_video_path,
        "rb"
    ) as video_file:

        st.download_button(
            label="🎥 Download Processed Video",
            data=video_file,
            file_name="processed_video.mp4",
            mime="video/mp4",
            use_container_width=True
        )

    # --------------------------------------------------------
    # SHOW PROCESSED VIDEO
    # --------------------------------------------------------

    st.subheader(
        "🎬 Processed Video"
    )

    st.video(
        processed_video_path
    )


# ============================================================
# CLEAN TEMP INPUT
# ============================================================

try:

    os.remove(
        input_path
    )

except Exception:
    pass