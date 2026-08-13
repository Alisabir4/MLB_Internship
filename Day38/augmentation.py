import os
import cv2
import random
import shutil
import numpy as np

SOURCE_IMAGES = "dataset/train/images"
SOURCE_LABELS = "dataset/train/labels"

OUTPUT_IMAGES = "augmented_dataset/train/images"
OUTPUT_LABELS = "augmented_dataset/train/labels"

os.makedirs(OUTPUT_IMAGES, exist_ok=True)
os.makedirs(OUTPUT_LABELS, exist_ok=True)

TARGET = 650

image_files = [
    f for f in os.listdir(SOURCE_IMAGES)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

# Copy original training images first
for file in image_files:
    shutil.copy(
        os.path.join(SOURCE_IMAGES, file),
        os.path.join(OUTPUT_IMAGES, file)
    )

    label = os.path.splitext(file)[0] + ".txt"

    shutil.copy(
        os.path.join(SOURCE_LABELS, label),
        os.path.join(OUTPUT_LABELS, label)
    )

count = len(image_files)
index = 0

while count < TARGET:

    file = random.choice(image_files)

    image_path = os.path.join(SOURCE_IMAGES, file)
    label_path = os.path.join(
        SOURCE_LABELS,
        os.path.splitext(file)[0] + ".txt"
    )

    image = cv2.imread(image_path)

    if image is None:
        continue

    h, w = image.shape[:2]

    # Read YOLO labels
    boxes = []

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) == 5:
                boxes.append([
                    int(parts[0]),
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3]),
                    float(parts[4])
                ])

    # Random augmentation
    choice = random.choice(["flip", "rotate", "brightness", "scale"])

    if choice == "flip":

        image = cv2.flip(image, 1)

        for box in boxes:
            box[1] = 1 - box[1]

    elif choice == "rotate":

        angle = random.choice([-10, 10])

        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        image = cv2.warpAffine(
            image,
            matrix,
            (w, h)
        )

        for box in boxes:
            x = box[1] * w
            y = box[2] * h

            new_x = (
                matrix[0][0] * x
                + matrix[0][1] * y
                + matrix[0][2]
            )

            new_y = (
                matrix[1][0] * x
                + matrix[1][1] * y
                + matrix[1][2]
            )

            box[1] = max(0, min(1, new_x / w))
            box[2] = max(0, min(1, new_y / h))

    elif choice == "brightness":

        factor = random.uniform(0.7, 1.3)

        image = np.clip(
            image.astype(np.float32) * factor,
            0,
            255
        ).astype(np.uint8)

    elif choice == "scale":

        factor = random.uniform(0.85, 1.15)

        new_w = int(w * factor)
        new_h = int(h * factor)

        image = cv2.resize(
            image,
            (new_w, new_h)
        )

        image = cv2.resize(
            image,
            (w, h)
        )

    output_name = f"aug_{index}_{file}"

    cv2.imwrite(
        os.path.join(OUTPUT_IMAGES, output_name),
        image
    )

    with open(
        os.path.join(
            OUTPUT_LABELS,
            os.path.splitext(output_name)[0] + ".txt"
        ),
        "w"
    ) as f:

        for box in boxes:
            f.write(
                f"{box[0]} {box[1]} {box[2]} "
                f"{box[3]} {box[4]}\n"
            )

    count += 1
    index += 1

print("Augmentation completed.")
print("Original training images:", len(image_files))
print("Final training images:", count)