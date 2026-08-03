import cv2
from collections import defaultdict


def process_video(
    model,
    source_path,
    output_path,
    tracker="bytetrack.yaml",
    conf=0.30,
    progress_callback=None,
):

    cap = cv2.VideoCapture(source_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    unique_ids = set()
    class_counts = defaultdict(set)

    frame_number = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            persist=True,
            tracker=tracker,
            conf=conf,
            verbose=False
        )

        annotated = frame.copy()

        if (
            len(results)
            and results[0].boxes is not None
            and results[0].boxes.id is not None
        ):

            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy().astype(int)
            scores = results[0].boxes.conf.cpu().numpy()

            for box, track_id, cls, score in zip(
                boxes,
                ids,
                classes,
                scores
            ):

                x1, y1, x2, y2 = map(int, box)

                class_name = model.names[int(cls)]

                unique_ids.add(track_id)
                class_counts[class_name].add(track_id)

                label = (
                    f"{class_name} "
                    f"ID:{track_id} "
                    f"{score:.2f}"
                )

                cv2.rectangle(
                    annotated,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    annotated,
                    label,
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        writer.write(annotated)

        frame_number += 1

        if progress_callback:
            progress_callback(frame_number, total_frames)

    cap.release()
    writer.release()

    return {
        "frames": frame_number,
        "unique_object_count": len(unique_ids),
        "per_class_unique_counts": {
            k: len(v)
            for k, v in class_counts.items()
        },
        "output_path": output_path,
    }