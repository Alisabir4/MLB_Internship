import os
import random
import streamlit as st
from PIL import Image, ImageDraw

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Day 38 - Custom Dataset",
    page_icon="🥤",
    layout="wide"
)

st.title("🥤 Day 38 - Custom Object Detection Dataset")

DATASET = "dataset"
CLASSES = ["black", "white"]


# =========================
# DATASET ANALYSIS
# =========================

def analyze_dataset():

    results = {}

    for split in ["train", "valid", "test"]:

        image_dir = os.path.join(DATASET, split, "images")
        label_dir = os.path.join(DATASET, split, "labels")

        if not os.path.exists(image_dir):
            results[split] = None
            continue

        images = [
            f for f in os.listdir(image_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        labels = [
            f for f in os.listdir(label_dir)
            if f.endswith(".txt")
        ]

        class_count = {name: 0 for name in CLASSES}
        missing = []

        for image in images:

            name = os.path.splitext(image)[0]
            label_file = os.path.join(label_dir, name + ".txt")

            if not os.path.exists(label_file):
                missing.append(image)
                continue

            with open(label_file, "r") as file:

                for line in file:

                    parts = line.strip().split()

                    if not parts:
                        continue

                    class_id = int(parts[0])

                    if class_id < len(CLASSES):
                        class_count[CLASSES[class_id]] += 1

        results[split] = {
            "images": len(images),
            "labels": len(labels),
            "annotations": sum(class_count.values()),
            "classes": class_count,
            "missing": missing
        }

    return results


# =========================
# CHECK DATASET
# =========================

if not os.path.exists(DATASET):

    st.error("Dataset folder not found.")

else:

    results = analyze_dataset()

    st.header("📊 Dataset Statistics")

    train = results["train"]
    valid = results["valid"]
    test = results["test"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Original Images",
        sum(
            results[s]["images"]
            for s in ["train", "valid", "test"]
            if results[s]
        )
    )

    col2.metric(
        "Train",
        train["images"] if train else 0
    )

    col3.metric(
        "Validation",
        valid["images"] if valid else 0
    )

    col4.metric(
        "Test",
        test["images"] if test else 0
    )


    # =========================
    # SPLIT DETAILS
    # =========================

    st.header("Dataset Split")

    for split in ["train", "valid", "test"]:

        data = results[split]

        if data:

            st.subheader(split.capitalize())

            c1, c2, c3, c4 = st.columns(4)

            c1.write(f"**Images:** {data['images']}")
            c2.write(f"**Labels:** {data['labels']}")
            c3.write(f"**Annotations:** {data['annotations']}")
            c4.write(
                f"**Missing:** {len(data['missing'])}"
            )


    # =========================
    # CLASS DISTRIBUTION
    # =========================

    st.header("Class Distribution")

    total_classes = {name: 0 for name in CLASSES}

    for split in ["train", "valid", "test"]:

        data = results[split]

        if data:

            for class_name in CLASSES:
                total_classes[class_name] += data["classes"][class_name]

    col1, col2 = st.columns(2)

    col1.metric("Black", total_classes["black"])
    col2.metric("White", total_classes["white"])


    st.bar_chart(total_classes)


    # =========================
    # MISSING ANNOTATIONS
    # =========================

    st.header("Annotation Check")

    total_missing = 0

    for split in ["train", "valid", "test"]:

        data = results[split]

        if data and data["missing"]:

            total_missing += len(data["missing"])

            st.warning(
                f"{split}: {len(data['missing'])} images without annotations"
            )

    if total_missing == 0:

        st.success(
            "All images have corresponding YOLO annotation files."
        )


    # =========================
    # RANDOM IMAGE
    # =========================

    st.header("Random Annotated Image")

    split = st.selectbox(
        "Select dataset split",
        ["train", "valid", "test"]
    )

    image_dir = os.path.join(DATASET, split, "images")
    label_dir = os.path.join(DATASET, split, "labels")

    images = [
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if images:

        if st.button("Show Random Image"):

            image_name = random.choice(images)

            image_path = os.path.join(
                image_dir,
                image_name
            )

            label_path = os.path.join(
                label_dir,
                os.path.splitext(image_name)[0] + ".txt"
            )

            image = Image.open(image_path).convert("RGB")

            draw = ImageDraw.Draw(image)

            width, height = image.size

            if os.path.exists(label_path):

                with open(label_path, "r") as file:

                    for line in file:

                        parts = line.strip().split()

                        if len(parts) != 5:
                            continue

                        class_id = int(parts[0])
                        x_center = float(parts[1])
                        y_center = float(parts[2])
                        box_width = float(parts[3])
                        box_height = float(parts[4])

                        x1 = int(
                            (x_center - box_width / 2) * width
                        )

                        y1 = int(
                            (y_center - box_height / 2) * height
                        )

                        x2 = int(
                            (x_center + box_width / 2) * width
                        )

                        y2 = int(
                            (y_center + box_height / 2) * height
                        )

                        class_name = (
                            CLASSES[class_id]
                            if class_id < len(CLASSES)
                            else str(class_id)
                        )

                        draw.rectangle(
                            [x1, y1, x2, y2],
                            outline="red",
                            width=3
                        )

                        draw.text(
                            (x1, max(0, y1 - 15)),
                            class_name,
                            fill="red"
                        )

            st.image(
                image,
                caption=image_name,
                use_container_width=True
            )


    # =========================
    # SUMMARY
    # =========================

    st.header("Dataset Summary")

    st.write(
        "This dataset contains 241 original images "
        "with YOLO bounding-box annotations."
    )

    st.write(
        "Classes: black and white"
    )

    st.write(
        "Validation and test images remain untouched."
    )