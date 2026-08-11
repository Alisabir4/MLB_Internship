from ultralytics import YOLO
import os

MODEL_PATH = "yolov8n.pt"
DATA_PATH = "evaluation.yaml"

RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)

print("=" * 60)
print("YOLOv8 MODEL PERFORMANCE AUDIT")
print("=" * 60)

# Load model
print("\nLoading YOLOv8 Nano model...")
model = YOLO(MODEL_PATH)

# Run validation
print("\nRunning evaluation on 100 images...\n")

results = model.val(
    data=DATA_PATH,
    split="test",
    imgsz=640,
    batch=8,
    conf=0.25,
    iou=0.50,
    plots=True,
    project=RESULTS_DIR,
    name="evaluation"
)

# Get metrics
precision = float(results.box.mp)
recall = float(results.box.mr)
map50 = float(results.box.map50)
map5095 = float(results.box.map)

# Display results
print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"mAP@50    : {map50:.4f}")
print(f"mAP@50-95 : {map5095:.4f}")

# Save metrics
metrics_path = os.path.join(
    RESULTS_DIR,
    "metrics.txt"
)

with open(metrics_path, "w") as f:

    f.write("YOLOv8 Model Performance Audit\n")
    f.write("=" * 40 + "\n\n")

    f.write("Model: yolov8n.pt\n")
    f.write("Evaluation Images: 100\n\n")

    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"mAP@50: {map50:.4f}\n")
    f.write(f"mAP@50-95: {map5095:.4f}\n")

# Per-class results
print("\n" + "=" * 60)
print("PER-CLASS mAP@50-95")
print("=" * 60)

class_maps = results.box.maps

for class_id, score in enumerate(class_maps):

    if score > 0:

        class_name = model.names.get(
            class_id,
            f"class_{class_id}"
        )

        print(
            f"{class_id:2d} | "
            f"{class_name:20s} | "
            f"{score:.4f}"
        )

print("\n" + "=" * 60)
print("Evaluation completed successfully!")
print("=" * 60)

print(f"\nMetrics saved to: {metrics_path}")
print(f"Results saved to: {RESULTS_DIR}/evaluation/")