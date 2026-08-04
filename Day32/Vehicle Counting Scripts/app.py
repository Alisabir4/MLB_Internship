import streamlit as st
import tempfile
import os
import cv2

from vehicle_counter import VehicleCounter

st.set_page_config(
    page_title="Vehicle Counting System",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Vehicle Counting using YOLOv8")

st.markdown("Detect • Track • Count Vehicles")

uploaded_file = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4", "avi", "mov"]
)

if uploaded_file is not None:

    os.makedirs("output", exist_ok=True)

    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_file.read())
    temp_video.close()

    output_path = "output/counted_video.mp4"

    if st.button("▶ Start Processing", use_container_width=True):

        counter = VehicleCounter("yolov8n.pt")

        # Live video placeholder
        video_placeholder = st.empty()

        # Progress bar
        progress_bar = st.progress(0)

        # Status
        status = st.empty()

        # Metrics
        col1, col2, col3 = st.columns(3)

        car_metric = col1.empty()
        truck_metric = col2.empty()
        total_metric = col3.empty()

        # Get video information
        cap = cv2.VideoCapture(temp_video.name)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        processed = 0

        for frame, car, truck, total in counter.process_video(
                temp_video.name,
                output_path
        ):

            processed += 1

            # Update live video
            video_placeholder.image(
                frame,
                channels="BGR",
                use_container_width=True
            )

            # Update metrics
            car_metric.metric("🚗 Cars", car)
            truck_metric.metric("🚚 Trucks", truck)
            total_metric.metric("🚘 Total", total)

            # Update progress
            if total_frames > 0:
                progress = processed / total_frames
                progress_bar.progress(min(progress, 1.0))

            status.info(
                f"Processing Frame {processed}/{total_frames}"
            )

        progress_bar.progress(1.0)

        status.success("✅ Processing Complete")

        st.success("Video Saved Successfully")

        st.subheader("Processed Video")

        st.video(output_path)

        with open(output_path, "rb") as file:

            st.download_button(
                "⬇ Download Processed Video",
                data=file,
                file_name="counted_video.mp4",
                mime="video/mp4",
                use_container_width=True
            )