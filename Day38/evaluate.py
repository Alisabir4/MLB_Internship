from ultralytics import YOLO

model = YOLO("runs/detect/runs/cup_model-3/weights/best.pt")

results = model.val(
    data="augmented_dataset/data.yaml",
    imgsz=640,
    batch=4
)

print("Evaluation completed.")
print("Precision:", results.box.mp)
print("Recall:", results.box.mr)
print("mAP@50:", results.box.map50)
print("mAP@50-95:", results.box.map)