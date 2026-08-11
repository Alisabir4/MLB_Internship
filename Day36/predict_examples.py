from ultralytics import YOLO
import os
import shutil

MODEL_PATH = "yolov8n.pt"
IMAGE_DIR = "test100/images"
OUTPUT_DIR = "predictions"

os.makedirs(OUTPUT_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

images = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

# Process all 100 images
for image_name in images:

    image_path = os.path.join(
        IMAGE_DIR,
        image_name
    )

    results = model.predict(
        source=image_path,
        conf=0.25,
        iou=0.50,
        imgsz=640,
        save=False,
        verbose=False
    )

    annotated = results[0].plot()

    output_path = os.path.join(
        OUTPUT_DIR,
        image_name
    )

    # Save annotated prediction
    import cv2
    cv2.imwrite(output_path, annotated)

print("=" * 50)
print("Prediction generation completed")
print("=" * 50)
print(f"Images processed : {len(images)}")
print(f"Predictions saved: {OUTPUT_DIR}")