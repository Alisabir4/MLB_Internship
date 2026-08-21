import cv2
import time
import logging
from pathlib import Path

from app.services.detector import detector


logger = logging.getLogger("ai_video_api")


def process_video(
    input_path: str,
    output_path: str,
    progress_callback=None,
    confidence: float = 0.25,
    job_id: str = "unknown",
):
    """
    Process a video using YOLO and save the annotated result.
    """

    start_time = time.time()

    logger.info(
        f"Video processing started | "
        f"job_id={job_id} "
        f"confidence={confidence}"
    )

    # --------------------------------------------------
    # Open input video
    # --------------------------------------------------

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():

        logger.error(
            f"Unable to open video | "
            f"job_id={job_id}"
        )

        raise ValueError(
            "Unable to open video file. "
            "The video may be corrupted or unsupported."
        )

    # --------------------------------------------------
    # Read video information
    # --------------------------------------------------

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    # --------------------------------------------------
    # Validate video information
    # --------------------------------------------------

    if total_frames <= 0:

        cap.release()

        raise ValueError(
            "Video contains no frames."
        )

    if fps <= 0:

        fps = 25.0

    if width <= 0 or height <= 0:

        cap.release()

        raise ValueError(
            "Invalid video dimensions."
        )

    # --------------------------------------------------
    # Create output directory
    # --------------------------------------------------

    Path(
        output_path
    ).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------
    # Create video writer
    # --------------------------------------------------

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():

        cap.release()

        logger.error(
            f"Unable to create output video | "
            f"job_id={job_id}"
        )

        raise ValueError(
            "Unable to create output video."
        )

    # --------------------------------------------------
    # Processing variables
    # --------------------------------------------------

    processed_frames = 0
    total_detections = 0

    # --------------------------------------------------
    # Process frames
    # --------------------------------------------------

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            # --------------------------------------------------
            # YOLO prediction
            # --------------------------------------------------

            results = detector.predict(
                frame,
                confidence=confidence,
            )

            detection_count = 0

            for result in results:

                if result.boxes is not None:

                    detection_count += len(
                        result.boxes
                    )

                frame = result.plot()

            # --------------------------------------------------
            # Update statistics
            # --------------------------------------------------

            processed_frames += 1

            total_detections += (
                detection_count
            )

            # --------------------------------------------------
            # Add frame information
            # --------------------------------------------------

            cv2.putText(
                frame,
                (
                    f"Frame: "
                    f"{processed_frames}/"
                    f"{total_frames}"
                ),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            # --------------------------------------------------
            # Calculate progress
            # --------------------------------------------------

            progress = int(
                (
                    processed_frames
                    / total_frames
                ) * 100
            )

            if progress_callback:

                progress_callback(
                    progress
                )

            # --------------------------------------------------
            # Write frame
            # --------------------------------------------------

            writer.write(frame)

    except Exception as e:

        logger.error(
            f"Frame processing failed | "
            f"job_id={job_id} "
            f"error={str(e)}",
            exc_info=True,
        )

        raise

    finally:

        cap.release()
        writer.release()

    # --------------------------------------------------
    # Processing statistics
    # --------------------------------------------------

    processing_time = (
        time.time() - start_time
    )

    average_fps = (
        processed_frames
        / processing_time
        if processing_time > 0
        else 0
    )

    logger.info(
        f"Video processing completed | "
        f"job_id={job_id} "
        f"frames={processed_frames} "
        f"detections={total_detections} "
        f"time={processing_time:.2f}s"
    )

    return {
        "total_frames": total_frames,
        "processed_frames": processed_frames,
        "total_detections": total_detections,
        "average_fps": round(
            average_fps,
            2,
        ),
        "processing_time": round(
            processing_time,
            2,
        ),
        "confidence": confidence,
    }