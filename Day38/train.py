from ultralytics import YOLO
import time

model = YOLO("yolov8n.pt")

start = time.time()

results = model.train(
    data="augmented_dataset/data.yaml",
    epochs=10,
    imgsz=640,
    batch=8,
    project="runs",
    name="cup_model"
)

end = time.time()

print("Training completed.")
print(f"Training time: {(end - start) / 60:.2f} minutes")