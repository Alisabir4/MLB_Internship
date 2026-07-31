from ultralytics import YOLO
import os

MODEL = r"D:\python\MLB_Internship\Day29\best.pt"

if not os.path.exists(MODEL):
    print("best.pt not found!")
    exit()

model = YOLO(MODEL)

print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

metrics = model.val()

print("\nEvaluation Completed\n")

print(metrics)

print("\nResults Summary")

print("----------------------------")

print("Precision :", metrics.box.mp)

print("Recall    :", metrics.box.mr)

print("mAP50     :", metrics.box.map50)

print("mAP50-95  :", metrics.box.map)