from pathlib import Path
from ultralytics import YOLO


MODEL_PATH = Path("models/best.pt")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"YOLO model not found: {MODEL_PATH}"
    )


class YOLODetector:
    def __init__(self):
        self.model = YOLO(str(MODEL_PATH))

    def predict(self, frame):
        return self.model.predict(
            source=frame,
            conf=0.25,
            verbose=False
        )


detector = YOLODetector()