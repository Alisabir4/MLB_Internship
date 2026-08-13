from ultralytics import YOLO

model = YOLO("runs/detect/runs/cup_model-3/weights/best.pt")

model.predict(
    source="unseen_test/images",
    save=True,
    conf=0.25,
    project="unseen_test",
    name="predictions"
)

print("Prediction completed.")