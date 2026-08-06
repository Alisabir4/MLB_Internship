import os
import cv2
import time
import tempfile
import pandas as pd
import streamlit as st
from ultralytics import YOLO
from datetime import datetime

st.set_page_config(page_title="Intelligent Security Monitoring", layout="wide")

st.title("🛡️ Intelligent Security Monitoring System")

uploaded_video = st.file_uploader(
    "Upload a Video",
    type=["mp4", "avi", "mov", "mkv"]
)

confidence = st.slider(
    "Confidence Threshold",
    0.1,
    1.0,
    0.4,
    0.05
)

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

output_dir = "outputs"
snapshot_dir = os.path.join(output_dir, "snapshots")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(snapshot_dir, exist_ok=True)

events = []
inside_people = set()
entry_times = {}
stay_times = {}
track_states = {}

total_entries = 0
total_exits = 0
max_occupancy = 0

processed_video_path = os.path.join(output_dir, "processed_video.mp4")
csv_path = os.path.join(output_dir, "events.csv")
if uploaded_video is not None:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())

    cap = cv2.VideoCapture(tfile.name)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(
        processed_video_path,
        fourcc,
        fps,
        (width, height)
    )

    # -------- Hardcoded ROI --------
    roi_x1 = width // 4
    roi_y1 = height // 4

    roi_x2 = width * 3 // 4
    roi_y2 = height * 3 // 4

    frame_placeholder = st.empty()

    progress = st.progress(0)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_no = 0

    start_time = time.time()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_no += 1

        progress.progress(min(frame_no / total_frames, 1.0))

        cv2.rectangle(
            frame,
            (roi_x1, roi_y1),
            (roi_x2, roi_y2),
            (0, 255, 255),
            2
        )

        results = model.track(
            frame,
            persist=True,
            classes=[0],
            conf=confidence,
            verbose=False
        )

        if (
            len(results)
            and results[0].boxes.id is not None
        ):

            boxes = results[0].boxes.xyxy.cpu().numpy()

            ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box, track_id in zip(boxes, ids):

                x1, y1, x2, y2 = map(int, box)

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                inside = (
                    roi_x1 < cx < roi_x2
                    and
                    roi_y1 < cy < roi_y2
                )
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if track_id not in track_states:
                    track_states[track_id] = False

                # ---------------- ENTRY ----------------
                if inside and not track_states[track_id]:

                    track_states[track_id] = True

                    inside_people.add(track_id)

                    entry_times[track_id] = time.time()

                    total_entries += 1

                    max_occupancy = max(
                        max_occupancy,
                        len(inside_people)
                    )

                    events.append({
                        "Tracking ID": track_id,
                        "Event Type": "Entry",
                        "Timestamp": now
                    })

                    crop = frame[
                        max(0, y1):min(height, y2),
                        max(0, x1):min(width, x2)
                    ]

                    if crop.size > 0:
                        cv2.imwrite(
                            os.path.join(
                                snapshot_dir,
                                f"person_{track_id}.jpg"
                            ),
                            crop
                        )

                # ---------------- EXIT ----------------
                elif (not inside) and track_states[track_id]:

                    track_states[track_id] = False

                    if track_id in inside_people:
                        inside_people.remove(track_id)

                    total_exits += 1

                    stay = time.time() - entry_times.get(
                        track_id,
                        time.time()
                    )

                    stay_times[track_id] = stay

                    events.append({
                        "Tracking ID": track_id,
                        "Event Type": "Exit",
                        "Timestamp": now
                    })

                color = (0, 255, 0) if inside else (0, 0, 255)

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                cv2.circle(
                    frame,
                    (cx, cy),
                    4,
                    color,
                    -1
                )

                cv2.putText(
                    frame,
                    f"ID:{track_id}",
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )
        # -------- Live Statistics --------
        cv2.putText(
            frame,
            f"Inside: {len(inside_people)}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Entries: {total_entries}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,0,0),
            2
        )

        cv2.putText(
            frame,
            f"Exits: {total_exits}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,0,255),
            2
        )

        out.write(frame)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(
            frame_rgb,
            channels="RGB",
            use_container_width=True
        )

    cap.release()
    out.release()

    pd.DataFrame(events).to_csv(
        csv_path,
        index=False
    )

    average_time = (
        sum(stay_times.values()) / len(stay_times)
        if stay_times else 0
    )

    total_time = time.time() - start_time

    st.success("Processing Completed!")

    st.subheader("Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Entries", total_entries)
        st.metric("Total Exits", total_exits)
        st.metric("Maximum Occupancy", max_occupancy)

    with col2:
        st.metric("People Inside", len(inside_people))
        st.metric("Average Stay Time (sec)", round(average_time,2))
        st.metric("Processing Time (sec)", round(total_time,2))

    st.subheader("Stay Time")

    if stay_times:

        stay_df = pd.DataFrame({
            "Tracking ID": stay_times.keys(),
            "Stay Time (Seconds)": [
                round(v,2)
                for v in stay_times.values()
            ]
        })

        st.dataframe(
            stay_df,
            use_container_width=True
        )

    with open(processed_video_path, "rb") as f:
        st.download_button(
            "⬇ Download Processed Video",
            f,
            file_name="processed_video.mp4"
        )

    with open(csv_path, "rb") as f:
        st.download_button(
            "⬇ Download Events CSV",
            f,
            file_name="Events.csv"
        )