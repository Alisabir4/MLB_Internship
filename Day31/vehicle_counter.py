import cv2
from ultralytics import YOLO
import os


# Vehicle classes from COCO dataset
VEHICLE_CLASSES = {
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    7: "Truck"
}


class VehicleCounter:

    def __init__(self, model_path="yolov8n.pt"):

        self.model = YOLO(model_path)

        self.vehicle_count = {
            "Car": 0,
            "Motorcycle": 0,
            "Bus": 0,
            "Truck": 0
        }

        self.counted_ids = set()



    def process_video(self, input_video, output_video):

        cap = cv2.VideoCapture(input_video)


        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = cap.get(cv2.CAP_PROP_FPS)


        # Video writer

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        out = cv2.VideoWriter(
            output_video,
            fourcc,
            fps,
            (width,height)
        )


        # Counting line

        line_y = int(height * 0.55)


        while True:

            ret, frame = cap.read()

            if not ret:
                break



            results = self.model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                verbose=False
            )



            # Draw counting line

            cv2.line(
                frame,
                (0,line_y),
                (width,line_y),
                (0,255,0),
                3
            )



            if results[0].boxes.id is not None:


                boxes = results[0].boxes.xyxy.cpu().numpy()

                ids = results[0].boxes.id.cpu().numpy()

                classes = results[0].boxes.cls.cpu().numpy()



                for box,track_id,cls in zip(
                    boxes,
                    ids,
                    classes
                ):


                    cls = int(cls)

                    if cls not in VEHICLE_CLASSES:
                        continue



                    x1,y1,x2,y2 = map(int,box)


                    center_x = int((x1+x2)/2)
                    center_y = int((y1+y2)/2)



                    # Count crossing

                    if (
                        center_y > line_y
                        and track_id not in self.counted_ids
                    ):

                        self.counted_ids.add(track_id)


                        vehicle_name = VEHICLE_CLASSES[cls]

                        self.vehicle_count[vehicle_name]+=1



                    # Draw box

                    cv2.rectangle(
                        frame,
                        (x1,y1),
                        (x2,y2),
                        (255,0,0),
                        2
                    )


                    cv2.circle(
                        frame,
                        (center_x,center_y),
                        5,
                        (0,0,255),
                        -1
                    )


                    cv2.putText(
                        frame,
                        f"{VEHICLE_CLASSES[cls]} ID:{int(track_id)}",
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255,255,255),
                        2
                    )



            # Display counter


            y = 40

            total = 0


            for name,count in self.vehicle_count.items():

                total += count

                cv2.putText(
                    frame,
                    f"{name}: {count}",
                    (20,y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,255),
                    2
                )

                y += 35



            cv2.putText(
                frame,
                f"Total Vehicles: {total}",
                (20,y+10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                3
            )



            out.write(frame)



        cap.release()
        out.release()


        return self.vehicle_count