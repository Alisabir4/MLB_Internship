import streamlit as st
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import yaml
from ultralytics import YOLO

st.set_page_config(
    page_title="YOLO Model Performance Audit",
    layout="wide"
)

st.title("YOLO Model Performance Audit")

MODEL_PATH = "yolov8n.pt"
DATA_YAML = "data.yaml"
IMAGE_DIR = "test100/images"
LABEL_DIR = "test100/labels"
RESULT_DIR = "results"

os.makedirs(RESULT_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

CLASS_NAMES = [
    "bicycle",
    "bus",
    "car",
    "motorcycle",
    "person",
    "truck"
]

# COCO class ID -> Traffic class ID
COCO_TO_TRAFFIC = {
    1: 0,   # bicycle
    5: 1,   # bus
    2: 2,   # car
    3: 3,   # motorcycle
    0: 4,   # person
    7: 5    # truck
}


# -------------------------------------------------
# CONFUSION MATRIX
# -------------------------------------------------

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


def generate_confusion_matrix():

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

        ground_truth = []

        with open(label_path, "r") as file:

            for line in file:

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

        results = model.predict(
            image,
            conf=0.25,
            iou=0.50,
            verbose=False
        )[0]

        predictions = []

        if results.boxes is not None:

            boxes = results.boxes.xyxy.cpu().numpy()
            classes = results.boxes.cls.cpu().numpy()

            for box, cls in zip(boxes, classes):

                coco_class = int(cls)

                if coco_class not in COCO_TO_TRAFFIC:
                    continue

                predictions.append(
                    [
                        COCO_TO_TRAFFIC[coco_class],
                        box.tolist()
                    ]
                )

        matched_gt = set()
        matched_predictions = set()

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

                gt_class = ground_truth[best_gt][0]

                confusion[gt_class][pred_class] += 1

                matched_gt.add(best_gt)
                matched_predictions.add(pred_index)

        # Missed objects
        for gt_index, (gt_class, _) in enumerate(ground_truth):

            if gt_index not in matched_gt:
                confusion[gt_class][6] += 1

        # False detections
        for pred_index, (pred_class, _) in enumerate(predictions):

            if pred_index not in matched_predictions:
                confusion[6][pred_class] += 1

    # Plot
    labels = CLASS_NAMES + ["background"]

    fig, ax = plt.subplots(figsize=(9, 7))

    im = ax.imshow(confusion)

    fig.colorbar(im, ax=ax)

    ax.set_xticks(range(7))
    ax.set_yticks(range(7))

    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Traffic-200 Confusion Matrix")

    for i in range(7):
        for j in range(7):

            ax.text(
                j,
                i,
                confusion[i, j],
                ha="center",
                va="center"
            )

    plt.tight_layout()

    matrix_path = os.path.join(
        RESULT_DIR,
        "traffic_confusion_matrix.png"
    )

    plt.savefig(
        matrix_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    return matrix_path


# -------------------------------------------------
# MODEL EVALUATION
# -------------------------------------------------

st.header("Model Evaluation")

if st.button("Run Evaluation"):

    if not os.path.exists(DATA_YAML):

        st.error(
            "data.yaml not found. Keep data.yaml and test100 folder "
            "in the project for evaluation."
        )

    elif not os.path.exists(IMAGE_DIR):

        st.error(
            "test100/images not found."
        )

    else:

        with st.spinner("Running YOLOv8 evaluation..."):

            results = model.val(
                data=DATA_YAML,
                split="test",
                imgsz=640,
                conf=0.25,
                iou=0.50,
                plots=False,
                verbose=True
            )

            precision = float(results.box.mp)
            recall = float(results.box.mr)
            map50 = float(results.box.map50)
            map5095 = float(results.box.map)

        st.success("Evaluation completed.")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Precision",
            f"{precision:.4f}"
        )

        col2.metric(
            "Recall",
            f"{recall:.4f}"
        )

        col3.metric(
            "mAP@50",
            f"{map50:.4f}"
        )

        col4.metric(
            "mAP@50-95",
            f"{map5095:.4f}"
        )

        # Save metrics
        with open(
            os.path.join(RESULT_DIR, "metrics.txt"),
            "w"
        ) as file:

            file.write(
                f"Precision : {precision:.4f}\n"
                f"Recall    : {recall:.4f}\n"
                f"mAP@50    : {map50:.4f}\n"
                f"mAP@50-95 : {map5095:.4f}\n"
            )

        # Generate custom 6-class confusion matrix
        with st.spinner("Generating confusion matrix..."):

            matrix_path = generate_confusion_matrix()

        st.header("Confusion Matrix")

        st.image(
            matrix_path,
            caption="Traffic-200 6-Class Confusion Matrix",
            use_container_width=True
        )


# -------------------------------------------------
# CHALLENGING EXAMPLES
# -------------------------------------------------

st.header("Challenging Examples")

uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded is not None:

    file_bytes = np.asarray(
        bytearray(uploaded.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    if image is not None:

        results = model.predict(
            source=image,
            conf=0.25,
            iou=0.50,
            verbose=False
        )

        annotated = results[0].plot()

        st.image(
            cv2.cvtColor(
                annotated,
                cv2.COLOR_BGR2RGB
            ),
            caption="YOLOv8 Prediction",
            use_container_width=True
        )