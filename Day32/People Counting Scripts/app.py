import os
import cv2
import streamlit as st
from people_counter import PeopleCounter

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Smart People Counting System",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Smart People Counting System")
st.markdown(
    """
Upload a video to:
- Detect People
- Track IDs
- Display Live Count
- Save Processed Video
"""
)

# -------------------------------
# Create folders
# -------------------------------
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("Settings")

confidence = st.sidebar.slider(
    "Confidence",
    0.10,
    1.00,
    0.30,
    0.05
)

uploaded_file = st.file_uploader(
    "Upload Video",
    type=["mp4", "avi", "mov", "mkv"]
)

if uploaded_file:

    input_path = os.path.join(
        UPLOAD_DIR,
        uploaded_file.name
    )

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.subheader("Original Video")
    st.video(input_path)

    if st.button("🚀 Start Live Detection"):

        output_path = os.path.join(
            OUTPUT_DIR,
            "processed_people.mp4"
        )

        counter = PeopleCounter(
            conf=confidence
        )

        st.subheader("Live Detection")

        video_placeholder = st.empty()
        count_placeholder = st.empty()
        progress_bar = st.progress(0)

        cap = cv2.VideoCapture(input_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        frame_no = 0

        for frame, people_count in counter.process_video_live(
            input_path,
            output_path
        ):

            frame_no += 1

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            video_placeholder.image(
                rgb,
                channels="RGB",
                use_container_width=True
            )

            count_placeholder.metric(
                "People Count",
                people_count
            )

            if total_frames > 0:
                progress_bar.progress(
                    min(frame_no / total_frames, 1.0)
                )

        progress_bar.empty()

        st.success("✅ Processing Complete!")

        st.subheader("Processed Video")

        st.video(output_path)

        with open(output_path, "rb") as file:
            st.download_button(
                label="⬇ Download Processed Video",
                data=file,
                file_name="people_count.mp4",
                mime="video/mp4"
            )