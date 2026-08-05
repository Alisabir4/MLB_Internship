import cv2
import os
from ultralytics import YOLO


class PeopleCounter:

    def __init__(
        self,
        model_path="yolov8n.pt",
        conf=0.30,
        tracker="bytetrack.yaml"
    ):

        self.model = YOLO(model_path)
        self.conf = conf
        self.tracker = tracker

    # ---------------------------------------
    # IMAGE DETECTION
    # ---------------------------------------
    def process_image(self, image_path, output_path):

        image = cv2.imread(image_path)

        results = self.model.predict(
            image,
            conf=self.conf,
            verbose=False
        )

        people_count = 0

        result = results[0]

        if result.boxes is not None:

            for box in result.boxes:

                cls = int(box.cls[0])

                if cls != 0:
                    continue

                people_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    image,
                    f"{confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        cv2.rectangle(image, (10, 10), (250, 60), (0, 0, 0), -1)

        cv2.putText(
            image,
            f"People : {people_count}",
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        cv2.imwrite(output_path, image)

        return image, people_count

    # ---------------------------------------
    # VIDEO DETECTION
    # ---------------------------------------
    def process_video_live(self, input_path, output_path):

        cap = cv2.VideoCapture(input_path)

        if not cap.isOpened():
            raise Exception("Cannot open video.")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 30

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        writer = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        peak_people = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            results = self.model.track(
                frame,
                persist=True,
                tracker=self.tracker,
                conf=self.conf,
                verbose=False
            )

            people_count = 0

            if len(results):

                result = results[0]

                if result.boxes is not None:

                    for box in result.boxes:

                        cls = int(box.cls[0])

                        if cls != 0:
                            continue

                        people_count += 1

                        x1, y1, x2, y2 = map(
                            int,
                            box.xyxy[0]
                        )

                        confidence = float(box.conf[0])

                        track_id = -1

                        if box.id is not None:
                            track_id = int(box.id[0])

                        cv2.rectangle(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (0, 255, 0),
                            2
                        )

                        cv2.putText(
                            frame,
                            f"ID:{track_id} {confidence:.2f}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2
                        )

            peak_people = max(
                peak_people,
                people_count
            )

            cv2.rectangle(
                frame,
                (10, 10),
                (320, 90),
                (0, 0, 0),
                -1
            )

            cv2.putText(
                frame,
                f"People : {people_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Peak : {peak_people}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            writer.write(frame)

            yield frame, people_count, peak_people

        cap.release()
        writer.release()