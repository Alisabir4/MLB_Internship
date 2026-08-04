import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os

st.set_page_config(page_title="Smart Vehicle Counting System", layout="centered")

st.title(" Smart Vehicle Counting System")

st.write("Upload a traffic video to detect and count vehicles.")

# Load YOLO model
model = YOLO("yolov8n.pt")

uploaded_file = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4", "avi", "mov"]
)

if uploaded_file is not None:

    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_input.write(uploaded_file.read())
    temp_input.close()

    cap = cv2.VideoCapture(temp_input.name)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = "output.mp4"

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    line_y = height // 2

    vehicle_classes = {
        2: "Car",
        3: "Motorcycle",
        5: "Bus",
        7: "Truck"
    }

    counted_ids = set()

    total = 0

    progress = st.progress(0)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    processed = 0

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        cv2.line(frame, (0, line_y), (width, line_y), (0,255,255), 3)

        if results[0].boxes.id is not None:

            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy().astype(int)

            for box, track_id, cls in zip(boxes, ids, classes):

                if cls not in vehicle_classes:
                    continue

                x1, y1, x2, y2 = map(int, box)

                cx = (x1+x2)//2
                cy = (y1+y2)//2

                label = vehicle_classes[cls]

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

                cv2.putText(
                    frame,
                    f"{label} ID:{track_id}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )

                if abs(cy-line_y) < 5:

                    if track_id not in counted_ids:
                        counted_ids.add(track_id)
                        total += 1

        cv2.putText(
            frame,
            f"Total Vehicles: {total}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,0,0),
            3
        )

        writer.write(frame)

        processed += 1
        progress.progress(min(processed/frame_count,1.0))

    cap.release()
    writer.release()

    st.success(f"Processing Completed!\n\nTotal Vehicles Counted: {total}")

    st.video(output_path)

    with open(output_path,"rb") as file:
        st.download_button(
            "Download Processed Video",
            file,
            file_name="vehicle_counting_output.mp4"
        )

    os.remove(temp_input.name)