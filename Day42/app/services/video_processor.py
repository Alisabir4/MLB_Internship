import cv2
import time
from pathlib import Path

from app.services.detector import detector


def process_video(
    input_path: str,
    output_path: str,
    progress_callback=None,
):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise ValueError(
            "Unable to open video file. The video may be corrupted or unsupported."
        )

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if total_frames <= 0:
        cap.release()
        raise ValueError("Video contains no frames.")

    if fps <= 0:
        fps = 25.0

    if width <= 0 or height <= 0:
        cap.release()
        raise ValueError("Invalid video dimensions.")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        cap.release()
        raise ValueError("Unable to create output video.")

    processed_frames = 0
    total_detections = 0
    start_time = time.time()

    try:
        while True:
            success, frame = cap.read()

            if not success:
                break

            results = detector.predict(frame)

            detection_count = 0

            for result in results:
                if result.boxes is not None:
                    detection_count += len(result.boxes)

                frame = result.plot()

            processed_frames += 1
            total_detections += detection_count

            cv2.putText(
                frame,
                f"Frame: {processed_frames}/{total_frames}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            progress = int(
                (processed_frames / total_frames) * 100
            )

            if progress_callback:
                progress_callback(progress)

            writer.write(frame)

    finally:
        cap.release()
        writer.release()

    processing_time = time.time() - start_time

    average_fps = (
        processed_frames / processing_time
        if processing_time > 0
        else 0
    )

    return {
        "total_frames": total_frames,
        "processed_frames": processed_frames,
        "total_detections": total_detections,
        "average_fps": round(average_fps, 2),
        "processing_time": round(processing_time, 2),
    }