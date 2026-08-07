import os
import cv2
import time
import tempfile
import numpy as np
import pandas as pd
import streamlit as st

from ultralytics import YOLO
from datetime import datetime


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Intelligent Security Monitoring",
    page_icon="🛡️",
    layout="wide"
)


st.title("🛡️ Intelligent Security Monitoring System")

st.markdown(
"""
Detect and Track People using **YOLOv8 + ByteTrack**

Features:
- Person Detection
- Object Tracking
- ROI Monitoring
- Entry / Exit Counting
- Occupancy Monitoring
- Stay Time Analysis
- CSV Reports
- Download Results
"""
)


# ---------------- SIDEBAR ----------------

st.sidebar.header("⚙ Settings")


uploaded_file = st.sidebar.file_uploader(
    "Upload Image or Video",
    type=[
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "mp4",
        "avi",
        "mov",
        "mkv"
    ]
)


confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.1,
    1.0,
    0.4,
    0.05
)


iou = st.sidebar.slider(
    "IoU Threshold",
    0.1,
    1.0,
    0.45,
    0.05
)


show_roi = st.sidebar.checkbox(
    "Show ROI",
    True
)


save_snapshots = st.sidebar.checkbox(
    "Save Snapshots",
    True
)



# ---------------- MODEL ----------------

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")


model = load_model()



# ---------------- OUTPUT PATHS ----------------

OUTPUT_DIR = "outputs"

SNAPSHOT_DIR = os.path.join(
    OUTPUT_DIR,
    "snapshots"
)


os.makedirs(
    SNAPSHOT_DIR,
    exist_ok=True
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


VIDEO_OUTPUT = os.path.join(
    OUTPUT_DIR,
    "processed_video.mp4"
)


IMAGE_OUTPUT = os.path.join(
    OUTPUT_DIR,
    "processed_image.jpg"
)


CSV_OUTPUT = os.path.join(
    OUTPUT_DIR,
    "events.csv"
)



# ---------------- VARIABLES ----------------

events = []

inside_people = set()

entry_times = {}

stay_times = {}

track_states = {}


total_entries = 0

total_exits = 0

max_occupancy = 0


processing_time = 0

frame_no = 0

fps = 0



# ---------------- DASHBOARD ----------------


col1, col2, col3, col4 = st.columns(4)


people_metric = col1.empty()

entry_metric = col2.empty()

exit_metric = col3.empty()

occupancy_metric = col4.empty()


display_area = st.empty()

progress_bar = st.progress(0)

status = st.empty()



# ---------------- FILE CHECK ----------------

if uploaded_file is None:

    st.info(
        "📂 Upload an image or video to start."
    )

    st.stop()



extension = uploaded_file.name.split(".")[-1].lower()


IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png",
    "bmp"
]


VIDEO_TYPES = [
    "mp4",
    "avi",
    "mov",
    "mkv"
]
# ---------------- ROI FUNCTION ----------------

def get_roi(width, height):

    return (
        width // 4,
        height // 4,
        width * 3 // 4,
        height * 3 // 4
    )



# ---------------- SAVE SNAPSHOT ----------------

def save_snapshot(frame, x1, y1, x2, y2, name):

    if not save_snapshots:
        return

    crop = frame[
        max(0,y1):min(frame.shape[0],y2),
        max(0,x1):min(frame.shape[1],x2)
    ]

    if crop.size:

        cv2.imwrite(
            os.path.join(
                SNAPSHOT_DIR,
                name
            ),
            crop
        )



# ---------------- IMAGE PROCESSING ----------------

def process_image(file):

    image = cv2.imdecode(
        np.frombuffer(
            file.read(),
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )


    if image is None:

        st.error(
            "Cannot read image"
        )

        return


    h,w = image.shape[:2]


    rx1,ry1,rx2,ry2 = get_roi(
        w,
        h
    )


    if show_roi:

        cv2.rectangle(
            image,
            (rx1,ry1),
            (rx2,ry2),
            (0,255,255),
            2
        )


    results = model.predict(
        image,
        classes=[0],
        conf=confidence,
        iou=iou,
        verbose=False
    )


    count = 0


    for r in results:

        for box in r.boxes:

            count += 1


            x1,y1,x2,y2 = map(
                int,
                box.xyxy[0]
            )


            conf = float(
                box.conf[0]
            )


            color = (
                (0,255,0)
            )


            cv2.rectangle(
                image,
                (x1,y1),
                (x2,y2),
                color,
                2
            )


            cv2.putText(
                image,
                f"Person {conf:.2f}",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )


            events.append(
                {
                    "Person":count,
                    "Confidence":round(conf,2)
                }
            )


            save_snapshot(
                image,
                x1,
                y1,
                x2,
                y2,
                f"person_{count}.jpg"
            )



    cv2.imwrite(
        IMAGE_OUTPUT,
        image
    )


    people_metric.metric(
        "Detected People",
        count
    )


    display_area.image(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        ),
        channels="RGB"
    )



# ---------------- VIDEO PROCESSING ----------------

def process_video(file):

    global total_entries
    global total_exits
    global max_occupancy
    global processing_time
    global fps
    global frame_no


    temp = tempfile.NamedTemporaryFile(
        delete=False
    )

    temp.write(
        file.read()
    )


    cap = cv2.VideoCapture(
        temp.name
    )


    if not cap.isOpened():

        st.error(
            "Cannot open video"
        )

        return



    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )


    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )


    fps = cap.get(
        cv2.CAP_PROP_FPS
    )


    if fps == 0:

        fps = 30



    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )


    rx1,ry1,rx2,ry2 = get_roi(
        width,
        height
    )


    writer = cv2.VideoWriter(
        VIDEO_OUTPUT,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width,height)
    )


    start = time.time()


    while True:


        ret,frame = cap.read()


        if not ret:
            break


        frame_no += 1


        progress_bar.progress(
            min(
                frame_no/total_frames,
                1
            )
        )


        if show_roi:

            cv2.rectangle(
                frame,
                (rx1,ry1),
                (rx2,ry2),
                (0,255,255),
                2
            )


        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            conf=confidence,
            iou=iou,
            verbose=False
        )


        if results[0].boxes.id is not None:

            boxes = results[0].boxes.xyxy.cpu().numpy()

            ids = results[0].boxes.id.cpu().numpy().astype(int)

            confs = results[0].boxes.conf.cpu().numpy()


            for box,track_id,conf in zip(
                boxes,
                ids,
                confs
            ):


                x1,y1,x2,y2 = map(
                    int,
                    box
                )


                cx = (x1+x2)//2

                cy = (y1+y2)//2


                inside = (
                    rx1 < cx < rx2
                    and
                    ry1 < cy < ry2
                )


                if track_id not in track_states:

                    track_states[track_id] = False



                if inside and not track_states[track_id]:


                    track_states[track_id]=True

                    inside_people.add(
                        track_id
                    )

                    entry_times[track_id]=time.time()

                    total_entries += 1

                    max_occupancy=max(
                        max_occupancy,
                        len(inside_people)
                    )



                elif not inside and track_states[track_id]:


                    track_states[track_id]=False

                    inside_people.discard(
                        track_id
                    )

                    total_exits += 1


                    stay_times[track_id]=(
                        time.time()
                        -
                        entry_times.get(
                            track_id,
                            time.time()
                        )
                    )


                cv2.rectangle(
                    frame,
                    (x1,y1),
                    (x2,y2),
                    (0,255,0),
                    2
                )


                cv2.putText(
                    frame,
                    f"ID:{track_id}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )


        writer.write(frame)


        display_area.image(
            cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )
        )


    cap.release()

    writer.release()


    processing_time = (
        time.time()-start
    )
# ---------------- RUN PROCESSING ----------------

if extension in IMAGE_TYPES:

    with st.spinner("Processing Image..."):

        process_image(
            uploaded_file
        )


elif extension in VIDEO_TYPES:

    status.info(
        "📹 Processing Video..."
    )

    process_video(
        uploaded_file
    )

    status.success(
        "✅ Video Processing Completed"
    )


else:

    st.error(
        "Unsupported file format"
    )



# ---------------- SAVE CSV REPORT ----------------

events_df = pd.DataFrame(
    events
)


if not events_df.empty:

    events_df.to_csv(
        CSV_OUTPUT,
        index=False
    )

else:

    pd.DataFrame(
        columns=[
            "Frame",
            "Tracking ID",
            "Event",
            "Confidence",
            "Timestamp"
        ]
    ).to_csv(
        CSV_OUTPUT,
        index=False
    )



# ---------------- FINAL DASHBOARD ----------------

st.markdown("---")

st.header(
    "📊 Monitoring Summary"
)


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Total Entries",
    total_entries
)


c2.metric(
    "Total Exits",
    total_exits
)


c3.metric(
    "Current Occupancy",
    len(inside_people)
)


c4.metric(
    "Max Occupancy",
    max_occupancy
)



# ---------------- STAY TIME ----------------

if stay_times:

    st.subheader(
        "🕒 Stay Time Analysis"
    )


    stay_df = pd.DataFrame(
        {
            "Tracking ID":
            list(stay_times.keys()),

            "Stay Time Seconds":
            [
                round(x,2)
                for x in stay_times.values()
            ]
        }
    )


    st.dataframe(
        stay_df,
        use_container_width=True
    )



# ---------------- EVENT TABLE ----------------

if not events_df.empty:

    st.subheader(
        "📄 Event Report"
    )


    st.dataframe(
        events_df,
        use_container_width=True
    )



# ---------------- DOWNLOADS ----------------

st.markdown("---")

st.subheader(
    "⬇ Download Results"
)


d1,d2 = st.columns(2)



if extension in VIDEO_TYPES:

    with d1:

        if os.path.exists(VIDEO_OUTPUT):

            with open(
                VIDEO_OUTPUT,
                "rb"
            ) as f:

                st.download_button(
                    "⬇ Download Processed Video",
                    f,
                    "processed_video.mp4",
                    "video/mp4"
                )


else:

    with d1:

        if os.path.exists(IMAGE_OUTPUT):

            with open(
                IMAGE_OUTPUT,
                "rb"
            ) as f:

                st.download_button(
                    "⬇ Download Processed Image",
                    f,
                    "processed_image.jpg",
                    "image/jpeg"
                )



with d2:

    if os.path.exists(CSV_OUTPUT):

        with open(
            CSV_OUTPUT,
            "rb"
        ) as f:

            st.download_button(
                "⬇ Download CSV Report",
                f,
                "events.csv",
                "text/csv"
            )



# ---------------- SNAPSHOTS ----------------

if save_snapshots:

    snapshots = len(
        os.listdir(
            SNAPSHOT_DIR
        )
    )


    st.success(
        f"📸 Snapshots Saved: {snapshots}"
    )



# ---------------- SIDEBAR INFO ----------------

st.sidebar.markdown("---")

st.sidebar.info(
"""
**Project**
Intelligent Security Monitoring

**Model**
YOLOv8 Nano

**Tracker**
ByteTrack

**Framework**
Streamlit

**Developer**
Ali Sabir
"""
)