from pathlib import Path
from ultralytics import YOLO
import cv2


MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "best.pt"


class YOLODetector:
    def __init__(self):
        self.model = YOLO(str(MODEL_PATH))

    def predict(self, image_path: str, confidence: float = 0.5):
        results = self.model.predict(
            source=image_path,
            conf=confidence,
            verbose=False
        )

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence_score = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                class_name = self.model.names[class_id]

                detections.append({
                    "class": class_name,
                    "confidence": round(confidence_score, 4),
                    "bbox": [
                        round(x1, 2),
                        round(y1, 2),
                        round(x2, 2),
                        round(y2, 2)
                    ]
                })

        return detections

    def predict_image(self, image_path: str, confidence: float = 0.5):
        results = self.model.predict(
            source=image_path,
            conf=confidence,
            verbose=False
        )

        result = results[0]

        annotated_image = result.plot()

        return annotated_image


detector = YOLODetector()