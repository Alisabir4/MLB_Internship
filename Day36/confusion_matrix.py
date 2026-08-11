from ultralytics import YOLO
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

MODEL_PATH = "yolov8n.pt"
IMAGE_DIR = "test100/images"
LABEL_DIR = "test100/labels"

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

# COCO ID -> traffic class
COCO_TO_TRAFFIC = {
    1: 0,  # bicycle
    5: 1,  # bus
    2: 2,  # car
    3: 3,  # motorcycle
    0: 4,  # person
    7: 5   # truck
}

CLASS_NAMES = [
    "bicycle",
    "bus",
    "car",
    "motorcycle",
    "person",
    "truck",
    "background"
]

def calculate_iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = max(0, box1[2] - box1[0]) * max(0, box1[3] - box1[1])
    area2 = max(0, box2[2] - box2[0]) * max(0, box2[3] - box2[1])

    union = area1 + area2 - intersection

    if union == 0:
        return 0

    return intersection / union


confusion = np.zeros((7, 7), dtype=int)

images = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

for image_name in images:

    image_path = os.path.join(IMAGE_DIR, image_name)
    label_path = os.path.join(
        LABEL_DIR,
        os.path.splitext(image_name)[0] + ".txt"
    )

    image = cv2.imread(image_path)

    if image is None or not os.path.exists(label_path):
        continue

    height, width = image.shape[:2]

    # Ground truth
    ground_truth = []

    with open(label_path, "r") as f:
        for line in f:

            parts = line.strip().split()

            if len(parts) != 5:
                continue

            class_id = int(parts[0])

            if class_id not in COCO_TO_TRAFFIC:
                continue

            x_center = float(parts[1]) * width
            y_center = float(parts[2]) * height
            box_width = float(parts[3]) * width
            box_height = float(parts[4]) * height

            box = [
                x_center - box_width / 2,
                y_center - box_height / 2,
                x_center + box_width / 2,
                y_center + box_height / 2
            ]

            ground_truth.append(
                [COCO_TO_TRAFFIC[class_id], box]
            )

    # Predictions
    result = model.predict(
        image,
        conf=0.25,
        iou=0.50,
        verbose=False
    )[0]

    predictions = []

    if result.boxes is not None:

        for box, cls in zip(
            result.boxes.xyxy.cpu().numpy(),
            result.boxes.cls.cpu().numpy()
        ):

            coco_class = int(cls)

            if coco_class not in COCO_TO_TRAFFIC:
                continue

            predictions.append(
                [COCO_TO_TRAFFIC[coco_class], box.tolist()]
            )

    matched_gt = set()
    matched_pred = set()

    matches = []

    # Match predictions to ground truth using IoU
    for pred_index, (pred_class, pred_box) in enumerate(predictions):

        best_iou = 0
        best_gt = None

        for gt_index, (gt_class, gt_box) in enumerate(ground_truth):

            if gt_index in matched_gt:
                continue

            iou = calculate_iou(pred_box, gt_box)

            if iou > best_iou:
                best_iou = iou
                best_gt = gt_index

        if best_gt is not None and best_iou >= 0.50:

            matched_gt.add(best_gt)
            matched_pred.add(pred_index)

            gt_class = ground_truth[best_gt][0]

            confusion[gt_class][pred_class] += 1

    # Missed objects
    for gt_index, (gt_class, _) in enumerate(ground_truth):

        if gt_index not in matched_gt:
            confusion[gt_class][6] += 1

    # False detections
    for pred_index, (pred_class, _) in enumerate(predictions):

        if pred_index not in matched_pred:
            confusion[6][pred_class] += 1


# Plot confusion matrix
plt.figure(figsize=(10, 8))

plt.imshow(confusion, interpolation="nearest")
plt.title("Traffic-200 Confusion Matrix")
plt.colorbar()

plt.xticks(
    range(7),
    CLASS_NAMES,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(7),
    CLASS_NAMES
)

for i in range(7):
    for j in range(7):

        if confusion[i, j] > 0:
            plt.text(
                j,
                i,
                confusion[i, j],
                ha="center",
                va="center"
            )

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()

output_path = os.path.join(
    OUTPUT_DIR,
    "traffic_confusion_matrix.png"
)

plt.savefig(
    output_path,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("=" * 50)
print("6-Class Confusion Matrix Generated")
print("=" * 50)
print(f"Saved to: {output_path}")