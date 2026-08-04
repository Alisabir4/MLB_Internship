import streamlit as st
import os
import tempfile

from vehicle_counter import VehicleCounter



# Page configuration

st.set_page_config(
    page_title="Smart Vehicle Counting System",
    page_icon="🚗",
    layout="wide"
)



st.title("🚗 Smart Vehicle Counting System")
st.write(
    "YOLOv8 + ByteTrack based vehicle detection, tracking and counting"
)



# Create folders

os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)



# Upload video

uploaded_video = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4","avi","mov"]
)



if uploaded_video is not None:


    input_path = os.path.join(
        "uploads",
        uploaded_video.name
    )


    with open(input_path,"wb") as f:
        f.write(uploaded_video.read())



    st.success("Video uploaded successfully")



    if st.button("🚀 Start Vehicle Counting"):


        output_path = os.path.join(
            "output",
            "processed_video.mp4"
        )


        with st.spinner(
            "Processing video... Please wait"
        ):


            counter = VehicleCounter(
                "yolov8n.pt"
            )


            counts = counter.process_video(
                input_path,
                output_path
            )



        st.success(
            "Processing completed!"
        )



        st.subheader("📊 Vehicle Count")


        col1,col2,col3,col4 = st.columns(4)


        with col1:
            st.metric(
                "Cars",
                counts["Car"]
            )


        with col2:
            st.metric(
                "Motorcycles",
                counts["Motorcycle"]
            )


        with col3:
            st.metric(
                "Buses",
                counts["Bus"]
            )


        with col4:
            st.metric(
                "Trucks",
                counts["Truck"]
            )



        st.subheader(
            "Processed Video"
        )


        # Display video

        st.video(
            output_path
        )



        # Download button


        with open(
            output_path,
            "rb"
        ) as video_file:


            st.download_button(
                label="⬇️ Download Processed Video",
                data=video_file,
                file_name="vehicle_count_result.mp4",
                mime="video/mp4"
            )