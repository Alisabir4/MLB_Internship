from pathlib import Path

from ultralytics import YOLO


# --------------------------------------------------
# Model Path
# --------------------------------------------------

BASE_DIR = Path(
    __file__
).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "best.pt"
)


# --------------------------------------------------
# Check Model
# --------------------------------------------------

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"YOLO model not found: {MODEL_PATH}"
    )


# --------------------------------------------------
# YOLO Detector
# --------------------------------------------------

class YOLODetector:

    def __init__(self):

        self.model = YOLO(
            str(MODEL_PATH)
        )

    def predict(
        self,
        frame,
        confidence: float = 0.25,
    ):

        return self.model.predict(
            source=frame,
            conf=confidence,
            verbose=False,
        )


# --------------------------------------------------
# Global Detector Instance
# --------------------------------------------------

detector = YOLODetector()