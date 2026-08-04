import streamlit as st
import tempfile
import os
import cv2

from vehicle_counter import VehicleCounter

st.set_page_config(
    page_title="Smart Vehicle Counting System",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Smart Vehicle Counting System")

st.markdown(
    """
Detect, Track and Count **Cars**, **Motorcycles**, **Buses**, and **Trucks**
using **YOLOv8 + ByteTrack**.
"""
)

uploaded_file = st.file_uploader(
    "Upload a Traffic Video",
    type=["mp4", "avi", "mov", "mkv"]
)

if uploaded_file is not None:

    os.makedirs("output", exist_ok=True)

    temp_video = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_video.write(uploaded_file.read())
    temp_video.close()

    output_path = "output/counted_video.mp4"

    if st.button("▶ Start Vehicle Counting", use_container_width=True):

        counter = VehicleCounter("yolov8n.pt")

        st.divider()

        video_placeholder = st.empty()

        progress_bar = st.progress(0)

        status_text = st.empty()

        st.subheader("Live Statistics")

        col1, col2, col3, col4, col5 = st.columns(5)

        car_metric = col1.empty()
        bike_metric = col2.empty()
        bus_metric = col3.empty()
        truck_metric = col4.empty()
        total_metric = col5.empty()

        cap = cv2.VideoCapture(temp_video.name)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        cap.release()

        processed_frames = 0
                # -----------------------------
        # Live Processing Loop
        # -----------------------------
        for (
            frame,
            car,
            motorcycle,
            bus,
            truck,
            total
        ) in counter.process_video(
            temp_video.name,
            output_path
        ):

            processed_frames += 1

            # Display current processed frame
            video_placeholder.image(
                frame,
                channels="BGR",
                use_container_width=True
            )

            # Update metrics
            car_metric.metric("🚗 Cars", car)
            bike_metric.metric("🏍 Motorcycle", motorcycle)
            bus_metric.metric("🚌 Bus", bus)
            truck_metric.metric("🚚 Truck", truck)
            total_metric.metric("🚘 Total", total)

            # Progress Bar
            if total_frames > 0:

                progress = processed_frames / total_frames

                progress_bar.progress(
                    min(progress, 1.0)
                )

            status_text.info(
                f"Processing Frame {processed_frames} of {total_frames}"
            )

        progress_bar.progress(1.0)

        status_text.success(
            "✅ Vehicle Counting Completed Successfully!"
        )
                # -----------------------------------
        # Display Processed Video
        # -----------------------------------

        st.divider()

        st.subheader("🎥 Processed Video")

        if os.path.exists(output_path):

            st.video(output_path)

            with open(output_path, "rb") as video_file:

                st.download_button(
                    label="⬇ Download Processed Video",
                    data=video_file,
                    file_name="counted_video.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )

        else:

            st.error("Processed video not found.")

        # -----------------------------------
        # Clean Up Temporary File
        # -----------------------------------

        try:

            if os.path.exists(temp_video.name):

                os.remove(temp_video.name)

        except Exception:

            pass

        st.success("✅ Vehicle Counting Completed!")