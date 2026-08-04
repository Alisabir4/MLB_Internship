import streamlit as st
import tempfile
import os
import numpy as np

from vehicle_counter import VehicleCounter


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Smart Vehicle Counting System",
    page_icon="🚗",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("🚗 Smart Vehicle Counting System")
st.write(
    "YOLOv8 + ByteTrack based Vehicle Detection, Tracking and Counting"
)


# -----------------------------
# Upload Video
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4", "avi", "mov"]
)


if uploaded_file:


    # Save uploaded video temporarily

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_file.write(
        uploaded_file.read()
    )

    input_path = temp_file.name


    # Output folder

    os.makedirs(
        "output",
        exist_ok=True
    )


    output_path = "output/vehicle_counted_video.mp4"



    if st.button(
        "▶ Start Vehicle Counting",
        use_container_width=True
    ):


        counter = VehicleCounter(
            "yolov8n.pt"
        )


        # -----------------------------
        # UI Containers
        # -----------------------------

        video_placeholder = st.empty()

        status = st.empty()

        progress = st.progress(0)


        col1, col2, col3, col4, col5 = st.columns(5)


        car_box = col1.empty()
        motorcycle_box = col2.empty()
        bus_box = col3.empty()
        truck_box = col4.empty()
        total_box = col5.empty()



        # -----------------------------
        # Processing
        # -----------------------------

        frame_number = 0


        for (
            frame,
            cars,
            motorcycles,
            buses,
            trucks,
            total

        ) in counter.process_video(
            input_path,
            output_path
        ):


            frame_number += 1


            # Show live frame

            

            if frame is None:
                st.error("Frame is None")
                st.stop()

            st.write(type(frame))

            if not isinstance(frame, np.ndarray):
                st.error(f"Invalid frame type: {type(frame)}")
                st.stop()

            video_placeholder.image(
                frame,
                channels="BGR",
                use_container_width=True,
            )


            # Update statistics

            car_box.metric(
                "🚗 Cars",
                cars
            )

            motorcycle_box.metric(
                "🏍 Motorcycles",
                motorcycles
            )

            bus_box.metric(
                "🚌 Buses",
                buses
            )

            truck_box.metric(
                "🚚 Trucks",
                trucks
            )

            total_box.metric(
                "🚘 Total",
                total
            )


            status.info(
                f"Processing Frame: {frame_number}"
            )


            # Simple progress animation

            progress.progress(
                min(frame_number % 100 / 100, 1.0)
            )



        status.success(
            "✅ Processing Completed"
        )


        progress.progress(1.0)



        # -----------------------------
        # Final Video
        # -----------------------------

        st.subheader(
            "Processed Video"
        )


        st.video(
            output_path
        )


        with open(
            output_path,
            "rb"
        ) as file:


            st.download_button(

                label="⬇ Download Processed Video",

                data=file,

                file_name="vehicle_counted_video.mp4",

                mime="video/mp4",

                use_container_width=True
            )



else:

    st.info(
        "Please upload a traffic video to start."
    )