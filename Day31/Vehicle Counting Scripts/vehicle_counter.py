import cv2
from ultralytics import YOLO


class VehicleCounter:

    def __init__(self, model_path="yolov8n.pt"):

        self.model = YOLO(model_path)

        # COCO classes
        # 2 = Car
        # 7 = Truck
        self.vehicle_classes = [2, 7]

        self.counted_ids = set()

        self.car_count = 0
        self.truck_count = 0
        self.total_count = 0

        self.line_y = 350

    def process_video(self, input_path, output_path):

        cap = cv2.VideoCapture(input_path)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        writer = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            results = self.model.track(
                frame,
                persist=True,
                classes=self.vehicle_classes,
                verbose=False
            )

            cv2.line(
                frame,
                (0, self.line_y),
                (width, self.line_y),
                (0, 255, 255),
                3
            )

            if results[0].boxes.id is not None:

                boxes = results[0].boxes.xyxy.cpu().numpy()
                ids = results[0].boxes.id.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy()

                for box, track_id, cls in zip(boxes, ids, classes):

                    x1, y1, x2, y2 = map(int, box)

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    if int(cls) == 2:
                        label = "Car"
                        color = (0, 255, 0)
                    else:
                        label = "Truck"
                        color = (255, 0, 0)

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        color,
                        2
                    )

                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

                    cv2.putText(
                        frame,
                        f"{label} ID:{track_id}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2
                    )

                    if abs(cy - self.line_y) < 5:

                        if track_id not in self.counted_ids:

                            self.counted_ids.add(track_id)

                            self.total_count += 1

                            if label == "Car":
                                self.car_count += 1
                            else:
                                self.truck_count += 1

            cv2.putText(
                frame,
                f"Cars : {self.car_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Trucks : {self.truck_count}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"Total : {self.total_count}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            writer.write(frame)

            # IMPORTANT:
            # This sends the processed frame to Streamlit immediately.
            yield frame, self.car_count, self.truck_count, self.total_count

        cap.release()
        writer.release()