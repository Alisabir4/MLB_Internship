import cv2
import os
import tempfile
import gradio as gr
import spaces


@spaces.GPU
def process_video(video_path):

    if video_path is None:
        return None

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    output_path = os.path.join(
        tempfile.gettempdir(),
        "processed_video.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_no = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        blur = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        edges = cv2.Canny(
            blur,
            50,
            150
        )

        processed = cv2.cvtColor(
            edges,
            cv2.COLOR_GRAY2BGR
        )

        cv2.putText(
            processed,
            f"FPS: {fps}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            processed,
            f"Width: {width}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            processed,
            f"Height: {height}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            processed,
            f"Total Frames: {total_frames}",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            processed,
            f"Current Frame: {frame_no}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        out.write(processed)

    cap.release()
    out.release()

    return output_path


demo = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Upload Video"),
    outputs=gr.Video(label="Processed Video"),
    title="Real-Time Video Processing Tool",
    description="""
Upload a video to:

• Convert each frame to Grayscale

• Apply Gaussian Blur

• Apply Canny Edge Detection

• Display FPS, Width, Height, Total Frames and Current Frame

• Save and return the processed video

This application is designed for Hugging Face Spaces and is compatible with ZeroGPU.
""",
)

demo.launch()