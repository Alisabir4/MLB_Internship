from cv2 import cv2
from ultralytics import YOLO


class VehicleCounter:

    def __init__(self, model_path="yolov8n.pt"):

        # Load YOLO model
        self.model = YOLO(model_path)

        # COCO Vehicle Classes
        # 2 = Car
        # 3 = Motorcycle
        # 5 = Bus
        # 7 = Truck
        self.vehicle_classes = [2, 3, 5, 7]

        # Counted IDs
        self.counted_ids = set()

        # Counters
        self.car_count = 0
        self.motorcycle_count = 0
        self.bus_count = 0
        self.truck_count = 0
        self.total_count = 0

        # Counting line position
        self.line_y = 350

    def process_video(self, input_path, output_path):

        cap = cv2.VideoCapture(input_path)

        if not cap.isOpened():
            raise Exception("Unable to open video.")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps == 0:
            fps = 30

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

            # YOLO Tracking
            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                classes=self.vehicle_classes,
                conf=0.30,
                verbose=False
            )

            # Draw Counting Line
            cv2.line(
                frame,
                (0, self.line_y),
                (width, self.line_y),
                (0, 255, 255),
                3
            )

            # Skip frame if no detections
            if len(results) == 0:

                writer.write(frame)

                yield (
                    frame,
                    self.car_count,
                    self.motorcycle_count,
                    self.bus_count,
                    self.truck_count,
                    self.total_count
                )

                continue

            # Skip frame if tracker IDs are unavailable
            if results[0].boxes.id is None:

                writer.write(frame)

                yield (
                    frame,
                    self.car_count,
                    self.motorcycle_count,
                    self.bus_count,
                    self.truck_count,
                    self.total_count
                )

                continue

            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            classes = results[0].boxes.cls.cpu().numpy()
            confidences = results[0].boxes.conf.cpu().numpy()
                        # Process every detected vehicle
            for box, track_id, cls, conf in zip(
                boxes,
                ids,
                classes,
                confidences
            ):

                x1, y1, x2, y2 = map(int, box)

                # Center Point
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # Vehicle Class
                if int(cls) == 2:
                    label = "Car"
                    color = (0, 255, 0)

                elif int(cls) == 3:
                    label = "Motorcycle"
                    color = (0, 255, 255)

                elif int(cls) == 5:
                    label = "Bus"
                    color = (255, 0, 255)

                elif int(cls) == 7:
                    label = "Truck"
                    color = (255, 0, 0)

                else:
                    continue

                # Bounding Box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                # Center Point
                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    (0, 0, 255),
                    -1
                )

                # Vehicle Label
                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

                # Tracking ID
                cv2.putText(
                    frame,
                    f"ID: {track_id}",
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

                # Count vehicle when crossing line
                if abs(cy - self.line_y) <= 5:

                    if track_id not in self.counted_ids:

                        self.counted_ids.add(track_id)

                        self.total_count += 1

                        if label == "Car":
                            self.car_count += 1

                        elif label == "Motorcycle":
                            self.motorcycle_count += 1

                        elif label == "Bus":
                            self.bus_count += 1

                        elif label == "Truck":
                            self.truck_count += 1
                                        # -----------------------------
            # Display Live Statistics
            # -----------------------------

            cv2.rectangle(frame, (10, 10), (300, 210), (40, 40, 40), -1)

            cv2.putText(
                frame,
                f"Cars : {self.car_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Motorcycles : {self.motorcycle_count}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Buses : {self.bus_count}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"Trucks : {self.truck_count}",
                (20, 145),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"Total : {self.total_count}",
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            # Save processed frame
            writer.write(frame)

            # Send processed frame to Streamlit
            yield (
                frame,
                self.car_count,
                self.motorcycle_count,
                self.bus_count,
                self.truck_count,
                self.total_count
            )

        # -----------------------------
        # Release Resources
        # -----------------------------
        cap.release()
        writer.release()