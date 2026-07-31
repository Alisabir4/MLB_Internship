import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile
import os
import cv2


# Page Configuration

st.set_page_config(
    page_title="Road Sign Detection System",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Road Sign Detection System")
st.write("Upload an image or video to detect road signs using a custom YOLOv8 model.")


# Load Model

MODEL_PATH = r"D:\python\MLB_Internship\Day29\best.pt"

if not os.path.exists(MODEL_PATH):
    st.error(f"Model not found!\n\nExpected location:\n{MODEL_PATH}")
    st.stop()

model = YOLO(MODEL_PATH)


# Sidebar

st.sidebar.title("Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.1,
    1.0,
    0.5,
    0.05
)

input_type = st.sidebar.radio(
    "Choose Input Type",
    ["Image", "Video"]
)

# IMAGE DETECTION

if input_type == "Image":

    uploaded_image = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:

        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image, use_container_width=True)

        if st.button("Detect Objects"):

            results = model.predict(
                image,
                conf=confidence
            )

            annotated_image = results[0].plot()

            with col2:
                st.subheader("Detection Result")
                st.image(
                    annotated_image,
                    channels="BGR",
                    use_container_width=True
                )

            st.subheader("Detected Objects")

            boxes = results[0].boxes

            if len(boxes) == 0:
                st.warning("No objects detected.")

            else:
                for box in boxes:

                    class_id = int(box.cls[0])

                    class_name = model.names[class_id]

                    score = float(box.conf[0])

                    st.write(
                        f"**{class_name}** : {score:.2f}"
                    )

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
            )

            cv2.imwrite(
                temp_file.name,
                annotated_image
            )

            with open(temp_file.name, "rb") as file:

                st.download_button(
                    "⬇ Download Result",
                    file,
                    file_name="prediction.jpg",
                    mime="image/jpeg"
                )

# VIDEO DETECTION

else:

    uploaded_video = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_video is not None:

        temp_video = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        )

        temp_video.write(uploaded_video.read())

        st.video(temp_video.name)

        if st.button("Detect Objects in Video"):

            with st.spinner("Processing Video..."):

                results = model.predict(
                    source=temp_video.name,
                    conf=confidence,
                    save=True
                )

            st.success("Video Processed Successfully!")

            save_dir = results[0].save_dir

            output_video = None

            for file in os.listdir(save_dir):

                if file.endswith((".mp4", ".avi", ".mov")):
                    output_video = os.path.join(save_dir, file)
                    break

            if output_video:

                st.video(output_video)

                with open(output_video, "rb") as f:

                    st.download_button(
                        "⬇ Download Processed Video",
                        f,
                        file_name="prediction.mp4",
                        mime="video/mp4"
                    )

            else:
                st.info(
                    "Processed video saved in:\n\n"
                    f"{save_dir}"
                )

# Footer

st.markdown(
    """
    <div style="text-align: right; color: gray; font-size:16px;">
        Developed by <strong>Ali Sabir</strong>
    </div>
    """,
    unsafe_allow_html=True
)