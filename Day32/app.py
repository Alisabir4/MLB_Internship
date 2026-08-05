import os
import cv2
import streamlit as st
from people_counter import PeopleCounter

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="👥 Smart People Counting System",
    page_icon="👥",
    layout="wide"
)

# -----------------------------
# Folders
# -----------------------------
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙️ Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.10,
    1.00,
    0.30,
    0.05
)

mode = st.sidebar.radio(
    "Choose Input Type",
    ["Image", "Video"]
)

counter = PeopleCounter(conf=confidence)

# -----------------------------
# Title
# -----------------------------
st.title("👥 Smart People Counting System")

st.markdown("""
Detect and count people using **YOLOv8 + ByteTrack**

### Features
- 📷 Image Detection
- 🎥 Video Detection
- 🆔 Person Tracking
- 📊 Live People Count
- 📈 Peak Occupancy
- 💾 Download Processed Output
""")
# ===================================================
# IMAGE MODE
# ===================================================
if mode == "Image":

    uploaded_image = st.file_uploader(
        "Upload an Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:

        image_path = os.path.join(
            UPLOAD_DIR,
            uploaded_image.name
        )

        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image_path, use_container_width=True)

        if st.button("🔍 Detect People"):

            output_path = os.path.join(
                OUTPUT_DIR,
                "processed_image.jpg"
            )

            image, people_count = counter.process_image(
                image_path,
                output_path
            )

            with col2:
                st.subheader("Processed Image")

                st.image(
                    cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                    use_container_width=True
                )

            st.metric(
                "People Detected",
                people_count
            )

            with open(output_path, "rb") as file:

                st.download_button(
                    "⬇ Download Image",
                    file,
                    file_name="people_detection.jpg",
                    mime="image/jpeg"
                )
                # ===================================================
# VIDEO MODE
# ===================================================
elif mode == "Video":

    uploaded_video = st.file_uploader(
        "Upload a Video",
        type=["mp4", "avi", "mov", "mkv"]
    )

    if uploaded_video:

        video_path = os.path.join(
            UPLOAD_DIR,
            uploaded_video.name
        )

        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

        st.subheader("Original Video")
        st.video(video_path)

        if st.button("🎥 Start Detection"):

            output_path = os.path.join(
                OUTPUT_DIR,
                "processed_video.mp4"
            )

            # UI placeholders
            video_placeholder = st.empty()

            col1, col2 = st.columns(2)

            with col1:
                people_metric = st.empty()

            with col2:
                peak_metric = st.empty()

            progress = st.progress(0)

            # Get total frames
            cap = cv2.VideoCapture(video_path)

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            cap.release()

            frame_no = 0

            # Live processing
            for frame, people_count, peak_people in counter.process_video_live(
                video_path,
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

                people_metric.metric(
                    "Current People",
                    people_count
                )

                peak_metric.metric(
                    "Peak Occupancy",
                    peak_people
                )

                if total_frames > 0:

                    progress.progress(
                        min(frame_no / total_frames, 1.0)
                    )

            progress.empty()

            st.success("✅ Video Processing Completed!")

            st.subheader("Processed Video")

            st.video(output_path)

            with open(output_path, "rb") as file:

                st.download_button(
                    "⬇ Download Processed Video",
                    file,
                    file_name="people_detection.mp4",
                    mime="video/mp4"
                )