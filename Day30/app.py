import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os
import time
from collections import defaultdict


# -------------------------------------------------
# Page Setup
# -------------------------------------------------

st.set_page_config(
    page_title="Smart Object Tracking System",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Smart Object Tracking System")

st.write(
    """
YOLOv8 Object Detection + Tracking

Features:
- Object Detection
- Object Tracking IDs
- Confidence Score
- Unique Object Count
- ByteTrack / BoT-SORT
"""
)


# -------------------------------------------------
# Load Model
# -------------------------------------------------

@st.cache_resource
def load_model():

    return YOLO("yolov8n.pt")


model = load_model()


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("Settings")


tracker_name = st.sidebar.selectbox(
    "Tracker",
    [
        "ByteTrack",
        "BoT-SORT"
    ]
)


confidence = st.sidebar.slider(
    "Confidence",
    0.1,
    1.0,
    0.3,
    0.05
)


tracker = (
    "bytetrack.yaml"
    if tracker_name == "ByteTrack"
    else "botsort.yaml"
)


# -------------------------------------------------
# Upload Video
# -------------------------------------------------

uploaded_video = st.file_uploader(
    "Upload Video",
    type=[
        "mp4",
        "avi",
        "mov",
        "mkv"
    ]
)


if uploaded_video:


    temp_input = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )


    temp_input.write(
        uploaded_video.read()
    )

    temp_input.close()


    input_path = temp_input.name


    st.video(input_path)


    start = st.button(
        "🚀 Start Tracking"
    )


    if start:


        output_path = os.path.join(
            tempfile.gettempdir(),
            f"tracked_{int(time.time())}.mp4"
        )


        cap = cv2.VideoCapture(
            input_path
        )


        fps = cap.get(
            cv2.CAP_PROP_FPS
        )


        if fps == 0:
            fps = 30


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


        # Try browser compatible codec

        writer = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(
                *"avc1"
            ),
            fps,
            (width,height)
        )


        if not writer.isOpened():

            writer = cv2.VideoWriter(
                output_path,
                cv2.VideoWriter_fourcc(
                    *"mp4v"
                ),
                fps,
                (width,height)
            )


        placeholder = st.empty()


        progress = st.progress(0)


        total_frames = int(
            cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )


        frame_count = 0


        unique_ids = set()

        class_ids = defaultdict(set)


        st.info(
            "Tracking started..."
        )


        while True:


            success, frame = cap.read()


            if not success:
                break



            results = model.track(
                frame,
                persist=True,
                tracker=tracker,
                conf=confidence,
                verbose=False
            )



            annotated = frame.copy()



            if (
                results[0].boxes.id
                is not None
            ):


                boxes = (
                    results[0]
                    .boxes
                    .xyxy
                    .cpu()
                    .numpy()
                )


                ids = (
                    results[0]
                    .boxes
                    .id
                    .cpu()
                    .numpy()
                    .astype(int)
                )


                classes = (
                    results[0]
                    .boxes
                    .cls
                    .cpu()
                    .numpy()
                    .astype(int)
                )


                scores = (
                    results[0]
                    .boxes
                    .conf
                    .cpu()
                    .numpy()
                )



                for box, obj_id, cls, score in zip(
                    boxes,
                    ids,
                    classes,
                    scores
                ):


                    x1,y1,x2,y2 = map(
                        int,
                        box
                    )


                    name = model.names[
                        int(cls)
                    ]


                    unique_ids.add(
                        obj_id
                    )


                    class_ids[name].add(
                        obj_id
                    )


                    label = (
                        f"{name} "
                        f"ID:{obj_id} "
                        f"{score:.2f}"
                    )


                    cv2.rectangle(
                        annotated,
                        (x1,y1),
                        (x2,y2),
                        (0,255,0),
                        2
                    )


                    cv2.putText(
                        annotated,
                        label,
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,255,0),
                        2
                    )



            writer.write(
                annotated
            )


            placeholder.image(
                annotated,
                channels="BGR",
                use_container_width=True
            )



            frame_count += 1


            if total_frames:

                progress.progress(
                    min(
                        frame_count / total_frames,
                        1.0
                    )
                )


        cap.release()

        writer.release()


        progress.empty()


        st.success(
            "✅ Tracking Completed"
        )


        # ---------------------------
        # Summary
        # ---------------------------


        st.subheader(
            "📊 Tracking Summary"
        )


        col1,col2 = st.columns(2)


        col1.metric(
            "Unique Objects",
            len(unique_ids)
        )


        col2.metric(
            "Frames",
            frame_count
        )


        st.subheader(
            "Object Counts"
        )


        table=[]


        for k,v in class_ids.items():

            table.append(
                {
                    "Object":k,
                    "Count":len(v)
                }
            )


        st.table(table)



        # ---------------------------
        # Final Video
        # ---------------------------


        st.subheader(
            "🎥 Processed Video"
        )


        if os.path.exists(output_path):


            with open(
                output_path,
                "rb"
            ) as f:

                video_bytes=f.read()



            st.video(
                video_bytes
            )


            st.download_button(
                "📥 Download Video",
                video_bytes,
                "tracked_output.mp4",
                "video/mp4"
            )



        else:

            st.error(
                "Video not created"
            )

else:

    st.info(
        "Upload a video to start"
    )