import streamlit as st
import cv2
import pandas as pd
import tempfile
import os
from ultralytics import YOLO

st.set_page_config(page_title="Security Monitoring", layout="wide")
st.title("🛡️ Intelligent Security Monitoring System")

# ----------------- Load Model -----------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ----------------- Sidebar -----------------
conf = st.sidebar.slider("Confidence", 0.1, 1.0, 0.3, 0.05)

st.sidebar.subheader("ROI")
rx1 = st.sidebar.number_input("X1", value=200)
ry1 = st.sidebar.number_input("Y1", value=150)
rx2 = st.sidebar.number_input("X2", value=700)
ry2 = st.sidebar.number_input("Y2", value=500)

uploaded = st.file_uploader(
    "Upload Video",
    type=["mp4", "avi", "mov"]
)

frame_window = st.empty()

# ----------------- Variables -----------------
inside = {}
events = []
active = set()

os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ----------------- Helper Functions -----------------
def inside_roi(cx, cy):
    return rx1 < cx < rx2 and ry1 < cy < ry2


def sec_to_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    return f"{h:02}:{m:02}:{s:02}"


def draw_roi(frame):
    cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 255, 255), 2)
    cv2.putText(
        frame,
        "ROI",
        (rx1, ry1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )


# ----------------- Start -----------------
if uploaded and st.button("Process Video"):

    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(uploaded.read())

    cap = cv2.VideoCapture(tmp.name)

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path = "outputs/processed.mp4"

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    progress = st.progress(0)

    active_metric = st.empty()
    entry_metric = st.empty()
    exit_metric = st.empty()

    frame_no = 0

    # ========= PART 2 STARTS FROM HERE =========
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_no += 1
        current_time = frame_no / fps

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=conf,
            verbose=False
        )

        draw_roi(frame)

        if len(results) > 0:

            boxes = results[0].boxes

            if boxes is not None and boxes.id is not None:

                ids = boxes.id.cpu().numpy().astype(int)
                xyxy = boxes.xyxy.cpu().numpy()
                cls = boxes.cls.cpu().numpy()
                confs = boxes.conf.cpu().numpy()

                current_inside = set()

                for box, pid, c, cf in zip(xyxy, ids, cls, confs):

                    # Person class only
                    if int(c) != 0:
                        continue

                    x1, y1, x2, y2 = map(int, box)

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    is_inside = inside_roi(cx, cy)

                    color = (0, 255, 0)

                    if is_inside:
                        color = (0, 0, 255)
                        current_inside.add(pid)

                        if pid not in inside:
                            inside[pid] = current_time

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                    cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)

                    cv2.putText(
                        frame,
                        f"ID {pid}",
                        (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2
                    )

                # Detect Exit
                for pid in list(active):

                    if pid not in current_inside:

                        entry = inside.pop(pid)

                        events.append({
                            "Person_ID": pid,
                            "Entry_Time": sec_to_time(entry),
                            "Exit_Time": sec_to_time(current_time),
                            "Duration(sec)": round(current_time-entry, 2)
                        })

                active = current_inside.copy()

        cv2.putText(
            frame,
            f"Active : {len(active)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Entries : {len(inside)}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Logs : {len(events)}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        writer.write(frame)

        frame_window.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            channels="RGB",
            use_container_width=True
        )

        progress.progress(min(frame_no / total, 1.0))

        active_metric.metric("👤 Active People", len(active))
        entry_metric.metric("➡️ Inside", len(inside))
        exit_metric.metric("⬅️ Exited", len(events))

    cap.release()
    writer.release()

    csv_path = "logs/events.csv"

    pd.DataFrame(events).to_csv(csv_path, index=False)

    st.success("✅ Processing Completed")

    st.subheader("Event Logs")
    st.dataframe(pd.DataFrame(events), use_container_width=True)

    with open(output_path, "rb") as f:
        st.download_button(
            "⬇ Download Processed Video",
            f,
            file_name="processed.mp4"
        )

    with open(csv_path, "rb") as f:
        st.download_button(
            "⬇ Download CSV Log",
            f,
            file_name="events.csv"
        )