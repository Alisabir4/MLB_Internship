import os
import cv2
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

video_folder = r"D:\python\MLB_Internship\Day28\Sample Input Videos"
output_folder = r"D:\python\MLB_Internship\Day28\Output Images & Videos"

os.makedirs(output_folder, exist_ok=True)

video_extensions = (".mp4", ".avi", ".mov", ".mkv")

videos = [
    v for v in os.listdir(video_folder)
    if v.lower().endswith(video_extensions)
]

for video_name in videos:

    video_path = os.path.join(video_folder, video_name)

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = os.path.join(output_folder, video_name)

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    print(f"\nProcessing {video_name}")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)

        annotated = results[0].plot()

        writer.write(annotated)

    cap.release()
    writer.release()

print("\nAll videos processed successfully!")